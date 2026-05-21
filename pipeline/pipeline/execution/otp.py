import logging
from pipeline.clients.dnse import DNSEClient
from pipeline.config import settings

logger = logging.getLogger(__name__)


async def send_otp(dnse: DNSEClient) -> dict:
    email = settings.dnse_email
    if not email:
        raise RuntimeError("PIPELINE_DNSE_EMAIL not configured")
    result = await dnse.send_email_otp(email)
    logger.info("OTP email sent to %s: %s", email, result)
    return result


async def create_trading_token(dnse: DNSEClient, passcode: str, otp_type: str = "email_otp") -> dict:
    result = await dnse.create_trading_token(otp_type, passcode)
    logger.info("Trading token created (type=%s)", otp_type)
    return result