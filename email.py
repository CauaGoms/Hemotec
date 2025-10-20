from mailersend import MailerSendClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Client automatically uses the loaded MAILERSEND_API_KEY
ms = MailerSendClient()