# 🏥 MediScript — Safety-First AI Medical Discharge Verification & Patient Recovery Assistant

> **MediScript** is a clinical safety platform and multi-tab web application engineered to convert complex, jargon-heavy hospital discharge summaries into grounded, safe, and regional-language patient recovery plans. Designed with a **Safety-First Architecture**, MediScript prevents dangerous AI hallucinations by utilizing **Safe Refusal Guardrails** whenever encountering ambiguous, blurry, or unreadable doctor handwriting.

---

## 🌟 Key Features & Highlights

- **🛡️ Safe Refusal Guardrails**: Unlike standard LLMs that make unsafe guesses on blurry or scribbled text, MediScript detects ambiguous prescriptions, actively pauses the item, and escalates it to clinicians.
- **🔍 Line-by-Line Evidence & RxNorm Grounding**: Cross-references every extracted medication against the **NIH RxNorm Clinical Drug Database** (Concept IDs) and provides exact source text line references.
- **🇮🇳 Regional Localization & TTS**: Translates post-discharge care schedules into plain Tamil text and generates spoken audio guides via an embedded Text-to-Speech engine.
- **🧠 Interactive Teach-Back Comprehension Module**: Incorporates a clinical Teach-Back quiz to verify patient schedule comprehension prior to portal checkout.
- **🔥 Live Firebase Firestore Persistence**: Continuous, asynchronous cloud data synchronization tracking patient records, role-based access control, and real-time administrative telemetry.
- **⚡ Local-Edge Processing**: Primary OCR runs locally via Tesseract for sub-second rendering and network-independent presentation reliability.

---

## 🏗️ System Architecture



mediscript/
│
├── app.py                         # Main Streamlit command entry point & UI multi-tab portal
├── requirements.txt                # Project dependencies
├── .env                           # Environment variables & API keys
├── .gitignore                     # Git tracking exclusions
├── firebase_key.json              # Firebase service account credentials (Ignored)
│
├── src/                           # Core Application Package
│   ├── init.py
│   ├── ocr/                       # Optical Character Recognition Engine
│   │   ├── init.py
│   │   ├── tesseract_ocr.py       # Primary local Tesseract OCR engine
│   │   └── vision_ocr.py          # Google Cloud Vision fallback OCR
│   │
│   ├── extraction/                # LLM Structured Parsing & Validation
│   │   ├── init.py
│   │   ├── llm_extractor.py       # Gemini API structured JSON parser
│   │   └── validators.py          # Data sanitizer & default field normalizer
│   │
│   ├── verification/              # Clinical Verification Engine & Guardrails
│   │   ├── init.py
│   │   ├── engine.py              # Line-by-line evidence proof & RxNorm grounding
│   │   ├── refusal.py             # Safe Refusal logic & ambiguous dose interceptor
│   │   └── schema.py              # Unified patient/hospital schema definitions
│   │
│   ├── translation/               # Regional Language Localization
│   │   ├── init.py
│   │   └── tamil.py               # Tamil instruction & schedule transformer
│   │
│   ├── tts/                       # Audio Generation Module
│   │   ├── init.py
│   │   └── speech.py              # Text-to-Speech (gTTS) audio generator
│   │
│   └── utils/                     # Utility Handlers
│       ├── init.py
│       ├── file_handler.py        # Edge temporary file stream handling
│       └── helpers.py             # Caregiver summary exporter & formatting tools
│
├── samples/                       # Benchmark Test Datasets
│   ├── clear_sample_1.txt         # Standard Discharge Dataset (Ramesh Kumar)
│   └── unclear_dose_sample.pdf    # Illegible/Ambiguous Dose Dataset (Suresh Patel)
│
├── assets/                        # Custom CSS Styling & UI Elements
│   └── style.css
│
└── tests/                         # Automated Unit Tests
├── test_extraction.py         # JSON schema & extraction tester
└── test_verification.py       # Safe Refusal trigger tester



---

## 📊 Datasets & Grounding Standards

1. **NIH RxNorm Vocabulary**: Every extracted drug is grounded against official RxNorm concept IDs (e.g., Metformin $\rightarrow$ `RxNorm ID: 6809`, Atorvastatin $\rightarrow$ `RxNorm ID: 83367`).
2. **PhysioNet MIMIC-III Clinical Benchmark**: Sample discharge summaries are structured based on de-identified real-world clinical discharge schemas from the MIMIC-III database.

---

## 🛠️ Setup & Installation

### Prerequisites
* Python 3.9+
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed locally

### 1. Clone the Repository
```bash
git clone [https://github.com/Darshan908022/mediscript.git](https://github.com/Darshan908022/mediscript.git)
cd mediscript