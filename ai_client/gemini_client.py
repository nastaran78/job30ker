import typing
from google import genai
from google.genai import types

from ai_client.base import BaseClient
from prompt.prompts import generate_prompt


class JobInfo(typing.TypedDict):
    """TypedDict for job information."""
    GOOD_MATCH: bool
    SCORE: int
    JOB_ID: str
    JOB_NAME: str
    JOB_COMPANY: str
    JOB_LOCATION: str
    JOB_LINK: str
    JOB_EXPERIENCE: typing.Literal[
        'Internship',
        'Entry level',
        'Associate',
        'Mid - Senior level',
        'Director',
        'Executive'
    ]
    JOB_TYPE: typing.Literal['full-time', 'part-time', 'internship', 'working-student']
    JOB_REMOTE: typing.Literal['remote', 'hybrid', 'on-site']
    JOB_DESC_PROS: list[str]
    JOB_DESC_CONS: list[str]


class GeminiClient(BaseClient):
    """Client for interacting with the Gemini API."""
    MODEL_NAME = 'gemini-2.0-flash'

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def create_chat(self):
        """Create a chat session with the Gemini model."""
        return self.client.chats.create(model=self.MODEL_NAME)

    async def get_job_details(self, job: str, notifier) -> None:
        """
        Fetch job details from the Gemini API and send a notification if the job is a good match.

        Args:
            job (str): Job description to process.
            notifier: Notifier instance for sending messages.
        """
        try:
            chat = self.create_chat()
            response = chat.send_message(
                generate_prompt(job),
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=JobInfo,
                ),
            )
            parsed_response = response.parsed
            if parsed_response.get('SCORE', 0) > 60 or parsed_response.get('GOOD_MATCH', False):
                await notifier.send_message(parsed_response)
        except Exception as e:
            raise RuntimeError(f"Error fetching job details: {e}")
