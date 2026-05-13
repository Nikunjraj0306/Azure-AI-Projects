import os
import re
from collections import Counter
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Load env
load_dotenv()

LANGUAGE_ENDPOINT = os.getenv("LANGUAGE_ENDPOINT")
LANGUAGE_KEY = os.getenv("LANGUAGE_KEY")

# Azure client
language_client = TextAnalyticsClient(
    endpoint=LANGUAGE_ENDPOINT,
    credential=AzureKeyCredential(LANGUAGE_KEY)
)


# -----------------------------
# Summarization
# -----------------------------
def summarize_text(text):

    try:
        if not text.strip():
            return "No text found."

        # Split sentences
        sentences = re.split(r'[.!?]+', text)

        # Remove very short sentences
        sentences = [
            s.strip()
            for s in sentences
            if len(s.strip()) > 20
        ]

        if len(sentences) <= 3:
            return text

        # Try Azure key phrases first
        keywords = []

        try:
            response = language_client.extract_key_phrases([text])

            for doc in response:
                if not doc.is_error:
                    keywords.extend(doc.key_phrases)

        except:
            pass

        # Fallback if Azure fails
        if not keywords:

            words = re.findall(
                r'\w+',
                text.lower()
            )

            stopwords = {
                "the", "is", "a", "an",
                "and", "or", "in",
                "on", "of", "to",
                "for", "with"
            }

            words = [
                word
                for word in words
                if word not in stopwords
            ]

            word_freq = Counter(words)

            sentence_scores = {}

            for sentence in sentences:
                score = 0

                for word in sentence.lower().split():
                    score += word_freq.get(word, 0)

                sentence_scores[
                    sentence
                ] = score

        else:
            sentence_scores = {}

            for sentence in sentences:
                score = 0

                for keyword in keywords:
                    if keyword.lower() in sentence.lower():
                        score += 1

                sentence_scores[
                    sentence
                ] = score

        # Top 4 important sentences
        top_sentences = sorted(
            sentence_scores,
            key=sentence_scores.get,
            reverse=True
        )[:4]

        summary = ". ".join(top_sentences)

        return summary + "."

    except Exception as e:
        return (
            f"Summarization error: "
            f"{str(e)}"
        )


# -----------------------------
# Simplification
# -----------------------------
def simplify_text(text):

    try:
        if not text.strip():
            return "No text found."

        response = language_client.extract_key_phrases(
            [text]
        )

        phrases = []

        for doc in response:
            if not doc.is_error:
                phrases.extend(
                    doc.key_phrases
                )

        if not phrases:
            return (
                "Easy Explanation:\n\n"
                + text[:500]
            )

        simplified = (
            "Easy Explanation:\n\n• "
            + "\n• ".join(phrases)
        )

        return simplified

    except Exception as e:
        return (
            f"Simplification error: "
            f"{str(e)}"
        )