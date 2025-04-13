import argparse

from ai_client.gemini_client import GeminiClient
from config.config import GOOGLE_API_KEY
from notification.telegram import Notifier
from scraper.scrape import search_jobs


def get_llm_client(model_name: str):
    """Return the appropriate LLM client based on the model name."""
    if model_name.lower() == "gemini":
        return GeminiClient(GOOGLE_API_KEY)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Job Matching System")
    parser.add_argument(
        "--model",
        type=str,
        default="gemini",
        help="Specify the LLM model to use (e.g., 'gemini')",
    )
    args = parser.parse_args()

    notifier = Notifier()
    llm_client = get_llm_client(args.model)
    search_jobs(llm_client, notifier)
