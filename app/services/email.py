import os


def send_verification_code(email: str, code: str) -> None:
    print(f"\n{'='*50}")
    print(f"VERIFICATION CODE FOR: {email}")
    print(f"CODE: {code}")
    print(f"{'='*50}\n")

