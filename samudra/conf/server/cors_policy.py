from typing import List

from samudra.conf.setup import settings

ALLOWED_ORIGINS: List[str] = settings.get('cors_policy.allowed_origins')
