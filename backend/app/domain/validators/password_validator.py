from app.core.exceptions.domain_exception import ValidationException

def validate_password(password: str) -> None:
    errors = []

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    if errors:
        raise ValidationException(", ".join(errors))