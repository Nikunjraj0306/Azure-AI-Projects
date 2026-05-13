import os
import uuid
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Translator Credentials
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION")

# API URL
TRANSLATE_URL = (
    f"{TRANSLATOR_ENDPOINT}/translate?api-version=3.0"
)


def translate_text(text, target_language="hi"):
    """
    Translate text into multiple languages
    Examples:
    hi -> Hindi
    en -> English
    fr -> French
    de -> German
    es -> Spanish
    ja -> Japanese
    zh-Hans -> Chinese
    """

    try:
        headers = {
            "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
            "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4())
        }

        params = {
            "to": target_language
        }

        body = [
            {
                "text": text
            }
        ]

        response = requests.post(
            TRANSLATE_URL,
            params=params,
            headers=headers,
            json=body
        )

        response.raise_for_status()

        result = response.json()

        translated_text = result[0]["translations"][0]["text"]

        return translated_text

    except Exception as e:
        return f"Translation error: {str(e)}"