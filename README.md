# Help Me Apply — CV Matcher & Generator

A local-first app that compares a candidate’s CV to a job offer, explains what’s strong or missing, recommends improvements, and can generate a new CV based on a fixed template. Built with Streamlit, with multilingual UI (EN/FR), dynamic CV inputs, and local persistence so users don’t retype their info every time.

---

## ✨ Features

- **Step-by-step flow**
  1) **CV Info** (or **load saved** info from disk)
  2) **Job Offer** input + side-by-side **Analysis & Recommendations**
  3) **Generate CV** + **Download**
- **Dynamic CV inputs** for Education & Experience (add multiple entries with a + button)
- **Multilingual UI** (English/French) via `data/translations.json`
- **Local persistence**
  - During a session: `st.session_state`
  - Across reloads: JSON file (e.g., `data/cv.json`)
- **Clean layout**
  - Left: job offer + validate
  - Right: analysis results
  - Bottom: generated CV and download button

---

## 🗂️ Project Structure

```
help-me-apply/
├─ app.py                     # Streamlit app entrypoint (UI flow)
├─ core/
│  └─ storage.py              # save/load CV JSON to disk
├─ data/
│  ├─ translations.json       # EN/FR UI labels (easily extendable)
│  └─ cv.json      # (generated) persisted CV data
└─ requirements.txt
```

---

## 🚀 Quickstart

```bash
# 1) Create a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
streamlit run app.py
```

Open the URL shown (usually http://localhost:8501).

---

## 🧭 How to Use

1. **Choose Language** in the sidebar (EN/FR).
2. If a saved CV exists, the sidebar shows **“Use saved CV data? Yes/No”**:
   - **Yes** → jumps straight to the **Job Offer** page with your CV preloaded (CV form is hidden).
   - **No** → shows the **CV Info** page; fill inputs and **Validate** to proceed.
3. On the **Job Offer** page, paste the job description and **Validate**:
   - Analysis appears on the **right**.
   - A **Generate CV** button appears.
4. Click **Generate CV**, then review and **Download** the result.

> You can always click **“← Modify CV Information”** to go back and adjust your CV. When doing so, the saved CV (if available) is preloaded into the form.

---

## 🌍 Translations

All UI text lives in `data/translations.json`. Example:

```json
{
  "en": {
    "title": "CV Matcher and Generator",
    "validate_cv": "Validate CV Info",
    "validate_job": "Validate Job Offer",
    "generate_button": "Generate CV"
  },
  "fr": {
    "title": "Comparateur et Générateur de CV",
    "validate_cv": "Valider les infos CV",
    "validate_job": "Valider l'offre d'emploi",
    "generate_button": "Générer le CV"
  }
}
```

**How it works**

- To add a new language, add a new top-level key (e.g., `"es": {...}`) and optionally add it to the language selector.

**Dev tip**: You can add a sidebar button to hot-reload translations during development by calling `load_translations.clear()` and `st.experimental_rerun()`.

---

## 💾 Saving & Loading CV Data

- Clicking **Validate CV Info** saves your CV to `data/cv.json`.
- On startup (and via the sidebar), if the file exists, you can **Use saved CV data**:
  - **Yes** → the app loads your saved values into `st.session_state` and moves to Job Offer.
  - **No** → you start at CV input.
- Optional sidebar action (if implemented): **“Clear saved CV”** deletes the file and resets the flow.

**Format (example)**

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+33 6 12 34 56 78",
  "summary": "Data scientist with 4+ years in NLP.",
  "skills": "Python, ML, NLP, SQL",
  "education": [
    {"school": "XYZ University", "start": "2018-09-01", "end": "2021-06-30", "desc": "BSc Computer Science"}
  ],
  "experience": [
    {"company": "ABC Corp", "start": "2021-07-01", "end": "2023-12-31", "desc": "Built NLP pipelines for resumes."}
  ]
}
```

> Dates are stored as ISO strings and converted to `date` objects for Streamlit `date_input` widgets.

---

## 🧩 Key Implementation Notes

- **Session state & widgets**: In Streamlit, once a widget key exists (e.g., `key="use_saved_pref"`), don’t assign directly to `st.session_state.use_saved_pref`. Read it only.
- **Navigation**:
  - `step = 1` → CV inputs
  - `step = 2` → Job offer + analysis
  - `step = 3` → Analysis shown + Generate CV & Download
- **Sidebar selector for saved CV**:
  - Only affects navigation while `step <= 1` (so it doesn’t override later steps).
  - Alternatively, use `on_change` callback to apply the choice once.
- **Modify CV Information**:
  - When clicked, the app preloads saved CV (if exists) into `st.session_state` and routes to Step 1 so fields are pre-filled.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Streamlit**
- Standard library: `json`, `pathlib`, `datetime`
- (Optional / planned) `python-docx`, LaTeX/HTML templates for richer CV export
- (Optional / planned) Local LLM orchestration (Ollama, llama.cpp, etc.)

---

## ⚙️ Configuration

- **Paths**: `core/storage.py` uses project-root relative paths: `data/cv.json`
- **Templates** (optional, future): place in `templates/` for `.docx`, HTML, or LaTeX
- **LLM settings** (future): environment variables for model host/ports, etc.

---

## 🧪 Development Tips

- Use **unique keys** for all dynamic fields: `edu_school_0`, `exp_company_1`, etc.
- When adding/removing dynamic entries, keep counts in `st.session_state.education_entries` / `experience_entries`.
- For layout, prefer `st.columns` and `st.container` to keep sections tidy.

---

## 🗺️ Roadmap

- [ ] Plug in **LLM-based analysis** (local-first via Ollama or llama.cpp)
- [ ] Add **scoring** & structured feedback (match %, missing skills list)
- [ ] **Template-based CV generation** (DOCX/HTML/PDF)
- [ ] Multiple templates + style presets
- [ ] Export CV elements separately (profile, experience,skills,etc)
- [ ] User profiles / multiple saved CVs
- [ ] Basic auth for deployed environments

---

## 🐞 Troubleshooting

- **Saved file not found**:
  - Confirm `data/cv.json` path exists and the app has write permissions.

---

## 📜 License

Choose a license (e.g., MIT) and place it in `LICENSE`. Example:

```
MIT License — Copyright (c) 2025 ...
```

---

## 🙌 Credits

Built for a local-first, privacy-friendly job application workflow with a focus on multi-language UX and a simple, clear user journey.
