import streamlit as st
from datetime import date
from core.storage import save_cv_to_file, load_from_file
from datetime import datetime
from core.llm_tasks import get_llm, AnalyzerRecommender, Generator

# --- Page config ---
st.set_page_config(page_title="Help me apply", layout="wide")


# --- Init session state ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "education_entries" not in st.session_state:
    st.session_state.education_entries = 1
if "experience_entries" not in st.session_state:
    st.session_state.experience_entries = 1

# --- Sidebar: Language & Saved CV Management ---
lang_code = st.sidebar.selectbox("Language / Langue", ["en", "fr"])

# Load LLM once
llm = get_llm(language=lang_code, model="gemma3:4b")

analyzer = AnalyzerRecommender(llm)
generator = Generator(llm)

translations_filename = "translations.json"
translations = load_from_file(translations_filename)
t = translations.get(lang_code, translations["en"])

# Load saved data (if any)
cv_filename = "cv.json"
saved_data = load_from_file(cv_filename)

if saved_data:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Saved data")
    
    # Simple buttons instead of radio with callback
    if st.sidebar.button("📋 Use Saved CV"):
        # Load saved data into session_state
        st.session_state.cv_name = saved_data.get("name", "")
        st.session_state.cv_email = saved_data.get("email", "")
        st.session_state.cv_phone = saved_data.get("phone", "")
        st.session_state.cv_summary = saved_data.get("summary", "")
        st.session_state.cv_skills = saved_data.get("skills", "")
        st.session_state.education_entries = max(1, len(saved_data.get("education", [])))
        st.session_state.experience_entries = max(1, len(saved_data.get("experience", [])))

        # Load education entries
        for i, edu in enumerate(saved_data.get("education", [])):
            st.session_state[f"edu_school_{i}"] = edu.get("school", "")
            st.session_state[f"edu_start_{i}"] = datetime.fromisoformat(edu["start"])
            st.session_state[f"edu_end_{i}"] = datetime.fromisoformat(edu["end"])
            st.session_state[f"edu_desc_{i}"] = edu.get("desc", "")

        # Load experience entries
        for i, exp in enumerate(saved_data.get("experience", [])):
            st.session_state[f"exp_company_{i}"] = exp.get("company", "")
            st.session_state[f"exp_start_{i}"] = datetime.fromisoformat(exp["start"])
            st.session_state[f"exp_end_{i}"] = datetime.fromisoformat(exp["end"])
            st.session_state[f"exp_desc_{i}"] = exp.get("desc", "")

        # Go to job offer page
        st.session_state.step = 2
        st.rerun()
    
    if st.sidebar.button("🆕 Start Fresh"):
        st.session_state.step = 1
        st.rerun()
    
    if st.sidebar.button("🗑️ Clear Saved CV"):
        from core.storage import delete_cv_file
        try:
            delete_cv_file()
        except Exception:
            pass
        st.session_state.step = 1
        st.rerun()

def _load_saved_cv_into_session(saved):
    # Basic fields
    st.session_state.cv_name = saved.get("name", "")
    st.session_state.cv_email = saved.get("email", "")
    st.session_state.cv_phone = saved.get("phone", "")
    st.session_state.cv_summary = saved.get("summary", "")
    st.session_state.cv_skills = saved.get("skills", "")

    # Section counts
    st.session_state.education_entries = max(1, len(saved.get("education", [])))
    st.session_state.experience_entries = max(1, len(saved.get("experience", [])))

    # Dates can be iso strings or already date-like; handle both.
    from datetime import datetime, date as _date

    def _to_date(v):
        # Streamlit date_input needs a date; convert string to date
        if isinstance(v, _date):
            return v
        if isinstance(v, str) and v:
            # tolerate date or datetime iso strings
            try:
                return datetime.fromisoformat(v).date()
            except ValueError:
                pass
        return _date(2000, 1, 1)  # safe fallback

    # Education
    for i, edu in enumerate(saved.get("education", [])):
        st.session_state[f"edu_school_{i}"] = edu.get("school", "")
        st.session_state[f"edu_start_{i}"] = _to_date(edu.get("start", ""))
        st.session_state[f"edu_end_{i}"]   = _to_date(edu.get("end", ""))
        st.session_state[f"edu_desc_{i}"]  = edu.get("desc", "")

    # Experience
    for i, exp in enumerate(saved.get("experience", [])):
        st.session_state[f"exp_company_{i}"] = exp.get("company", "")
        st.session_state[f"exp_start_{i}"]   = _to_date(exp.get("start", ""))
        st.session_state[f"exp_end_{i}"]     = _to_date(exp.get("end", ""))
        st.session_state[f"exp_desc_{i}"]    = exp.get("desc", "")


st.title(t["title"])

cv_data = saved_data if saved_data else {}
job_text = ""

# --- STEP 1: CV Input ---
if st.session_state.step == 1:
    st.header(t["personal_info"])
    st.text_input(t["name"], key="cv_name")
    st.text_input(t["email"], key="cv_email")
    st.text_input(t["phone"], key="cv_phone")

    st.header(t["profile_summary"])
    st.text_area(t["summary_placeholder"], key="cv_summary")

    st.header(t["education"])
    for i in range(st.session_state.education_entries):
        with st.expander(f"{t['education']} {i + 1}"):
            st.text_input(f"{t['school']} ({i+1})", key=f"edu_school_{i}")
            st.date_input(f"{t['start_date']} ({i+1})", key=f"edu_start_{i}", value=date(2018, 1, 1))
            st.date_input(f"{t['end_date']} ({i+1})", key=f"edu_end_{i}", value=date(2021, 1, 1))
            st.text_area(f"{t['description']} ({i+1})", key=f"edu_desc_{i}")

    if st.button(f"+ {t['add_entry']} ({t['education']})"):
        st.session_state.education_entries += 1
        st.rerun()

    st.header(t["experience"])
    for i in range(st.session_state.experience_entries):
        with st.expander(f"{t['experience']} {i + 1}"):
            st.text_input(f"{t['company']} ({i+1})", key=f"exp_company_{i}")
            st.date_input(f"{t['start_date']} ({i+1})", key=f"exp_start_{i}", value=date(2021, 2, 1))
            st.date_input(f"{t['end_date']} ({i+1})", key=f"exp_end_{i}", value=date(2023, 2, 1))
            st.text_area(f"{t['description']} ({i+1})", key=f"exp_desc_{i}")

    if st.button(f"+ {t['add_entry']} ({t['experience']})"):
        st.session_state.experience_entries += 1
        st.rerun()

    st.text_area(t["skills_placeholder"], key="cv_skills")

    if st.button(t["validate_cv"]):
        # Build data dictionary
        cv_data = {
            "name": st.session_state.get("cv_name", ""),
            "email": st.session_state.get("cv_email", ""),
            "phone": st.session_state.get("cv_phone", ""),
            "summary": st.session_state.get("cv_summary", ""),
            "skills": st.session_state.get("cv_skills", ""),
            "education": [],
            "experience": []
        }

        for i in range(st.session_state.education_entries):
            cv_data["education"].append({
                "school": st.session_state.get(f"edu_school_{i}", ""),
                "start": str(st.session_state.get(f"edu_start_{i}", "")),
                "end": str(st.session_state.get(f"edu_end_{i}", "")),
                "desc": st.session_state.get(f"edu_desc_{i}", "")
            })

        for i in range(st.session_state.experience_entries):
            cv_data["experience"].append({
                "company": st.session_state.get(f"exp_company_{i}", ""),
                "start": str(st.session_state.get(f"exp_start_{i}", "")),
                "end": str(st.session_state.get(f"exp_end_{i}", "")),
                "desc": st.session_state.get(f"exp_desc_{i}", "")
            })

        save_cv_to_file(cv_data)  # Save locally
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: Job Offer Input ---
elif st.session_state.step == 2:
    # Navigation button to go back to CV
    if st.button(t["back_to_cv"]):
        saved = load_from_file(cv_filename)
        if saved:
            _load_saved_cv_into_session(saved)
        st.session_state.step = 1
        st.rerun()
    
    # Initialize job offer text if not already set
    if "job_offer_text" not in st.session_state:
        st.session_state.job_offer_text = ""
    
    st.header(t["job_offer"])
    st.text_area(t["job_offer_placeholder"], key="job_offer_text")

    if st.button(t["validate_job"]):
        st.session_state.step = 3
        st.rerun()

    job_text = st.session_state.get("job_offer_text", "")

# --- STEP 3: Analysis + CV Generation ---
elif st.session_state.step == 3:
    # Navigation buttons at the top
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 2])
    
    with col_nav1:
        if st.button(t["back_to_cv"]):
            saved = load_from_file(cv_filename)
            if saved:
                _load_saved_cv_into_session(saved)
            st.session_state.step = 1
            st.rerun()

    
    with col_nav2:
        if st.button(t["back_to_job"]):
            st.session_state.step = 2
            st.rerun()
    
    with col_nav3:
        if st.session_state.get("analysis_ready"):
            if st.button(t["redo_analysis"]):
                # Clear previous analysis results
                st.session_state.analysis_result = None
                st.session_state.analysis_ready = False
                st.session_state.generated_cv = None
                st.session_state.cv_ready = False
                st.rerun()
    
    st.markdown("---")  # Separator line
    
    st.subheader(t["job_offer"])

    col1, col2 = st.columns([1, 1])

    # --- Left column: Job Offer Display + Analyze Button ---
    with col1:
        st.text_area(
            t["job_offer_placeholder"], 
            value=st.session_state.get("job_offer_text", ""), 
            disabled=True,
            height=200
        )
        if st.button(t["analyze_button"]):
            analysis_and_recs = analyzer.run(cv_data, job_text)
            st.session_state.analysis_result = analysis_and_recs
            st.session_state.analysis_ready = True
            st.rerun()

    # --- Right column: Analysis Output ---
    with col2:
        st.subheader(t["analysis_title"])
        if st.session_state.get("analysis_ready"):
            st.markdown(st.session_state.analysis_result)
        else:
            st.info("👈 Click 'Analyze CV' to get feedback")

    # --- Below columns: Generated CV and Download ---
    if st.session_state.get("analysis_ready"):
        st.markdown("---")  # Divider line
        if st.button(t["generate_button"]):
            recs = st.session_state.analysis_result
            generated_sections = {
                "profile": generator.rewrite_profile(cv_data.get("summary", ""), recs),
                "skills": generator.rewrite_skills(cv_data.get("skills", ""), recs),
                "experience": [generator.rewrite_experience(e, recs) for e in cv_data.get("experience", [])],
                "education": [generator.rewrite_education(e, recs) for e in cv_data.get("education", [])],
            }
            st.session_state.generated_cv = generated_sections
            st.session_state.cv_ready = True
            st.rerun()

    if st.session_state.get("cv_ready"):
        st.success(t["cv_generated"])
        st.text_area("Generated CV", value=st.session_state.generated_cv, height=300)

        st.download_button(
            label=t["download_cv"],
            data=st.session_state.generated_cv,
            file_name="generated_cv.txt",
            mime="text/plain"
        )