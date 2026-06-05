import secrets


def generate_otp(digits: int = 4) -> str:
    return str(secrets.randbelow(10**digits)).zfill(digits)


def otp_key(phone_number: str) -> str: 
    return f"sms:otp:{phone_number}"

def lock_key(phone_number: str) -> str: 
    return f"sms:lock:{phone_number}"

def resend_key(phone_number: str) -> str: 
    return f"sms:resend:{phone_number}"
