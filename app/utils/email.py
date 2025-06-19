import os, ssl
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings

logger = logging.getLogger("email")
logger.setLevel(logging.INFO)

ssl._create_default_https_context = ssl._create_unverified_context

def send_email(to: str, subject: str, body: str):

    api_key = settings.SENDGRID_API_KEY
    if not api_key:
        # no key => local stub
        logger.info(f"[EMAIL STUB] To: {to}\nSubject: {subject}\n\n{body}\n")
        return

    # real SendGrid send
    message = Mail(
        from_email=settings.EMAIL_FROM_ADDRESS,
        to_emails=to,
        subject=subject,
        html_content=body,
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        logger.info(f"[SENDGRID] status={response.status_code}")
    except Exception as e:
        logger.error(f"Error sending email via SendGrid: {e}")
        raise