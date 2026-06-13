import asyncio
from datetime import datetime, timezone
from typing import Optional

from app.services.parser_service import ParserService


class ParserScheduler:
    """Singleton service that manages a background periodic parser task."""

    def __init__(self, parser_service: ParserService) -> None:
        self._parser_service = parser_service
        self._task: Optional[asyncio.Task] = None
        self._run_once_task: Optional[asyncio.Task] = None
        self._interval_minutes: int = 60
        self._last_run: Optional[datetime] = None
        self._last_result: Optional[dict] = None

    @property
    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    def start(self, interval_minutes: int = 60) -> dict:
        if self.is_running:
            return {"status": "already_running", "interval_minutes": self._interval_minutes}
        self._interval_minutes = interval_minutes
        self._task = asyncio.create_task(self._loop())
        return {"status": "started", "interval_minutes": interval_minutes}

    def stop(self) -> dict:
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = None
        return {"status": "stopped"}

    def status(self) -> dict:
        return {
            "is_running": self.is_running,
            "interval_minutes": self._interval_minutes,
            "last_run": self._last_run.isoformat() if self._last_run else None,
            "last_result": self._last_result,
        }

    def run_once_background(self) -> dict:
        """Запускает одиночный парсинг как фоновую asyncio-задачу."""
        if self._run_once_task and not self._run_once_task.done():
            return {"status": "already_running_once"}
        self._run_once_task = asyncio.create_task(self._run_once_async())
        return {"status": "started_once"}

    async def _run_once_async(self) -> None:
        self._last_run = datetime.now(timezone.utc)
        try:
            self._last_result = await self._parser_service.parse_habr()
        except Exception as exc:
            self._last_result = {"error": str(exc)}

    async def _loop(self) -> None:
        while True:
            self._last_run = datetime.now(timezone.utc)
            try:
                self._last_result = await self._parser_service.parse_habr()
            except Exception as exc:
                self._last_result = {"error": str(exc)}
            try:
                await asyncio.sleep(self._interval_minutes * 10)
            except asyncio.CancelledError:
                break
