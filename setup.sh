#!/bin/bash

echo "Installing ScamSenseAI dependencies..."

python -m pip install --upgrade pip
python -m pip install -r requirements_hackathon.txt

echo "Verifying installation..."

python -c "import streamlit; print('streamlit OK')"
python -c "import chromadb; print('chromadb OK')"
python -c "import easyocr; print('easyocr OK')"
python -c "from faster_whisper import WhisperModel; print('whisper OK')"
python -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')"

echo "Setup complete."
