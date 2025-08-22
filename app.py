import streamlit as st
from src.helper import extract_text_from_pdf, ask_gemini
from src.job_api import fetch_linkedin_jobs 

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("AI Job Recommender")
st.markdown("Upload your resume and get job recommendations based on your skills")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_gemini(f"Summarize this resume highlighting skills and education:\n\n{resume_text}")

    with st.spinner("Finding skill gaps..."):
        gaps = ask_gemini(f"Analyze this resume and highlight missing skills and certifications:\n\n{resume_text}")

    with st.spinner("Creating a future roadmap..."):
        roadmap = ask_gemini(f"Suggest a future career roadmap for this resume:\n\n{resume_text}")

    # Display results
    st.header("Resume Summary")
    st.write(summary)

    st.header("Skill Gaps")
    st.write(gaps)

    st.header("Future Roadmap")
    st.write(roadmap)

    if st.button("Get Job Recommendations"):
        with st.spinner("Extracting keywords..."):
            keywords = ask_gemini(f"Suggest best job titles and keywords for:\n\n{summary}")
            search_keywords_clean = keywords.replace("\n", " ").strip()

        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching LinkedIn jobs..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean)

        st.header("Top LinkedIn Jobs")
        if linkedin_jobs:
            for job in linkedin_jobs[:10]:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f"- [View Job]({job.get('link')})")
        else:
            st.warning("No LinkedIn jobs found.")

        st.header("Top Naukri Jobs")
        naukri_jobs = fetch_naukri_jobs(search_keywords_clean)
        if naukri_jobs:
            for job in naukri_jobs[:10]:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f"- [View Job]({job.get('link')})")
        else:
            st.warning("No Naukri jobs found.")
