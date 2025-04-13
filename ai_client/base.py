from abc import ABC, abstractmethod

class BaseClient(ABC):
    """Abstract base class for AI clients."""

    @abstractmethod
    async def get_job_details(self, job: str, notifier) -> None:
        """Fetch job details and send notifications."""
        pass