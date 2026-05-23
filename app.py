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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "report_history" not in st.session_state:
    st.session_state.report_history = []


if not st.session_state.logged_in:

    st.title("🔐 HealthLens AI Login")

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


st.title("🩺 HealthLens AI")
st.subheader("Multimodal Healthcare Assistant")

st.warning(
    "This tool is for educational use only. "
    "It is not a replacement for professional medical advice."
)

st.sidebar.title("🩺 HealthLens AI")
st.sidebar.caption("Multimodal Healthcare Assistant")
st.sidebar.success(f"Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

option = st.sidebar.radio(
    "Choose Module",
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


if option == "Home":

    st.header("Welcome to HealthLens AI")

    st.write("""
    HealthLens AI is a multimodal healthcare assistant that combines
    Generative AI, RAG, PDF processing, chatbot memory, and image understanding.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("AI Modules", "5")

    with col2:
        st.metric("Input Types", "4")

    with col3:
        st.metric("Safety Layer", "Active")

    with col4:
        st.metric("RAG Support", "Enabled")

    st.subheader("Available Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🤒 Symptom Analyzer\n\nAnalyze symptoms using Gemini AI.")

    with col2:
        st.info("📄 PDF Summarizer\n\nUpload medical reports and get simple explanation.")

    with col3:
        st.info("💬 Medical Chatbot\n\nChat with healthcare AI with memory.")

    col4, col5 = st.columns(2)

    with col4:
        st.info("📚 RAG Assistant\n\nAnswers using trusted medical documents.")

    with col5:
        st.info("🖼️ Skin Image Analyzer\n\nAnalyze skin images using multimodal AI.")

    st.subheader("System Workflow")

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


elif option == "Symptom Analyzer":

    st.header("🤒 Symptom Analyzer")

    symptoms = st.text_area(
        "Describe your symptoms:",
        placeholder="Example: I have fever, headache and body pain since yesterday..."
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
            st.write(result)

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


elif option == "PDF Report Summarizer":

    st.header("📄 PDF Report Summarizer")

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
                st.write(summary)

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


elif option == "Medical Chatbot":

    st.header("💬 Medical Chatbot")

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


elif option == "RAG Medical Assistant":

    st.header("📚 RAG Medical Assistant")

    st.write("This module answers using your trusted medical knowledge base.")

    if st.button("Build / Refresh Knowledge Base", use_container_width=True):
        with st.spinner("Creating medical knowledge base..."):
            message = create_vector_db()

        st.success(message)

    question = st.text_input(
        "Ask a question from medical knowledge base:",
        placeholder="Example: What are warning signs of dengue?"
    )

    if st.button("Ask RAG Assistant", use_container_width=True):

        if question.strip() == "":
            st.error("Please enter a question.")

        else:
            with st.spinner("Searching knowledge base..."):
                answer = rag_answer(question)

            st.subheader("RAG-Based Answer")
            st.write(answer)

            st.session_state.report_history.append(
                "Asked question using RAG medical assistant"
            )


elif option == "Skin Image Analyzer":

    st.header("🖼️ Skin Image Analyzer")

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
            st.write(result)

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


elif option == "History":

    st.header("User Activity History")

    if not st.session_state.report_history:
        st.info("No activity yet.")
    else:
        for index, item in enumerate(st.session_state.report_history, start=1):
            st.write(f"{index}. {item}")

    if st.button("Clear History", use_container_width=True):
        st.session_state.report_history = []
        st.rerun()