import os
import re

from app.repository.skill_repository import SkillRepository
from app.repository.vacancy_skills_repository import VacancySkillsRepository
from app.schemas.skill_schema import SkillCreate, FindSkill
from app.schemas.ai_schema import ExtractedSkill, SkillExtractionResult


_SYSTEM_PROMPT = """You are a technical recruiter assistant.
Analyze the job vacancy text and extract concrete, named skills and technologies — not generic concepts.

Return ONLY a valid JSON object in this exact format, no other text:
{"skills": [{"name": "Python", "type": "hard"}, {"name": "Docker", "type": "tool"}, {"name": "Communication", "type": "soft"}]}

Type rules:
- "hard"  — technical knowledge: programming languages, frameworks, libraries, algorithms, protocols
- "soft"  — interpersonal/business skills: communication, teamwork, leadership, time management
- "tool"  — specific named software/platforms/services: Docker, Jira, AWS, GitHub, Figma, PostgreSQL

DO NOT extract generic/abstract concepts that are not concrete technologies — e.g. "Database", "Authorization",
"Authentication", "Web Services", "Architecture", "Testing", "Development". Only extract them if a SPECIFIC
named technology is mentioned (e.g. "PostgreSQL" instead of "Database", "OAuth2" instead of "Authorization").

Naming rules (critical for de-duplication — follow exactly):
- Use the canonical, well-known spelling: "JavaScript" (not "Javascript" or "JS"), "PostgreSQL" (not "Postgres"),
  "Kubernetes" (not "K8s"), "Node.js" (not "NodeJS" or "Node JS")
- Write common acronyms fully uppercase: "REST", "SQL", "CI/CD", "API", "HTML", "CSS", "XML", "JSON"
- Write multi-word technology names with each significant word capitalized: "Machine Learning", "Time Management"
- Never output the same technology twice under different spellings or with/without suffixes
  (pick ONE canonical form, e.g. either "REST" or "REST API", not both)

Examples:
Input: "Ищем Python-разработчика. Нужны: Django, PostgreSQL, Docker, REST API, умение работать в команде."
Output: {"skills": [{"name": "Python", "type": "hard"}, {"name": "Django", "type": "hard"}, {"name": "PostgreSQL", "type": "tool"}, {"name": "Docker", "type": "tool"}, {"name": "REST", "type": "hard"}, {"name": "Teamwork", "type": "soft"}]}

Input: "Опыт работы с Kafka, RabbitMQ, знание SQL, ООП, желателен английский язык, грамотная речь."
Output: {"skills": [{"name": "Kafka", "type": "tool"}, {"name": "RabbitMQ", "type": "tool"}, {"name": "SQL", "type": "hard"}, {"name": "OOP", "type": "hard"}, {"name": "English", "type": "soft"}, {"name": "Communication", "type": "soft"}]}

Rules:
- Each skill name must be concise (1-4 words) and use the canonical spelling described above
- Do not duplicate skills, and do not output near-duplicates with different spelling/casing
- Extract the 5-15 most important and concrete skills — fewer precise skills is better than many vague ones
- Output ONLY the JSON, nothing else
"""

_COMMON_IT_SKILLS = [
    "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++", "C#", "PHP", "Swift",
    "FastAPI", "Django", "Flask", "React", "Vue", "Angular", "Next.js", "Node.js", "Spring",
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Elasticsearch", "ClickHouse",
    "Docker", "Kubernetes", "Git", "Linux", "AWS", "GCP", "Azure", "Terraform", "Ansible",
    "SQLAlchemy", "Pydantic", "Celery", "RabbitMQ", "Kafka", "Nginx",
    "REST", "GraphQL", "gRPC", "HTML", "CSS", "Bootstrap",
    "Pandas", "NumPy", "scikit-learn", "TensorFlow", "PyTorch",
    "CI/CD", "GitHub Actions", "Jenkins", "Jira", "Confluence",
]


class AIService:
    def __init__(
        self,
        skill_repository: SkillRepository,
        vacancy_skills_repository: VacancySkillsRepository,
    ) -> None:
        self.skill_repository = skill_repository
        self.vacancy_skills_repository = vacancy_skills_repository
        self._api_key: str = os.getenv("AI_API_KEY", "")
        self._model: str = os.getenv("AI_MODEL", "gpt-4o-mini")

    def extract_and_save_skills(self, vacancy_id: int, raw_text: str) -> list[str]:
        extracted = self._extract_skills(raw_text)
        skill_ids = [self._get_or_create_skill(s.name, s.type).id for s in extracted]
        self.vacancy_skills_repository.replace_all(vacancy_id, skill_ids)
        return [s.name for s in extracted]

    def calculate_match(self, user_skill_ids: set, vacancy_id: int) -> float:
        vacancy_skill_ids = self.vacancy_skills_repository.get_skill_ids(vacancy_id)
        if not vacancy_skill_ids:
            return 0.0
        matched = user_skill_ids & vacancy_skill_ids
        return round(len(matched) / len(vacancy_skill_ids) * 100, 1)


    def _extract_skills(self, text: str) -> list[ExtractedSkill]:
        if self._api_key:
            try:
                return self._extract_via_openai(text)
            except Exception as e:
                print(f"AI ERROR: {type(e).__name__}: {e}")
        return self._extract_via_regex(text)

    def _extract_via_openai(self, text: str) -> list[ExtractedSkill]:
        from groq import Groq

        client = Groq(api_key=self._api_key)
        completion = client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Job vacancy text:\n{text[:5000]}"},
            ],
            temperature=0.1,
            max_completion_tokens=1024,
        )

        raw_json = completion.choices[0].message.content.strip()
        print(f"\nRaw AI response: {raw_json[:500]}\n")
        match = re.search(r'\{.*\}', raw_json, re.DOTALL)
        if not match:
            return []
        parsed = SkillExtractionResult.model_validate_json(match.group())
        return parsed.skills

    def _extract_via_regex(self, text: str) -> list[ExtractedSkill]:
        print("\nUsing regex fallback for skill extraction...\n")
        found = []
        text_lower = text.lower()
        for skill_name in _COMMON_IT_SKILLS:
            if re.search(r'\b' + re.escape(skill_name.lower()) + r'\b', text_lower):
                found.append(ExtractedSkill(name=skill_name, type="hard"))
        return found

    def _get_or_create_skill(self, name: str, skill_type: str = "hard"):
        from app.core.exceptions import DuplicatedError
        result = self.skill_repository.read_by_options(FindSkill(name__eq=name))
        if result["founds"]:
            return result["founds"][0]
        try:
            return self.skill_repository.create(SkillCreate(name=name, category=skill_type))
        except DuplicatedError:
            result = self.skill_repository.read_by_options(FindSkill(name__eq=name))
            return result["founds"][0]
