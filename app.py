import streamlit as st

from modules.symptom_analyzer import analyze_symptoms
from modules.safety_checker import check_emergency
from modules.pdf_processor import extract_text_from_pdf, summarize_report
from modules.rag_engine import create_vector_db, rag_answer
from modules.image_predictor import analyze_skin_image
from modules.memory_chatbot import get_memory_response
from modules.auth import create_users_table, signup_user, login_user
from modules.report_generator import create_pdf_report
from modules.analytics import get_dashboard_stats
from modules.health_dashboard import get_health_dashboard_data
from modules.history_db import create_history_table, save_activity, get_user_history


create_users_table()
create_history_table()

st.set_page_config(
    page_title="HealthLens AI",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f3ff 0%, #eef2ff 45%, #ecfeff 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #312e81 50%, #4c1d95 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero-card {
    padding: 36px;
    border-radius: 30px;
    background: rgba(255, 255, 255, 0.82);
    box-shadow: 0 22px 50px rgba(79, 70, 229, 0.16);
    border: 1px solid rgba(255,255,255,0.85);
    margin-bottom: 28px;
}

.hero-title {
    font-size: 46px;
    font-weight: 850;
    background: linear-gradient(90deg, #4f46e5, #7c3aed, #0891b2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 18px;
    color: #475569;
    line-height: 1.7;
}

.glass-card, .section-card {
    padding: 28px;
    border-radius: 28px;
    background: rgba(255,255,255,0.88);
    box-shadow: 0 18px 45px rgba(79, 70, 229, 0.12);
    border: 1px solid rgba(255,255,255,0.85);
    margin-top: 18px;
    margin-bottom: 24px;
}

.result-box {
    padding: 24px;
    border-radius: 24px;
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    border: 1px solid #ddd6fe;
    color: #111827;
    white-space: pre-wrap;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.6);
}

.card-title {
    font-size: 22px;
    font-weight: 750;
    color: #1e1b4b;
}

.card-text {
    color: #64748b;
    font-size: 15px;
    line-height: 1.6;
}

.status-pill {
    display: inline-block;
    padding: 9px 15px;
    border-radius: 999px;
    background: linear-gradient(135deg, #ede9fe, #dbeafe);
    color: #3730a3;
    font-weight: 750;
    font-size: 14px;
    margin-right: 8px;
    border: 1px solid #c4b5fd;
}

.warning-box {
    padding: 16px 20px;
    border-radius: 20px;
    background: #fff7ed;
    color: #9a3412;
    border: 1px solid #fed7aa;
    margin-bottom: 22px;
}

.login-card {
    max-width: 540px;
    margin: 42px auto 22px auto;
    padding: 36px;
    border-radius: 30px;
    background: rgba(255,255,255,0.9);
    box-shadow: 0 24px 55px rgba(79, 70, 229, 0.16);
    text-align: center;
    border: 1px solid rgba(255,255,255,0.85);
}

.module-badge {
    padding: 16px;
    border-radius: 20px;
    background: linear-gradient(135deg, #ffffff, #eef2ff);
    border: 1px solid #ddd6fe;
    text-align: center;
    font-weight: 750;
    color: #312e81;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


def module_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="section-card">
        <h2>{icon} {title}</h2>
        <p class="card-text">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def show_result(title, content):
    st.subheader(title)
    st.markdown(f'<div class="result-box">{content}</div>', unsafe_allow_html=True)


def log_activity(activity):
    st.session_state.report_history.append(activity)
    save_activity(st.session_state.username, activity)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "report_history" not in st.session_state:
    st.session_state.report_history = []


if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-card">
        <h1 style="color:#0f172a;">🩺 HealthLens AI</h1>
        <p style="color:#64748b;">
        Secure access to your AI-powered multimodal healthcare assistant.
        </p>
    </div>
    """, unsafe_allow_html=True)

    auth_option = st.selectbox("Choose Option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

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

                saved_history = get_user_history(username)
                st.session_state.report_history = list(
                    reversed([item[0] for item in saved_history])
                )

                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.stop()


st.sidebar.title("🩺 HealthLens AI")
st.sidebar.caption("Multimodal GenAI Healthcare Platform")

st.sidebar.markdown("---")
st.sidebar.success(f"👤 {st.session_state.username}")

st.sidebar.markdown("### System Status")
st.sidebar.info("✅ Gemini / Fallback Ready")
st.sidebar.info("✅ RAG Enabled")
st.sidebar.info("✅ Chat Memory Active")
st.sidebar.info("✅ PDF Reports")
st.sidebar.info("✅ Persistent History")

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
        "Health Dashboard",
        "History"
    ]
)

st.sidebar.markdown("---")

if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.chat_history = []
    st.rerun()


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


if option == "Home":

    st.markdown("## Dashboard Overview")

    stats = get_dashboard_stats(st.session_state.report_history)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Reports Generated", stats["reports"])

    with col2:
        st.metric("Chat Queries", stats["chatbot"])

    with col3:
        st.metric("RAG Queries", stats["rag"])

    with col4:
        st.metric("Image Analyses", stats["image"])

    st.markdown("## Core Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🤒 Symptom Analyzer</div>
            <p class="card-text">Analyze symptoms and receive structured healthcare guidance.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">📄 PDF Report Summarizer</div>
            <p class="card-text">Upload medical reports and understand them in simple language.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">💬 Medical Chatbot</div>
            <p class="card-text">Ask healthcare questions with memory-enabled chat support.</p>
        </div>
        """, unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">📚 RAG Medical Assistant</div>
            <p class="card-text">Get answers using trusted medical documents.</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🖼️ Skin Image Analyzer</div>
            <p class="card-text">Upload skin images for safe educational observations.</p>
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
Downloadable PDF Report
""")


elif option == "Symptom Analyzer":

    module_header(
        "🤒",
        "Symptom Analyzer",
        "Describe symptoms and receive structured AI-powered guidance with precautions, red flags, and doctor consultation advice."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-badge">✅ Simple Explanation</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-badge">🩺 Precautions</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="module-badge">📌 Doctor Questions</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    symptoms = st.text_area(
        "Describe your symptoms",
        placeholder="Example: I have fever, headache and body pain since yesterday...",
        height=170
    )

    if st.button("Analyze Symptoms", use_container_width=True):

        if symptoms.strip() == "":
            st.error("Please enter symptoms first.")

        elif check_emergency(symptoms):
            st.error("Emergency warning: Please seek medical help immediately.")
            log_activity("Emergency symptom warning triggered")

        else:
            with st.spinner("Analyzing symptoms..."):
                result = analyze_symptoms(symptoms)

            show_result("AI Health Explanation", result)
            log_activity("Generated symptom analysis report")

            pdf_data = create_pdf_report(
                st.session_state.username,
                "Symptom Analysis Report",
                f"User Symptoms:\n{symptoms}\n\nAI Health Explanation:\n{result}"
            )

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name="symptom_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


elif option == "PDF Report Summarizer":

    module_header(
        "📄",
        "PDF Medical Report Summarizer",
        "Upload medical reports and understand key values, findings, and doctor discussion points in simple language."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-badge">📌 Key Findings</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-badge">📊 Important Values</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="module-badge">🩺 Doctor Points</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload medical report PDF", type=["pdf"])

    if uploaded_file is not None:
        st.success("PDF uploaded successfully.")

        if st.button("Summarize Report", use_container_width=True):

            with st.spinner("Extracting and summarizing report..."):
                report_text = extract_text_from_pdf(uploaded_file)

            if report_text.strip() == "":
                st.error("Could not extract text from this PDF.")

            else:
                summary = summarize_report(report_text)

                show_result("Report Summary", summary)
                log_activity("Generated PDF medical report summary")

                pdf_data = create_pdf_report(
                    st.session_state.username,
                    "Medical Report Summary",
                    summary
                )

                st.download_button(
                    label="📄 Download PDF Summary",
                    data=pdf_data,
                    file_name="medical_summary.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    st.markdown('</div>', unsafe_allow_html=True)


elif option == "Medical Chatbot":

    module_header(
        "💬",
        "Medical Chatbot",
        "Chat with a healthcare assistant that remembers your conversation during the session and responds safely."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="module-badge">🧠 Memory Enabled</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-badge">🛡️ Safe Guidance</div>', unsafe_allow_html=True)

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
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        with st.spinner("Thinking..."):
            answer = get_memory_response(user_question, st.session_state.chat_history)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        log_activity("Used medical chatbot")

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


elif option == "RAG Medical Assistant":

    module_header(
        "📚",
        "RAG Medical Assistant",
        "Ask health questions answered using trusted local medical documents and vector search."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-badge">📁 Local Docs</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-badge">🔍 Vector Search</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="module-badge">📌 Source-backed</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.write("Build the knowledge base first, then ask questions from trusted documents.")

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

            show_result("RAG-Based Answer", answer)
            log_activity("Asked question using RAG medical assistant")

    st.markdown('</div>', unsafe_allow_html=True)


elif option == "Skin Image Analyzer":

    module_header(
        "🖼️",
        "Skin Image Analyzer",
        "Upload a skin image and receive safe educational observations with dermatologist consultation guidance."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="module-badge">🖼️ Image Input</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="module-badge">🔎 Observation</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="module-badge">🩺 Dermatologist Guidance</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    uploaded_image = st.file_uploader("Upload skin image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:

        st.image(uploaded_image, caption="Uploaded Skin Image", use_container_width=True)

        if st.button("Analyze Skin Image", use_container_width=True):

            with st.spinner("Analyzing image..."):
                result = analyze_skin_image(uploaded_image)

            show_result("AI Skin Analysis", result)
            log_activity("Generated skin image analysis report")

            pdf_data = create_pdf_report(
                st.session_state.username,
                "Skin Image Analysis Report",
                result
            )

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name="skin_analysis.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


elif option == "Health Dashboard":

    module_header(
        "📊",
        "Health Dashboard",
        "View a summary of your recent AI healthcare activity."
    )

    dashboard_data = get_health_dashboard_data(st.session_state.report_history)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Activities", dashboard_data["total_activities"])

    with col2:
        st.metric("Symptom Reports", dashboard_data["symptom_reports"])

    with col3:
        st.metric("PDF Summaries", dashboard_data["pdf_reports"])

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Chatbot Queries", dashboard_data["chatbot_queries"])

    with col5:
        st.metric("RAG Queries", dashboard_data["rag_queries"])

    with col6:
        st.metric("Skin Reports", dashboard_data["skin_reports"])

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.subheader("Recent Activity")

    if not st.session_state.report_history:
        st.info("No activity yet.")
    else:
        for index, item in enumerate(st.session_state.report_history[-5:], start=1):
            st.write(f"{index}. {item}")

    st.markdown('</div>', unsafe_allow_html=True)


elif option == "History":

    module_header(
        "📜",
        "User Activity History",
        "Your activity is saved using SQLite and remains available after login."
    )

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if not st.session_state.report_history:
        st.info("No activity yet.")
    else:
        for index, item in enumerate(st.session_state.report_history, start=1):
            st.write(f"{index}. {item}")

    st.info("Persistent history is enabled. Activities remain saved after logout and restart.")

    st.markdown('</div>', unsafe_allow_html=True)