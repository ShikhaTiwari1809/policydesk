# PolicyDesk
**AI-Powered Healthcare Policy Understanding**  
Cotiviti Hackathon 2024 — Topic 3: Content Management in Healthcare

---

## Submission Deliverables

All submission files are in the `assessment_submission/` folder:

| File | Description |
|------|-------------|
| `Report.pdf` | Written report (2 pages + bibliography) |
| `Report.tex` | LaTeX source for the report |
| `PolicyDesk_Deck.pptx` | 8-slide PowerPoint presentation |
| `Presentation_Recording.mp4` | Video recording of presentation and POC demo |

---

## Project Structure

```
policydesk/
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env                          # OpenAI API key (not committed)
├── .gitignore
│
├── modes/
│   ├── summarizer.py             # Policy Summarizer mode
│   ├── diff.py                   # Policy Diff mode
│   ├── rules_converter.py        # Rules Converter mode
│   └── claim_copilot.py          # Claim Review Copilot mode
│
├── utils/
│   ├── pdf_parser.py             # PDF and text extraction (PyMuPDF)
│   ├── chunker.py                # Token counting and chunking (tiktoken)
│   └── gpt_client.py             # OpenAI API client wrapper
│
├── sample_docs/
│   ├── lcd_epidural_steroid.txt  # Sample CMS LCD for demo
│   ├── em_guidelines_2023.txt    # AMA E/M Guidelines 2023 (for diff demo)
│   ├── em_guidelines_2024.txt    # CMS E/M Updates 2024 (for diff demo)
│   └── synthetic_claims.json     # Three synthetic claims for copilot demo
│
└── assessment_submission/
    ├── Report.pdf
    ├── Report.tex
    ├── PolicyDesk_Deck.pptx
    └── Presentation_Recording.mp4
```

---

## Setup and Running

### Prerequisites
- Python 3.9 or higher
- An OpenAI API key with GPT-4o access

### 1. Clone or download the project

```bash
cd policydesk
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-key-here
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## Features

### Policy Summarizer
Upload any PDF or plain text policy document. The app extracts a structured summary including policy name, effective date, CPT codes, coverage criteria, exclusions, and documentation requirements.

### Policy Diff
Upload two versions of a policy (older and newer). The app identifies every material change, classifies each as High / Medium / Low impact, and shows the before and after text for each change.

### Rules Converter
Upload a policy and convert it to either a structured JSON rules array or executable Python adjudication code that can feed into a rules engine.

### Claim Review Copilot
Upload a policy and enter a claim scenario (manually or load from `synthetic_claims.json`). The app evaluates the claim against the policy and returns PASS / FLAG / DENY with confidence level, policy citations, missing documentation, and a reviewer recommendation.

---

## Sample Documents

Three sample documents are included for demo purposes:

- **`lcd_epidural_steroid.txt`** — Realistic CMS LCD L36920 for Epidural Steroid Injections. Use with Policy Summarizer and Claim Review Copilot.
- **`em_guidelines_2023.txt` + `em_guidelines_2024.txt`** — AMA/CMS E/M Guidelines across two years. Use with Policy Diff to see version comparison.
- **`synthetic_claims.json`** — Three synthetic claims (PASS, DENY, edge case FLAG). Use with Claim Review Copilot.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| UI | Streamlit |
| LLM | GPT-4o via OpenAI API |
| Prompting | Prompt engineering only — no fine-tuning, no RAG |
| PDF extraction | PyMuPDF (fitz) |
| Tokenization | tiktoken |
| API key management | python-dotenv |
| Output format | JSON-mode structured responses |
