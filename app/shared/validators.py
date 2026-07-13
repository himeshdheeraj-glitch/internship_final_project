import re
from typing import Optional

def validate_phone_format(phone: Optional[str]) -> bool:
    if not phone:
        return True
    pattern = r"^\+?[1-9]\d{1,14}$"
    return bool(re.match(pattern, phone))

def validate_zip_format(zip_code: str) -> bool:
    pattern = r"^[a-zA-Z0-9\s\-]{3,10}$"
    return bool(re.match(pattern, zip_code))
