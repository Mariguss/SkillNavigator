import asyncio
import random
import re
import feedparser
import httpx
from bs4 import BeautifulSoup

from app.repository.vacancy_repository import VacancyRepository
from app.repository.company_repository import CompanyRepository
from app.schemas.vacancy_schema import VacancyCreate
from app.schemas.company_schema import CompanyCreate, FindCompany
from app.core.exceptions import DuplicatedError

HABR_RSS_URL = "https://career.habr.com/vacancies/rss?currency=RUR&sort=relevance&type=all"

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
]

_RSS_RETRY_DELAYS = [5, 15, 45]  # секунды между попытками при 429/503


def _random_headers(referer: str = "https://career.habr.com/") -> dict:
    return {
        "User-Agent": random.choice(_USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": referer,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


class ParserService:
    def __init__(
        self,
        vacancy_repository: VacancyRepository,
        company_repository: CompanyRepository,
    ) -> None:
        self.vacancy_repository = vacancy_repository
        self.company_repository = company_repository
        self._ai_service = None  # внедряется после создания через set_ai_service()

    def set_ai_service(self, ai_service) -> None:
        self._ai_service = ai_service

    async def parse_habr(self) -> dict:
        added, skipped, errors = 0, 0, []

        rss_content = await self._fetch_rss_with_retry(HABR_RSS_URL)
        if rss_content is None:
            return {"added": 0, "skipped": 0, "errors": ["Не удалось загрузить RSS после нескольких попыток"]}

        feed = feedparser.parse(rss_content)

        for entry in feed.entries:
            try:
                title = str(entry.get("title", "")).replace("Требуется ", "").strip()
                url = str(entry.get("link", "")).strip()

                company_name = (
                    str(entry.get("author", "")).strip()
                    or str(entry.get("author_detail", {}).get("name", "")).strip()
                    or "Unknown"
                )

                if not url or not title:
                    skipped += 1
                    continue

                # Случайная задержка между запросами страниц вакансий
                await asyncio.sleep(random.uniform(1.5, 4.0))

                raw_text = await self._fetch_vacancy_text(url)
                if not raw_text:
                    raw_text = str(entry.get("summary", ""))

                company = self._get_or_create_company(company_name)

                try:
                    vacancy = self.vacancy_repository.create(
                        VacancyCreate(
                            company_id=company.id,
                            title=title,
                            url=url,
                            raw_text=raw_text,
                            is_active=True,
                        )
                    )
                    added += 1

                    # запускаем AI-извлечение навыков фоново, не блокируя парсер
                    if self._ai_service is not None and raw_text:
                        vacancy_id = vacancy.id
                        ai_svc = self._ai_service
                        asyncio.create_task(
                            asyncio.to_thread(ai_svc.extract_and_save_skills, vacancy_id, raw_text)
                        )

                except DuplicatedError:
                    skipped += 1

            except Exception as exc:
                errors.append(str(exc))

        return {"added": added, "skipped": skipped, "errors": errors}

    async def _fetch_rss_with_retry(self, url: str) -> bytes | None:
        """Загружает RSS с повторными попытками при 429/503."""
        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            for attempt, delay in enumerate([0] + _RSS_RETRY_DELAYS):
                if delay:
                    await asyncio.sleep(delay)
                try:
                    resp = await client.get(url, headers=_random_headers(referer="https://career.habr.com/"))
                    if resp.status_code in (429, 503):
                        continue  # повторяем с задержкой
                    resp.raise_for_status()
                    return resp.content
                except httpx.HTTPStatusError:
                    if attempt == len(_RSS_RETRY_DELAYS):
                        return None
                except Exception:
                    if attempt == len(_RSS_RETRY_DELAYS):
                        return None
        return None

    async def _fetch_vacancy_text(self, url: str) -> str:
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=12.0) as client:
                resp = await client.get(url, headers=_random_headers(referer=HABR_RSS_URL))
                if resp.status_code == 429:
                    # Короткая пауза и ещё одна попытка
                    await asyncio.sleep(random.uniform(5.0, 10.0))
                    resp = await client.get(url, headers=_random_headers(referer=HABR_RSS_URL))
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            body = (
                soup.find("div", class_=re.compile(r"vacancy.*description|job.*description", re.I))
                or soup.find("article")
                or soup.find("main")
                or soup.body
            )
            text = (body or soup).get_text(separator=" ", strip=True)
            return re.sub(r"\s+", " ", text).strip()[:12000]
        except Exception:
            return ""

    def _get_or_create_company(self, name: str):
        result = self.company_repository.read_by_options(FindCompany(name__eq=name))
        if result["founds"]:
            return result["founds"][0]
        try:
            return self.company_repository.create(CompanyCreate(name=name))
        except DuplicatedError:
            result = self.company_repository.read_by_options(FindCompany(name__eq=name))
            return result["founds"][0]
