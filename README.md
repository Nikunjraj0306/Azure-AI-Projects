# 🎓 Smart Classroom Assistant

An AI-powered **Smart Classroom Assistant** built using **Python, Flask, HTML, CSS, JavaScript, and Microsoft Azure AI Services**.

This application helps students and educators by extracting text from notes, summarizing content, simplifying difficult concepts, translating into multiple languages, and converting text to speech.

---

## 🚀 Features

### 📄 Document Intelligence (OCR)
- Upload **PDFs, images, and handwritten notes**
- Extract text using **Azure Document Intelligence**
- Supports scanned classroom notes

### 📝 Smart Summarization
- Generate concise summaries from long documents
- Helps students revise quickly

### 📚 Text Simplification
- Converts difficult text into simpler explanations
- Makes learning easier and more accessible

### 🌍 Multi-language Translation
Translate content into multiple languages:

- English
- Hindi
- French
- German
- Spanish
- Japanese
- Korean
- Chinese

Powered by **Azure Translator Service**

### 🎤 Speech-to-Text
- Convert spoken voice into text
- Useful for lectures and classroom interaction

### 🔊 Text-to-Speech
- Convert extracted or translated text into speech
- Supports multiple languages and voice synthesis

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Cloud & AI Services
- Azure Document Intelligence
- Azure Language Service
- Azure Translator
- Azure Speech Service

---

## 📂 Project Structure

```txt
Smart-Classroom-Assistant/
│── app.py
│── requirements.txt
│── .env
│
├── services/
│   ├── document_service.py
│   ├── language_service.py
│   ├── translator_service.py
│   └── speech_service.py
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    ├── script.js
    ├── uploads/
    └── audio/
