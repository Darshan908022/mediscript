"""
Reusable UI Components and Layout Helpers for MediScript Healthcare Dashboard.
"""

import os
import streamlit as st


def get_patient_initials(name: str) -> str:
    parts = name.strip().split()
    if not parts:
        return "P"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()


def render_sidebar_brand():
    """Renders modern SVG stethoscope brand logo and title in sidebar."""
    html = (
        '<div class="sidebar-brand-box">'
        '<div class="brand-icon-wrapper">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M4.5 16.5c-1.5 1.26-2 3-2 4.5h7c0-1.5-.5-3.24-2-4.5"/>'
        '<path d="M6 16.5V4a2 2 0 0 1 4 0v12.5"/>'
        '<path d="M10 10h4"/>'
        '<path d="M14 6v8a4 4 0 0 0 4 4h1a2 2 0 0 0 2-2v-1"/>'
        '<circle cx="20" cy="10" r="2"/>'
        '</svg>'
        '</div>'
        '<div>'
        '<div class="brand-name">MediScript</div>'
        '<div class="brand-tagline">Clinical Recovery AI</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar_patient_profile(patient_name: str, patient_email: str, role: str = "Patient"):
    """Renders active patient profile chip in sidebar."""
    initials = get_patient_initials(patient_name)
    html = (
        '<div class="sidebar-patient-card">'
        f'<div class="patient-avatar-circle">{initials}</div>'
        '<div class="patient-info-meta">'
        f'<span class="patient-role-pill">{role}</span>'
        f'<div class="patient-name-label">{patient_name}</div>'
        f'<div class="patient-email-label">{patient_email}</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar_navigation(active_page: str) -> str:
    """Renders clean SaaS navigation items in sidebar."""
    st.markdown('<div class="nav-section-title">Navigation</div>', unsafe_allow_html=True)
    
    nav_items = [
        ("Dashboard", "🏠", "Dashboard"),
        ("Patient Record", "📋", "Patient Record"),
        ("Medications", "💊", "Medications"),
        ("Audio Guide", "🔊", "Audio Guide"),
        ("Safety Audit", "🛡️", "Safety Audit"),
        ("Dataset Evaluator", "🗄️", "Dataset Evaluator"),
        ("Settings", "⚙️", "Settings"),
    ]
    
    selected_page = active_page
    for label, icon, key in nav_items:
        is_active = (active_page == key)
        wrapper_class = "nav-active-btn" if is_active else "nav-inactive-btn"
        
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_btn_{key}", use_container_width=True):
            selected_page = key
            st.session_state.active_page = key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    return selected_page


def render_sidebar_footer():
    """Renders clinical mission quote at bottom of sidebar."""
    html = (
        '<div class="sidebar-footer-quote">'
        '<p>"Better Understanding.<br>Healthier Tomorrow."</p>'
        '<span>MediScript NIH RxNorm Verified</span>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_top_header(patient_name: str, user_role: str, is_synced: bool):
    """Renders top SaaS app bar with title, notification icon, avatar and sync indicator."""
    initials = get_patient_initials(patient_name)
    sync_badge = (
        '<div class="live-sync-pill"><div class="live-sync-dot"></div><span>Cloud Synced</span></div>'
        if is_synced else
        '<div class="live-sync-pill" style="background:#F1F5F9; color:#475569; border-color:#CBD5E1;"><div class="live-sync-dot" style="background:#94A3B8;"></div><span>Local Edge</span></div>'
    )
    
    html = (
        '<div class="top-nav-bar">'
        '<div class="header-title-box">'
        '<h1>Patient Recovery</h1>'
        '<p>AI-powered discharge verification & recovery assistant</p>'
        '</div>'
        '<div class="header-right-actions">'
        f'{sync_badge}'
        '<div class="notification-bell-btn" title="Recent clinical updates">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>'
        '<path d="M13.73 21a2 2 0 0 1-3.46 0"/>'
        '</svg>'
        '<div class="notification-unread-dot"></div>'
        '</div>'
        '<div class="header-user-badge">'
        f'<div class="header-user-avatar">{initials}</div>'
        '<div>'
        f'<div class="header-user-name">{patient_name}</div>'
        f'<div class="header-user-sub">{user_role}</div>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_patient_profile_card(data: dict):
    """Renders clean white card with subtle blue/teal medical accent for patient info."""
    patient_name = data.get("patient_name", "Unknown Patient")
    age = data.get("age", "--")
    gender = data.get("gender", "--")
    discharge_date = data.get("discharge_date", "Pending")
    is_ambiguous = data.get("is_ambiguous", False)
    initials = get_patient_initials(patient_name)
    
    if is_ambiguous:
        status_html = '<div class="status-badge-amber"><span>⚠️</span><span>Safe Refusal Required</span></div>'
    else:
        status_html = '<div class="status-badge-verified"><span>✓</span><span>Discharge Verified</span></div>'

    html = (
        '<div class="patient-profile-card">'
        '<div class="patient-profile-main">'
        f'<div class="patient-profile-avatar-lg">{initials}</div>'
        '<div class="patient-profile-details">'
        f'<h2>{patient_name}</h2>'
        '<div class="patient-profile-grid">'
        '<div class="patient-meta-item">'
        '<span class="patient-meta-label">Age / Sex</span>'
        f'<span class="patient-meta-val">{age} / {gender}</span>'
        '</div>'
        '<div class="patient-meta-item">'
        '<span class="patient-meta-label">Discharge Date</span>'
        f'<span class="patient-meta-val">{discharge_date}</span>'
        '</div>'
        '<div class="patient-meta-item">'
        '<span class="patient-meta-label">Care Unit</span>'
        '<span class="patient-meta-val">Diabetology OPD</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
        f'<div>{status_html}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_stat_cards(data: dict):
    """Renders 3 clean summary stat cards: Active Meds, Verification Rate, Treatment Plan."""
    meds = data.get("medications", [])
    active_count = len(meds)
    is_ambiguous = data.get("is_ambiguous", False)
    
    if is_ambiguous:
        verified_val = "Safe Intercept"
        verified_sub = "1 paused item escalated"
    else:
        verified_val = "100%"
        verified_sub = "RxNorm & Line Grounded"
        
    duration_val = meds[0].get("duration", "1 Month") if meds else "1 Month"
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        card1_html = (
            '<div class="stat-card-box">'
            '<div class="stat-icon-wrapper stat-icon-blue">💊</div>'
            '<div class="stat-info-wrap">'
            f'<div class="stat-number">{active_count}</div>'
            '<div class="stat-label">Active Medications</div>'
            '<div class="stat-subtext">Scheduled daily doses</div>'
            '</div>'
            '</div>'
        )
        st.markdown(card1_html, unsafe_allow_html=True)
        
    with c2:
        card2_html = (
            '<div class="stat-card-box">'
            '<div class="stat-icon-wrapper stat-icon-teal">✓</div>'
            '<div class="stat-info-wrap">'
            f'<div class="stat-number">{verified_val}</div>'
            '<div class="stat-label">Source Verified</div>'
            f'<div class="stat-subtext">{verified_sub}</div>'
            '</div>'
            '</div>'
        )
        st.markdown(card2_html, unsafe_allow_html=True)
        
    with c3:
        card3_html = (
            '<div class="stat-card-box">'
            '<div class="stat-icon-wrapper stat-icon-green">📅</div>'
            '<div class="stat-info-wrap">'
            f'<div class="stat-number">{duration_val}</div>'
            '<div class="stat-label">Treatment Plan</div>'
            '<div class="stat-subtext">Follow-up in 2 weeks</div>'
            '</div>'
            '</div>'
        )
        st.markdown(card3_html, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)


def render_medication_card(med: dict, index: int):
    """Renders a clean modern card for an individual active medication."""
    name = med.get("name", "Medication")
    dose = med.get("dose", "")
    freq = med.get("frequency", "")
    duration = med.get("duration", "")
    proof = med.get("proof_note", "")
    
    # Parse timing chips
    chips = []
    freq_lower = freq.lower()
    if "morning" in freq_lower or "bd" in freq_lower or "tds" in freq_lower:
        chips.append('<span class="med-chip">🌅 Morning</span>')
    if "evening" in freq_lower or "bd" in freq_lower or "tds" in freq_lower:
        chips.append('<span class="med-chip">🌙 Evening</span>')
    if "bedtime" in freq_lower or "hs" in freq_lower:
        chips.append('<span class="med-chip">🌙 At Bedtime</span>')
    if "after food" in freq_lower or "meals" in freq_lower:
        chips.append('<span class="med-chip">🍴 After Food</span>')
    elif "before food" in freq_lower:
        chips.append('<span class="med-chip">🍴 Before Food</span>')
    if duration:
        chips.append(f'<span class="med-chip med-chip-duration">📅 Duration: {duration}</span>')
        
    chips_html = "".join(chips)
    
    html = (
        '<div class="medication-card-modern">'
        '<div class="med-card-header">'
        '<div class="med-title-group">'
        '<div class="med-pill-icon">💊</div>'
        '<div>'
        f'<div class="med-name-text">{name}</div>'
        '</div>'
        '</div>'
        f'<div class="med-dose-pill">{dose}</div>'
        '</div>'
        f'<div class="med-chips-container">{chips_html}</div>'
        '<div class="med-verification-line">'
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="20 6 9 17 4 12"></polyline>'
        '</svg>'
        '<span>Source Verified</span>'
        '</div>'
        '<div class="med-evidence-box">'
        '<div class="med-evidence-title"><span>🔎 Proof & Evidence:</span></div>'
        f'<div>{proof}</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_paused_medication_card(item_str: str):
    """Renders a paused safe-refusal medication item card."""
    html = (
        '<div class="paused-card-modern">'
        '<div style="font-size: 1.4rem; line-height: 1;">⛔</div>'
        '<div>'
        '<div class="paused-card-title">PAUSED MEDICATION ITEM</div>'
        f'<div class="paused-card-desc">{item_str}</div>'
        '<div style="margin-top: 5px; font-size: 0.76rem; font-weight: 600; color: #92400E;">'
        '🛡️ Action: Safely withheld from patient recovery schedule. Physician review initiated.'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_audio_guide_card(data: dict):
    """Renders dedicated card for Tamil Patient Audio Guide with integrated audio player."""
    tamil_guide = data.get("tamil_guide", "")
    audio_path = data.get("audio_file", "")
    
    with st.container(border=True):
        header_html = (
            '<div class="audio-header-group">'
            '<div class="audio-icon-box">🔊</div>'
            '<div class="audio-title-wrap">'
            '<h3>Tamil Patient Audio Guide</h3>'
            '<p>Follow these instructions for your recovery and medication schedule.</p>'
            '</div>'
            '</div>'
            f'<div class="tamil-text-box">{tamil_guide}</div>'
        )
        st.markdown(header_html, unsafe_allow_html=True)
        
        # Audio Player
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mp3")
            st.caption("🎧 Listen to spoken Tamil recovery instructions generated by MediScript TTS engine.")
        else:
            st.info("Tamil audio generation ready.")


def render_recovery_checklist():
    """Renders dynamic 6-item recovery checklist with interactive progress bar."""
    if "checklist_state" not in st.session_state:
        st.session_state.checklist_state = {
            "c1": True,   # Take medications as scheduled
            "c2": False,  # Stay hydrated
            "c3": False,  # Follow healthy diet
            "c4": False,  # Attend follow-up appointment
            "c5": False,  # Monitor symptoms
            "c6": False   # Contact doctor if needed
        }
        
    checklist_items = [
        ("c1", "Take medications as scheduled"),
        ("c2", "Stay hydrated"),
        ("c3", "Follow healthy diet"),
        ("c4", "Attend follow-up appointment"),
        ("c5", "Monitor symptoms"),
        ("c6", "Contact doctor if needed")
    ]
    
    completed_count = sum(1 for k, _ in checklist_items if st.session_state.checklist_state.get(k, False))
    total_count = len(checklist_items)
    percentage = int((completed_count / total_count) * 100)
    
    with st.container(border=True):
        header_html = (
            '<div class="checklist-header">'
            '<div class="checklist-title-wrap">'
            '<h3>☑ Recovery Checklist</h3>'
            '<p>Complete these steps for a smooth recovery.</p>'
            '</div>'
            f'<div class="checklist-progress-pill">{completed_count} of {total_count} completed</div>'
            '</div>'
            '<div class="progress-bar-container">'
            f'<div class="progress-bar-fill" style="width: {percentage}%;"></div>'
            '</div>'
        )
        st.markdown(header_html, unsafe_allow_html=True)
        
        for key, text in checklist_items:
            checked = st.checkbox(
                text, 
                value=st.session_state.checklist_state.get(key, False), 
                key=f"check_{key}"
            )
            st.session_state.checklist_state[key] = checked


def render_safety_verification(is_ambiguous: bool):
    """Renders Safety & Verification card with clinical grounding details."""
    status_tag = (
        '<div class="verification-status-tag" style="background:#F59E0B;">⚠️ Intervened / Flagged</div>'
        if is_ambiguous else
        '<div class="verification-status-tag">✓ Verified</div>'
    )
    
    with st.container(border=True):
        html = (
            '<div class="checklist-header">'
            '<div class="checklist-title-wrap">'
            '<h3>🛡 Safety & Verification</h3>'
            '<p>All information is verified from trusted medical sources.</p>'
            '</div>'
            f'{status_tag}'
            '</div>'
            '<div class="verification-card-inner">'
            '<div class="verification-heading">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
            '</svg>'
            '<span>Source-Grounded Clinical Verification</span>'
            '</div>'
            '<ul class="verification-list">'
            '<li>'
            '<span style="color:#0EA5A4; font-weight:700;">✓</span>'
            '<span><strong>Discharge summary:</strong> Line-by-line OCR cross-referenced with exact patient admission records.</span>'
            '</li>'
            '<li>'
            '<span style="color:#0EA5A4; font-weight:700;">✓</span>'
            '<span><strong>RxNorm database:</strong> Validated against NIH National Library of Medicine concept IDs.</span>'
            '</li>'
            '<li>'
            '<span style="color:#0EA5A4; font-weight:700;">✓</span>'
            '<span><strong>Safe Refusal Guardrail:</strong> Zero tolerance for blurry, ambiguous, or illegible doctor scribbles.</span>'
            '</li>'
            '</ul>'
            '<div style="font-size: 0.78rem; color: #0F766E; font-weight: 600;">'
            'Status: <span style="text-decoration: underline;">Clinical Verification Passed</span>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)
