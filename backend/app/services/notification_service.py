"""
Notification service — sends alert notifications via email (SMTP).
"""

import logging
import smtplib
from email.mime.text import MIMEText
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    """Send notifications via configured channels."""

    @staticmethod
    def _smtp_enabled() -> bool:
        return bool(settings.SMTP_HOST and settings.SMTP_PORT)

    @staticmethod
    def send_email(
        to: str,
        subject: str,
        body: str,
        body_html: Optional[str] = None,
    ) -> bool:
        """Send an email via SMTP. Returns True on success."""
        if not NotificationService._smtp_enabled():
            logger.warning("SMTP not configured, skipping email to %s", to)
            return False

        try:
            msg = MIMEText(body_html or body, "html" if body_html else "plain", "utf-8")
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_FROM
            msg["To"] = to

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                if settings.SMTP_USER:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM, [to], msg.as_string())

            logger.info("Email sent to %s: %s", to, subject)
            return True
        except Exception:
            logger.exception("Failed to send email to %s", to)
            return False

    @staticmethod
    def send_alert_email(
        alert_title: str,
        alert_message: str,
        severity: str,
        recipient: str = "",
    ) -> bool:
        """Send an alert notification email."""
        to = recipient or settings.SMTP_RECIPIENT or settings.SMTP_FROM
        if not to:
            logger.warning("No SMTP recipient configured, skipping alert email")
            return False

        severity_label = {"critical": "🔴 紧急", "warning": "🟡 警告", "info": "🔵 通知"}.get(severity, severity)

        subject = f"[BridgeWatch AI] {severity_label}: {alert_title}"
        body = f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a1a2e; padding: 20px; border-radius: 12px 12px 0 0;">
                <h2 style="color: #d3914d; margin: 0;">BridgeWatch AI 告警通知</h2>
            </div>
            <div style="background: #16213e; padding: 20px; border-radius: 0 0 12px 12px;">
                <p style="color: #e8edf3; font-size: 16px;"><strong>{alert_title}</strong></p>
                <p style="color: #a0b4c8;">{alert_message}</p>
                <p style="color: #6c8a9e; font-size: 12px; margin-top: 20px;">
                    此为系统自动发送，请勿回复。<br>
                    BridgeWatch AI — 基础设施智能监测面板
                </p>
            </div>
        </div>
        """

        return NotificationService.send_email(to=to, subject=subject, body_html=body)
