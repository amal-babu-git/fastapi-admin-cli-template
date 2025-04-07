import logging
from typing import Dict, Any

from fastapi import BackgroundTasks
from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.core.settings import settings

logger = logging.getLogger(__name__)

# Configure FastMail
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

# Create a global FastMail instance
fastmail = FastMail(conf)

async def send_email_async(
    email_to: EmailStr,
    subject: str,
    html_content: str,
) -> None:
    """Send an email asynchronously."""
    try:
        logger.info(f"Sending email to {email_to} using server {settings.MAIL_SERVER}")
        
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            body=html_content,
            subtype="html",
        )

        await fastmail.send_message(message)
        logger.info(f"Email sent successfully to {email_to}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        logger.exception("Email sending failed with exception:")
        # Don't raise the exception - we want the API to continue working even if email fails

async def send_verification_email(
    email_to: EmailStr,
    token: str,
    background_tasks: BackgroundTasks,
) -> None:
    """Queue a verification email to be sent in the background."""
    verification_url = f"{settings.FRONTEND_URL}/verify?token={token}"
    
    # Create a more appealing HTML template
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
            <h2 style="color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px;">Email Verification</h2>
            <p>Thank you for registering! Please click the link below to verify your email address:</p>
            <p style="text-align: center;">
                <a href="{verification_url}" style="display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a>
            </p>
            <p style="margin-top: 20px; font-size: 0.9em; color: #777;">If the button above doesn't work, copy and paste this URL into your browser:</p>
            <p style="word-break: break-all; font-size: 0.8em; color: #777;">{verification_url}</p>
            <p style="margin-top: 30px; font-size: 0.8em; color: #999;">If you did not request this verification, please ignore this email.</p>
        </body>
    </html>
    """

    # Add the task to the background tasks
    background_tasks.add_task(
        send_email_async,
        email_to=email_to,
        subject="Verify your email address",
        html_content=html_body,
    )
    
    logger.info(f"Verification email queued for {email_to}")
