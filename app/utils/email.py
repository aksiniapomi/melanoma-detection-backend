import os, ssl
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings

logger = logging.getLogger("email")
logger.setLevel(logging.INFO)

ssl._create_default_https_context = ssl._create_unverified_context

def send_email(to: str, subject: str, body: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    sender    = os.getenv("EMAIL_FROM_ADDRESS", smtp_user)

    # fallback to stub if creds missing
    if not smtp_host or not smtp_user or not smtp_pass:
        logger.info(f"[EMAIL STUB] To: {to}\nSubject: {subject}\n\n{body}\n")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = to
    msg.set_content(body, subtype="html")

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        logger.info(f"[SMTP] Email sent to {to}")
    except Exception as e:
        logger.error(f"Error sending via SMTP: {e}")
        raise