import re


def to_snake_case(text: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()