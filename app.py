from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import uuid

# Azure Services
from services.document_service import extract_text_from_document
from services.language_service import summarize_text, simplify_text
from services.translator_service import translate_text
from services.speech_service import text_to_speech, speech_to_text

# Load environment variables
load_dotenv()

app = Flask(__name__)

# -------------------------------
# Configuration
# -------------------------------
UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)


# -------------------------------
# Helper Functions
# -------------------------------
def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Document Upload + OCR
# -------------------------------
@app.route("/upload", methods=["POST"])
def upload_document():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                unique_filename
            )

            file.save(filepath)

            # Azure Document Intelligence OCR
            extracted_text = extract_text_from_document(filepath)

            return jsonify({
                "success": True,
                "filename": unique_filename,
                "extracted_text": extracted_text
            })

        return jsonify({
            "error": "Invalid file format"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# Summarization
# -------------------------------
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()

        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "error": "Text is required"
            }), 400

        summary = summarize_text(text)

        return jsonify({
            "success": True,
            "summary": summary
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# Text Simplification
# -------------------------------
@app.route("/simplify", methods=["POST"])
def simplify():
    try:
        data = request.get_json()

        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "error": "Text is required"
            }), 400

        simplified = simplify_text(text)

        return jsonify({
            "success": True,
            "simplified_text": simplified
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# Translation
# -------------------------------
@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()

        text = data.get("text", "")
        target_language = data.get("language", "hi")

        if not text.strip():
            return jsonify({
                "error": "Text is required"
            }), 400

        translated_text = translate_text(
            text,
            target_language
        )

        return jsonify({
            "success": True,
            "translated_text": translated_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# Text to Speech
# -------------------------------
@app.route("/text-to-speech", methods=["POST"])
def convert_text_to_speech():
    try:
        data = request.get_json()

        text = data.get("text", "")
        language = data.get("language", "en-US")

        if not text.strip():
            return jsonify({
                "error": "Text is required"
            }), 400

        filename = f"{uuid.uuid4()}.wav"

        output_path = os.path.join(
            app.config["AUDIO_FOLDER"],
            filename
        )

        text_to_speech(
            text=text,
            language=language,
            output_path=output_path
        )

        audio_url = f"/audio/{filename}"

        return jsonify({
            "success": True,
            "audio_url": audio_url
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# Speech to Text
# -------------------------------
@app.route("/speech-to-text", methods=["POST"])
def convert_speech_to_text():
    try:
        result = speech_to_text()

        return jsonify({
            "success": True,
            "recognized_text": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# Serve Generated Audio
# -------------------------------
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(
        app.config["AUDIO_FOLDER"],
        filename
    )


# -------------------------------
# Run Flask App
# -------------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
