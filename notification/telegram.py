import telegram
from jinja2 import Template
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class Notifier:
    TEMPLATE_PATH = "templates/job_info.md"

    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        self.template = self._load_template()

    def _load_template(self) -> Template:
        """Load and return the Jinja2 template."""
        try:
            with open(self.TEMPLATE_PATH, "r") as file:
                return Template(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found at {self.TEMPLATE_PATH}")
        except Exception as e:
            raise RuntimeError(f"Error loading template: {e}")

    def send_message(self, params: dict) -> telegram.Message:
        """Render the message and send it via Telegram."""
        try:
            message = self.template.render(**params)
            return self.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown"
            )
        except Exception as e:
            raise RuntimeError(f"Error sending message: {e}")