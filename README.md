# HealthLens AI

HealthLens AI is a multimodal healthcare assistant built using Generative AI.  
It helps users understand symptoms, medical reports, health questions, and skin images in simple language.

## Features

- Symptom Analyzer
- PDF Medical Report Summarizer
- Medical Chatbot with Memory
- RAG-based Medical Assistant
- Skin Image Analyzer
- Emergency Symptom Detection
- Downloadable AI Reports

## Tech Stack

- Python
- Streamlit
- Gemini AI
- FAISS
- LangChain
- PyMuPDF
- Pillow
- Sentence Transformers

## Project Architecture

```text
User Input
   ↓
Text / PDF / Image Processing
   ↓
Safety Check
   ↓
Gemini AI + RAG Engine
   ↓
Structured Healthcare Response
   ↓
Downloadable Report