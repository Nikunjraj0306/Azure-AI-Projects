import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Credentials
DOCUMENT_ENDPOINT = os.getenv(
    "DOCUMENT_INTELLIGENCE_ENDPOINT"
)

DOCUMENT_KEY = os.getenv(
    "DOCUMENT_INTELLIGENCE_KEY"
)

# Initialize Azure Document Intelligence Client
document_client = DocumentAnalysisClient(
    endpoint=DOCUMENT_ENDPOINT,
    credential=AzureKeyCredential(DOCUMENT_KEY)
)


def extract_text_from_document(file_path):
    """
    Extract text from PDF, image, or handwritten notes
    using Azure Document Intelligence OCR
    """

    try:
        with open(file_path, "rb") as file:
            poller = document_client.begin_analyze_document(
                model_id="prebuilt-read",
                document=file
            )

            result = poller.result()

        extracted_text = []

        # Read all pages and lines
        for page in result.pages:
            for line in page.lines:
                extracted_text.append(line.content)

        final_text = "\n".join(extracted_text)

        if not final_text.strip():
            return "No text detected in document."

        return final_text

    except Exception as e:
        return f"Document extraction error: {str(e)}"
