from app.core.logging import logger

async def send_email(email_to: str, subject: str, body: str) -> None:
    logger.info("--- MOCK EMAIL DISPATCH ---")
    logger.info(f"To: {email_to}")
    logger.info(f"Subject: {subject}")
    logger.info(f"Body: {body}")
    logger.info(f"---------------------------")

async def send_verification_email(email_to: str, token: str) -> None:
    await send_email(email_to, "Verify your email address", f"Verification token: {token}")

async def send_reset_password_email(email_to: str, token: str) -> None:
    await send_email(email_to, "Reset your password", f"Reset link token: {token}")
