import streamlit as st
import time
from PIL import Image
from modules.ocr_engine import extract_text_from_image
from modules.risk_engine import analyze_scam
from modules.speech_engine import transcribe_audio

def display_report(result):

    st.header("🔎 ScamSenseAI Investigation Report")
    st.subheader("🤖 Investigation Agents")
    with st.expander("🤖 Agent Workflow"):

        findings = result.get(
            "agent_findings",
            {}
        )

        for agent, output in findings.items():

            st.success(agent)

            st.write(output)
        

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Case ID: {result['case_id']}")

    with col2:
        st.info(f"Risk Level: {result['risk_level']}")

    st.caption(
        f"Analysis Time: {result['timestamp']}"
    )
    st.metric(
        "Risk Score",
        f"{result['risk_score']}/100"
    )

    if result["risk_score"] > 80:
        st.error("🚨 CONFIRMED SCAM")

    elif result["risk_score"] > 50:
        st.warning("⚠️ LIKELY SCAM")

    else:
        st.success("✅ LOW RISK")

    st.subheader("Scam Type")
    st.info(result["scam_type"])
    st.subheader("Evidence Collected")

    for item in result["evidence"]:
        st.write(f"📚 {item}")

    st.subheader("Red Flags")

    for item in result["red_flags"]:
        st.write(f"⚠️ {item}")

    st.subheader("Recommended Action")

    st.success(
        result["recommendation"]
    )

st.set_page_config(
    page_title="ScamSenseAI",
    page_icon="🛡️"
)

st.title("🛡️ ScamSenseAI")
st.subheader("AI Powered Fraud Detection")
tab1, tab2, tab3 = st.tabs(
    [
        "📝 Text Analysis",
        "🖼️ Image Analysis",
        "🎤 Audio Analysis"
    ]
)

with tab1:
    user_text = st.text_area(
        "Paste suspicious message"
    )

    if st.button("Analyze Scam"):

        if not user_text.strip():
            st.warning("Please enter a message to analyze.")
            st.stop()
        
        with st.spinner("Analyzing..."):

            start = time.time()

            result = analyze_scam(user_text)
            end = time.time()

            st.metric("Inference Time",f"{round(end-start,2)} sec")
            st.caption("Model: Qwen3-4B (Ollama)")
            display_report(result)
with tab2:

    st.header("Image Analysis")

    uploaded_file = st.file_uploader(
        "Upload Scam Screenshot",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:

        st.image(uploaded_file)

        if st.button("🔍 Analyze Screenshot"):

            with st.spinner("Step 1/2: Extracting text from image..."):

                image = Image.open(uploaded_file)

                image.save("temp_image.png")

                extracted_text = extract_text_from_image(
                    "temp_image.png"
                )

            st.success("✅ OCR Completed")

            st.subheader("Extracted Text")

            st.text(extracted_text)

            with st.spinner("Step 2/2: Analyzing for scams..."):

                result = analyze_scam(extracted_text)

            st.success("✅ Scam Analysis Completed")

            display_report(result)

with tab3:

    st.header("Audio Analysis")

    audio_file = st.file_uploader(
        "Upload Audio Recording",
        type=["wav", "mp3", "m4a"]
    )

    if audio_file:

        st.audio(audio_file)

        if st.button("🎤 Analyze Audio"):

            with st.spinner(
                "Step 1/2: Transcribing audio..."
            ):

                with open(
                    "temp_audio.wav",
                    "wb"
                ) as f:
                    f.write(audio_file.read())

                transcript = transcribe_audio(
                    "temp_audio.wav"
                )

            st.success(
                "✅ Transcription Completed"
            )

            st.subheader("Transcript")

            st.write(transcript)

            with st.spinner(
                "Step 2/2: Analyzing for scams..."
            ):

                result = analyze_scam(
                    transcript
                )

            st.success(
                "✅ Scam Analysis Completed"
            )
            display_report(result)
            