import logging

logger = logging.getLogger("email_stub")
logger.setLevel(logging.INFO)

def send_email(to: str, subject: str, body: str):
  
    logger.info(f"[EMAIL] To: {to}\nSubject: {subject}\n\n{body}\n")
