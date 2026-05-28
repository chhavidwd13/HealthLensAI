import streamlit as st

from modules.symptom_analyzer import analyze_symptoms
from modules.safety_checker import check_emergency
from modules.pdf_processor import extract_text_from_pdf, summarize_report
from modules.rag_engine import create_vector_db, rag_answer
from modules.image_predictor import analyze_skin_image
from modules.memory_chatbot import get_memory_response
from modules.auth import create_users_table, signup_user, login_user


create_users_table()

st.set_page_config(
    page_title="HealthLens AI",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CUSTOM UI CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef7ff 0%, #f8fbff 45%, #ecfff7 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #113b5c 55%, #0f766e 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero-card {
    padding: 34px;
    border-radius: 28px;
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
    border: 1px solid rgba(255,255,255,0.7);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 18px;
    color: #475569;
    line-height: 1.6;
}

.glass-card {
    padding: 24px;
    border-radius: 24px;
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(14px);
    box-shadow: 0 16px 35px rgba(15, 23, 42, 0.10);
    border: 1px solid rgba(255,255,255,0.75);
    min-height: 160px;
    transition: 0.2s ease-in-out;
}

.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 22px 42px rgba(15, 23, 42, 0.14);
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
}

.card-text {
    color: #64748b;
    font-size: 15px;
    line-height: 1.5;
}

.section-card {
    padding: 28px;
    border-radius: 26px;
    background: rgba(255,255,255,0.82);
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.10);
    border: 1px solid rgba(255,255,255,0.75);
    margin-top: 18px;
}

.status-pill {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    font-weight: 700;
    font-size: 14px;
    margin-right: 8px;
}

.warning-box {
    padding: 16px 20px;
    border-radius: 18px;
    background: #fff7ed;
    color: #9a3412;
    border: 1px solid #fed7aa;
    margin-bottom: 20px;
}

.login-card {
    max-width: 480px;
    margin: 40px auto;
    padding: 34px;
    border-radius: 28px;
    background: rgba(255,255,255,0.85);
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.14);
    border: 1px solid rgba(255,255,255,0.8);
}

.small-muted {
    color: #64748b;
    font-size: 14px;
}

.result-box {
    padding: 22px;
    border-radius: 22px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "report_history" not in st.session_state:
    st.session_state.report_history = []


# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-card">
        <h1 style="color:#0f172a; text-align:center;">🩺 HealthLens AI</h1>
        <p style="color:#64748b; text-align:center;">
        Secure access to your AI-powered healthcare assistant.
        </p>
    </div>
    """, unsafe_allow_html=True)

    auth_option = st.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if auth_option == "Signup":

        if st.button("Create Account", use_container_width=True):

            if username.strip() == "" or password.strip() == "":
                st.error("Please enter username and password.")

            elif signup_user(username, password):
                st.success("Account created successfully. Now login.")

            else:
                st.error("Username already exists.")

    else:

        if st.button("Login", use_container_width=True):

            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful.")
                st.rerun()

            else:
                st.error("Invalid username or password.")

    st.stop()


# ---------------- SIDEBAR ----------------
st.sidebar.title("🩺 HealthLens AI")
st.sidebar.caption("Multimodal GenAI Healthcare Platform")

st.sidebar.markdown("---")
st.sidebar.success(f"👤 {st.session_state.username}")

st.sidebar.markdown("### System Status")
st.sidebar.info("✅ Gemini / Fallback Ready")
st.sidebar.info("✅ RAG Enabled")
st.sidebar.info("✅ Chat Memory Active")
st.sidebar.info("✅ Report Downloads")

st.sidebar.markdown("---")

option = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Symptom Analyzer",
        "PDF Report Summarizer",
        "Medical Chatbot",
        "RAG Medical Assistant",
        "Skin Image Analyzer",
        "History"
    ]
)

st.sidebar.markdown("---")

if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()


# ---------------- HERO HEADER ----------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">HealthLens AI</div>
    <div class="hero-subtitle">
        A modern multimodal healthcare assistant powered by Generative AI, RAG,
        PDF intelligence, chatbot memory, and skin image understanding.
    </div>
    <br>
    <span class="status-pill">GenAI</span>
    <span class="status-pill">RAG</span>
    <span class="status-pill">Multimodal</span>
    <span class="status-pill">Healthcare AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="warning-box">
    ⚠️ This tool is for educational and informational use only. 
    It is not a replacement for professional medical advice, diagnosis, or treatment.
</div>
""", unsafe_allow_html=True)


# ---------------- HOME ----------------
if option == "Home":

    st.markdown("## Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("AI Modules", "5")

    with col2:
        st.metric("Input Types", "4")

    with col3:
        st.metric("Safety Layer", "Active")

    with col4:
        st.metric("RAG Support", "Enabled")

    st.markdown("## Core Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🤒 Symptom Analyzer</div>
            <p class="card-text">
            Enter symptoms and receive a structured AI-based health explanation.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">📄 PDF Summarizer</div>
            <p class="card-text">
            Upload medical reports and understand complex values in simple language.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">💬 Medical Chatbot</div>
            <p class="card-text">
            Ask healthcare questions with conversation memory support.
            </p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">📚 RAG Assistant</div>
            <p class="card-text">
            Answers questions using trusted medical documents stored in the project.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🖼️ Skin Image Analyzer</div>
            <p class="card-text">
            Analyze skin images using multimodal AI with safe educational guidance.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## System Workflow")

    st.code("""
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
""")


# ---------------- SYMPTOM ANALYZER ----------------
elif option == "Symptom Analyzer":

    st.markdown("## 🤒 Symptom Analyzer")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    symptoms = st.text_area(
        "Describe your symptoms",
        placeholder="Example: I have fever, headache and body pain since yesterday...",
        height=160
    )

    if st.button("Analyze Symptoms", use_container_width=True):

        if symptoms.strip() == "":
            st.error("Please enter symptoms first.")

        elif check_emergency(symptoms):
            st.error("Emergency warning: Please seek medical help immediately.")
            st.session_state.report_history.append(
                "Emergency symptom warning triggered"
            )

        else:
            with st.spinner("Analyzing symptoms..."):
                result = analyze_symptoms(symptoms)

            st.subheader("AI Health Explanation")
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

            st.session_state.report_history.append(
                "Generated symptom analysis report"
            )

            report_content = f"""
HealthLens AI - Symptom Analysis Report

User Symptoms:
{symptoms}

AI Health Explanation:
{result}

Disclaimer:
This report is AI-generated for educational purposes only.
It is not a replacement for professional medical advice.
"""

            st.download_button(
                "Download Symptom Report",
                report_content,
                "symptom_report.txt",
                "text/plain",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- PDF REPORT SUMMARIZER ----------------
elif option == "PDF Report Summarizer":

    st.markdown("## 📄 PDF Report Summarizer")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload medical report PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        st.success("PDF uploaded successfully.")

        if st.button("Summarize Report", use_container_width=True):

            with st.spinner("Extracting and summarizing report..."):
                report_text = extract_text_from_pdf(uploaded_file)

            if report_text.strip() == "":
                st.error("Could not extract text from this PDF.")
            else:
                summary = summarize_report(report_text)

                st.subheader("Report Summary")
                st.markdown(f'<div class="result-box">{summary}</div>', unsafe_allow_html=True)

                st.session_state.report_history.append(
                    "Generated PDF medical report summary"
                )

                report_content = f"""
HealthLens AI - Medical Report Summary

AI Summary:
{summary}

Disclaimer:
This summary is AI-generated for educational purposes only.
It is not a replacement for professional medical advice.
"""

                st.download_button(
                    "Download Medical Summary",
                    report_content,
                    "medical_report_summary.txt",
                    "text/plain",
                    use_container_width=True
                )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- MEDICAL CHATBOT ----------------
elif option == "Medical Chatbot":

    st.markdown("## 💬 Medical Chatbot")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

    user_question = st.chat_input("Ask a health-related question...")

    if user_question:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_question}
        )

        with st.spinner("Thinking..."):
            answer = get_memory_response(
                user_question,
                st.session_state.chat_history
            )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

        st.session_state.report_history.append(
            "Used medical chatbot"
        )

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- RAG ASSISTANT ----------------
elif option == "RAG Medical Assistant":

    st.markdown("## 📚 RAG Medical Assistant")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.write("This module answers using your trusted medical knowledge base.")

    if st.button("Build / Refresh Knowledge Base", use_container_width=True):
        with st.spinner("Creating medical knowledge base..."):
            message = create_vector_db()

        st.success(message)

    question = st.text_input(
        "Ask a question from medical knowledge base",
        placeholder="Example: What are warning signs of dengue?"
    )

    if st.button("Ask RAG Assistant", use_container_width=True):

        if question.strip() == "":
            st.error("Please enter a question.")

        else:
            with st.spinner("Searching knowledge base..."):
                answer = rag_answer(question)

            st.subheader("RAG-Based Answer")
            st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)

            st.session_state.report_history.append(
                "Asked question using RAG medical assistant"
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- SKIN IMAGE ANALYZER ----------------
elif option == "Skin Image Analyzer":

    st.markdown("## 🖼️ Skin Image Analyzer")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload skin image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Uploaded Skin Image",
            use_container_width=True
        )

        if st.button("Analyze Skin Image", use_container_width=True):

            with st.spinner("Analyzing image..."):
                result = analyze_skin_image(uploaded_image)

            st.subheader("AI Skin Analysis")
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

            st.session_state.report_history.append(
                "Generated skin image analysis report"
            )

            report_content = f"""
HealthLens AI - Skin Image Analysis Report

AI Skin Analysis:
{result}

Disclaimer:
This report is AI-generated for educational purposes only.
It is not a replacement for dermatologist consultation.
"""

            st.download_button(
                "Download Skin Analysis Report",
                report_content,
                "skin_analysis_report.txt",
                "text/plain",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- HISTORY ----------------
elif option == "History":

    st.markdown("## User Activity History")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if not st.session_state.report_history:
        st.info("No activity yet.")
    else:
        for index, item in enumerate(st.session_state.report_history, start=1):
            st.write(f"{index}. {item}")

    if st.button("Clear History", use_container_width=True):
        st.session_state.report_history = []
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)