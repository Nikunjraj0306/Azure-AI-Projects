// -------------------------------------
// DOM Elements
// -------------------------------------
const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const dropArea = document.getElementById("dropArea");

const extractBtn = document.getElementById("extractBtn");
const summaryBtn = document.getElementById("summaryBtn");
const simplifyBtn = document.getElementById("simplifyBtn");
const translateBtn = document.getElementById("translateBtn");
const speechBtn = document.getElementById("speechBtn");
const ttsBtn = document.getElementById("ttsBtn");

const extractedText = document.getElementById("extractedText");
const resultBox = document.getElementById("resultBox");
const languageSelect = document.getElementById("languageSelect");
const audioPlayer = document.getElementById("audioPlayer");

let selectedFile = null;


// -------------------------------------
// File Upload Handling
// -------------------------------------
browseBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (event) => {
    selectedFile = event.target.files[0];

    if (selectedFile) {
        dropArea.innerHTML = `
            <p>✅ ${selectedFile.name}</p>
            <span>Ready to extract</span>
        `;
    }
});


// -------------------------------------
// Drag & Drop
// -------------------------------------
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.borderColor = "#3b82f6";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.borderColor =
        "rgba(255,255,255,0.2)";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();

    selectedFile = e.dataTransfer.files[0];

    if (selectedFile) {
        dropArea.innerHTML = `
            <p>✅ ${selectedFile.name}</p>
            <span>Ready to extract</span>
        `;
    }
});


// -------------------------------------
// Extract OCR Text
// -------------------------------------
extractBtn.addEventListener("click", async () => {

    if (!selectedFile) {
        alert("Please upload a file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    extractBtn.innerText = "Extracting...";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            extractedText.value =
                data.extracted_text;
        } else {
            alert(data.error);
        }

    } catch (error) {
        alert("Extraction failed.");
        console.error(error);
    }

    extractBtn.innerText = "Extract Text";
});


// -------------------------------------
// Summarize Text
// -------------------------------------
summaryBtn.addEventListener("click", async () => {

    const text = extractedText.value.trim();

    if (!text) {
        alert("No text found.");
        return;
    }

    summaryBtn.innerText = "Summarizing...";

    try {

        const response = await fetch(
            "/summarize",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            }
        );

        const data = await response.json();

        if (data.success) {
            resultBox.value =
                data.summary;
        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
        alert("Summarization failed.");
    }

    summaryBtn.innerText = "Summarize";
});


// -------------------------------------
// Simplify Text
// -------------------------------------
simplifyBtn.addEventListener("click", async () => {

    const text = extractedText.value.trim();

    if (!text) {
        alert("No text found.");
        return;
    }

    simplifyBtn.innerText = "Simplifying...";

    try {

        const response = await fetch(
            "/simplify",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            }
        );

        const data = await response.json();

        if (data.success) {
            resultBox.value =
                data.simplified_text;
        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
        alert("Simplification failed.");
    }

    simplifyBtn.innerText = "Simplify";
});


// -------------------------------------
// Translate Text
// -------------------------------------
translateBtn.addEventListener(
    "click",
    async () => {

    const text = extractedText.value.trim();

    if (!text) {
        alert("No text found.");
        return;
    }

    const selectedLanguage =
        languageSelect.value;

    translateBtn.innerText =
        "Translating...";

    try {

        const response = await fetch(
            "/translate",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    language:
                    selectedLanguage
                })
            }
        );

        const data = await response.json();

        if (data.success) {
            resultBox.value =
                data.translated_text;
        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
        alert("Translation failed.");
    }

    translateBtn.innerText =
        "Translate";
});


// -------------------------------------
// Speech to Text
// -------------------------------------
speechBtn.addEventListener(
    "click",
    async () => {

    speechBtn.innerText =
        "Listening...";

    try {

        const response = await fetch(
            "/speech-to-text",
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (data.success) {

            extractedText.value =
                data.recognized_text;

        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
        alert("Speech failed.");
    }

    speechBtn.innerText =
        "🎤 Speech to Text";
});


// -------------------------------------
// Text to Speech
// -------------------------------------
ttsBtn.addEventListener(
    "click",
    async () => {

    const text =
        resultBox.value.trim() ||
        extractedText.value.trim();

    if (!text) {
        alert("No text available.");
        return;
    }

    ttsBtn.innerText =
        "Generating Audio...";

    const language =
        languageSelect.value;

    // Map translation code → speech code
    const speechLanguageMap = {
        en: "en-US",
        hi: "hi-IN",
        fr: "fr-FR",
        de: "de-DE",
        es: "es-ES",
        ja: "ja-JP",
        ko: "ko-KR",
        "zh-Hans": "zh-CN"
    };

    try {

        const response = await fetch(
            "/text-to-speech",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    language:
                    speechLanguageMap[
                        language
                    ]
                })
            }
        );

        const data =
            await response.json();

        if (data.success) {

            audioPlayer.style.display =
                "block";

            audioPlayer.src =
                data.audio_url;

            audioPlayer.play();

        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
        alert("Audio generation failed.");
    }

    ttsBtn.innerText =
        "🔊 Text to Speech";
});
