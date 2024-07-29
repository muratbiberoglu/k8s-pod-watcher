import re

from src.config.config import config


def format_string(text: str):
    text = text.strip()

    # Regular expression pattern to match content inside parentheses, including the parentheses
    text = re.sub(r'\(.*?\)', '', text)

    # Replace one or more consecutive whitespace characters with a comma
    text = re.sub(r'\s+', ',', text)

    return text


def get_kubectl_context(is_prod_env: bool) -> str:
    return config.get("PROD_CONTEXT") if is_prod_env else config.get("DEV_CONTEXT")
