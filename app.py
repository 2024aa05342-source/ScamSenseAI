import streamlit as st
import time
from PIL import Image
from modules.ocr_engine import extract_text_from_image
from modules.risk_engine import analyze_scam
from modules.speech_engine import transcribe_audio

def display_report(result):

    st.header("🔎 ScamSenseAI Investigation Report")
    with st.expander("For Judges: Multi-Agent Investigation Workflow"):

        findings = result.get(
            "agent_findings",
            {}
        )

        for agent, output in findings.items():

            st.success(agent)

            st.write(output)
 
    if result["risk_level"] == "CONFIRMED SCAM":
        st.error(
            "🚨 HIGH RISK SCAM\n\nDo NOT share OTPs, passwords, money or personal information."
        )
    
    elif result["risk_level"] == "LIKELY SCAM":
        st.warning(
            "⚠️ SUSPICIOUS MESSAGE\n\nPlease verify with a trusted family member or official source."
        )
    
    else:
        st.success(
            "✅ APPEARS SAFE\n\nNo major scam indicators were detected."
        )

    st.subheader("📌 What Did We Detect?")
    if result["risk_score"] > 80:
        st.error(
            "This message is very likely trying to steal money or personal information."
        )
    
    elif result["risk_score"] > 50:
        st.warning(
            "This message shows several signs of a scam. Be careful."
        )
    else:
        st.success(
            "No major scam indicators were detected."
        )
    st.info(result["scam_type"])
    st.subheader("🔍 Why Is This Suspicious?")

    for item in result["evidence"]:
        st.write(f"📚 {item}")

    st.subheader("⚠️ Warning Signs")

    for item in result["red_flags"]:
        st.write(f"⚠️ {item}")

    st.subheader("✅ What Should I Do?")

    st.success(
        result["recommendation"]
    )

    st.subheader("👨‍👩‍👧 Share With Family")
    
    family_report = f"""ScamSenseAI Alert
    
    Risk Level: {result['risk_level']}
    
    Scam Type: {result['scam_type']}
    
    Recommendation:
    {result['recommendation']}
    """
    
    st.text_area(
        "Share this with a family member or caregiver",
        family_report,
        height=200
    )

    

st.set_page_config(
    page_title="ScamSenseAI",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ ScamSenseAI")

st.subheader(
    "Helping You Stay Safe From Scams"
)

st.success(
    "Check suspicious messages, screenshots and voice recordings before taking action."
)

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

    if st.button("🔍 Check This Message"):

        if not user_text.strip():
            st.warning("Please enter a message to analyze.")
            st.stop()
        
        with st.spinner("Analyzing..."):

            start = time.time()

            result = analyze_scam(user_text)
            end = time.time()

            #st.metric("Inference Time",f"{round(end-start,2)} sec")
            #st.caption("Model: Qwen2.5-3B running on AMD GPU")
            display_report(result)

with tab2:

    st.header("Image Analysis")

    uploaded_file = st.file_uploader(
        "Upload Scam Screenshot",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:

        st.image(uploaded_file)

        if st.button("📷 Check This Screenshot"):

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

        if st.button("🎤 Check This Voice Recording"):

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
            