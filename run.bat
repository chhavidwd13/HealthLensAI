@echo off
cd /d D:\HealthLens-AI
call venv\Scripts\activate
python -m streamlit run app.py
pause