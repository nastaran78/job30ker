# Job30Ker

# Job Matching System

This project is a **Job Matching System** designed to recommend internship and job opportunities for described profile. The system leverages **LinkedIn job scraping**, **LLM-based job analysis** (e.g., Google Gemini), and **Telegram notifications** to provide tailored job recommendations.

## Features

- **LinkedIn Job Scraper**: Scrapes job postings from LinkedIn using Selenium.
- **LLM Integration**: Supports multiple AI clients (e.g., Google Gemini, OpenAI) for analyzing job descriptions and matching them to the candidate's profile.
- **Telegram Notifications**: Sends job recommendations directly to a Telegram chat.
- **Dynamic Client Support**: Easily extendable to support additional AI clients.
- **Customizable Matching Criteria**: Define specific criteria for job matching based on location, skills, and job type.

## Project Structure

```
.
├── ai_client/
│   ├── base.py               # Base class for AI clients
│   ├── gemini_client.py      # Google Gemini client implementation
│   ├── openai_client.py      # OpenAI client implementation
├── config/
│   ├── config.py             # Configuration for environment variables
├── notification/
│   ├── telegram.py           # Telegram notification system
├── prompt/
│   ├── prompts.py            # Prompt generation for LLMs
├── scraper/
│   ├── scrape.py             # LinkedIn job scraper
├── templates/
│   ├── job_info.md           # Template for Telegram messages
├── main.py                   # Entry point for the application
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)
- LinkedIn account credentials
- Telegram bot token and chat ID
- Google Gemini API key (or OpenAI API key if using OpenAI)

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   LINKEDIN_USERNAME=your_email
   LINKEDIN_PASSWORD=your_password
   TELEGRAM_ACCESS_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

3. Download and set up ChromeDriver:
   - [Download ChromeDriver](https://sites.google.com/chromium.org/driver/) compatible with your Chrome version.
   - Add the ChromeDriver executable to your system's PATH.

## Usage

1. Run the application:
   ```bash
   python -m main
   ```

2. The system will:
   - Log in to LinkedIn and scrape job postings (headless request through selenium).
   - Analyze job descriptions using the configured AI client.
   - Send job recommendations to your Telegram chat.

### Adding New AI Clients

To add support for a new AI client:
1. Create a new class in the `ai_client/` directory that inherits from `BaseClient`.
2. Implement the `get_job_details` method with the logic for the new client.
3. Update the `get_llm_client` in `main.py` to include the new client.

### Customizing Prompts

Modify the `prompts.py` file in the `prompt/` directory to customize the instructions, criteria, and output format for job matching.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [Google Gemini](https://ai.google.dev/gemini-api/docs)
- [OpenAI](https://platform.openai.com/docs/api-reference/introduction)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Selenium](https://www.selenium.dev/)
```