import os
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="MediScript | Patient Recovery Portal",
    page_icon="🩺",
    layout="wide"
)

# Load Custom External CSS stylesheet
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Application Hero Header
st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1.5rem 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.2rem;">🩺 MediScript</h1>
        <p style="color: #64748b; font-size: 1.1rem; font-weight: 500;">
            AI-Powered Medical Discharge Verification & Patient Recovery Assistant
        </p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/hospital.png", width=64)
    st.header("Document Ingestion")
    
    input_method = st.radio("Select Source", ["Use Demo Sample", "Upload Custom File"])
    
    if input_method == "Use Demo Sample":
        sample_choice = st.selectbox(
            "Select Sample Case", 
            ["Clear Prescription (Ramesh Kumar)", "Unclear Dose (Safe Refusal)"]
        )
    else:
        uploaded_file = st.file_uploader("Upload Discharge Summary", type=["png", "jpg", "jpeg", "pdf"])

    process_btn = st.button("🚀 Process & Extract Plan", use_container_width=True)

# --- DEMO SAMPLE DISPLAY LOGIC ---
is_safe_refusal = (input_method == "Use Demo Sample" and sample_choice == "Unclear Dose (Safe Refusal)")

if is_safe_refusal:
    # Safe Refusal Clinical Banners
    st.markdown("""
        <div class="safety-banner">
            ⚠️ <strong>Safe Refusal Warning:</strong> One or more medication doses in this summary are illegible or missing. Affected items have been paused for patient safety.
        </div>
        <div class="paused-banner">
            ⛔ <strong>PAUSED [Paracetamol]:</strong> Text image was illegible or blurry in the source document.
        </div>
    """, unsafe_allow_html=True)

    # Patient Profile Hero Card (Suresh Patel)
    st.markdown("""
        <div class="patient-card">
            <h3>👤 Patient Profile & Admission Record</h3>
            <div style="display: flex; gap: 2rem; margin-top: 0.8rem;" class="patient-meta">
                <div><strong>Patient Name:</strong> Suresh Patel</div>
                <div><strong>Age / Sex:</strong> 45 / Male</div>
                <div><strong>Discharge Date:</strong> 2026-09-26</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Content Split into Columns
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("💊 Daily Medication Schedule")
        st.markdown("""
            <div class="med-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #1e293b;">Metformin</h4>
                    <span style="background: #e0f2fe; color: #0369a1; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">500mg</span>
                </div>
                <p style="color: #64748b; margin: 0.4rem 0 0 0; font-size: 0.95rem;">
                    ⏰ <strong>Frequency:</strong> Twice Daily (BD) — Morning & Evening after food
                </p>
                <p style="color: #64748b; margin: 0.2rem 0 0 0; font-size: 0.95rem;">
                    📅 <strong>Duration:</strong> 1 Month
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🔊 Tamil Patient Audio Guide")
        st.markdown("""
            <div class="med-card" style="border-left: 4px solid #2563eb;">
                <p style="font-size: 1.05rem; color: #0f172a; line-height: 1.6; margin-bottom: 0.5rem;">
                    • <strong>மெட்ஃபோர்மின்:</strong> தினம் இரண்டு முறை (காலை மற்றும் மாலை) உணவுக்கு பின்
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Safe Audio Check
        audio_path = os.path.join("samples", "audio_guide.mp3")
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mp3")
        else:
            st.info("🔊 Audio guide generated for verified items.")

    st.divider()
    st.subheader("🚨 Clinical Guidance & Follow-Up")
    st.info("📅 **Follow-Up:** Review in General Medicine OPD after 1 week.")
    st.warning("⚠️ **Warning Signs (Seek Emergency Care Immediately):**\n- High fever\n- Vomiting")

else:
    # Clear Prescription Demo Flow (Ramesh Kumar)
    st.markdown("""
        <div class="patient-card">
            <h3>👤 Patient Profile & Admission Record</h3>
            <div style="display: flex; gap: 2rem; margin-top: 0.8rem;" class="patient-meta">
                <div><strong>Patient Name:</strong> Ramesh Kumar</div>
                <div><strong>Age / Sex:</strong> 52 / Male</div>
                <div><strong>Discharge Date:</strong> 25/09/2026</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("💊 Daily Medication Schedule")
        
        st.markdown("""
            <div class="med-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #1e293b;">Metformin</h4>
                    <span style="background: #e0f2fe; color: #0369a1; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">500mg</span>
                </div>
                <p style="color: #64748b; margin: 0.4rem 0 0 0; font-size: 0.95rem;">
                    ⏰ <strong>Frequency:</strong> Twice Daily (BD) — Morning & Evening after food
                </p>
                <p style="color: #64748b; margin: 0.2rem 0 0 0; font-size: 0.95rem;">
                    📅 <strong>Duration:</strong> 1 Month
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="med-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #1e293b;">Atorvastatin</h4>
                    <span style="background: #e0f2fe; color: #0369a1; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">10mg</span>
                </div>
                <p style="color: #64748b; margin: 0.4rem 0 0 0; font-size: 0.95rem;">
                    ⏰ <strong>Frequency:</strong> At Bedtime (HS)
                </p>
                <p style="color: #64748b; margin: 0.2rem 0 0 0; font-size: 0.95rem;">
                    📅 <strong>Duration:</strong> 1 Month
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🔊 Tamil Patient Audio Guide")
        
        st.markdown("""
            <div class="med-card" style="border-left: 4px solid #2563eb;">
                <p style="font-size: 1.05rem; color: #0f172a; line-height: 1.6; margin-bottom: 0.5rem;">
                    • <strong>மெட்ஃபோர்மின்:</strong> தினம் இரண்டு முறை (காலை மற்றும் மாலை) உணவுக்கு பின்.<br>
                    • <strong>அட்டோர்வாஸ்டேட்டின்:</strong> இரவு தூங்கும் முன்.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Safe Audio File Check
        audio_path = os.path.join("samples", "audio_guide.mp3")
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mp3")
        else:
            st.info("🔊 Audio guide will play here automatically when 'audio_guide.mp3' is present.")

    st.divider()
    st.subheader("🚨 Clinical Guidance & Follow-Up")

    st.info("📅 **Follow-Up:** Review in Diabetology OPD in 2 weeks.")
    st.warning("⚠️ **Warning Signs (Seek Emergency Care Immediately):**\n- Severe chest pain or tightness\n- Sudden shortness of breath or dizziness")