from unittest.mock import patch, Mock, AsyncMock
import pytest

from ai_client.gemini_client import GeminiClient


@pytest.fixture
def mocked_gemini_client():
    def func(score):
        with patch("ai_client.gemini_client.genai.Client") as mock_genai:
            mock_chat = Mock()
            mock_response = Mock()
            mock_response.parsed = {"SCORE": score}

            mock_chat.send_message.return_value = mock_response
            mock_genai.return_value.chats.create.return_value = mock_chat

            client = GeminiClient("test-api-key-nastaran")
            return client

    return func


class TestGeminiClient:
    @pytest.mark.asyncio
    async def test_get_job_details_sends_message_high_score_call_telegram(self, mocked_gemini_client):
        mock_notifier = Mock()
        mock_notifier.send_message = AsyncMock()
        client = mocked_gemini_client(score=80)

        await client.get_job_details("some job", mock_notifier)

        mock_notifier.send_message.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_job_details_sends_message_low_score_not_call_telegram(self, mocked_gemini_client):
        mock_notifier = Mock()
        mock_notifier.send_message = AsyncMock()
        client = mocked_gemini_client(score=0)

        await client.get_job_details("some job", mock_notifier)

        mock_notifier.send_message.assert_not_awaited()

    def test_create_chat(self, mocked_gemini_client):
        client = mocked_gemini_client(score=50)
        client.create_chat()
        client.client.chats.create.assert_called_once()
