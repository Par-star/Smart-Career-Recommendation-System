# app.py
import streamlit as st
import io, re, json
import pdfplumber
from docx import Document

st.set_page_config(page_title="Smart Career Reco", layout="centered")
st.title("Smart Career Recommendation (MVP)")

# load careers
with open("careers.json","r",encoding="utf-8") as f:
    careers = json.load(f)

COMMON_SKILLS = sorted(list({s for c in careers for s in c["required_skills"]} | 
                            {"python","java","sql","javascript","react","docker","aws","nlp","data visualization","machine learning","tensorflow","pytorch","excel","communication","statistics"}))

def extract_text_from_pdf_bytes(bts):
    try:
        with pdfplumber.open(io.BytesIO(bts)) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        return "\n".join(pages)
    except Exception as e:
        return bts.decode(errors="ignore")

def extract_text_from_docx_bytes(bts):
    doc = Document(io.BytesIO(bts))
    return "\n".join([p.text for p in doc.paragraphs])

def get_text_and_skills(uploaded_file, manual_text=""):
    text = ""
    skills_found = []
    if uploaded_file:
        bts = uploaded_file.read()
        name = uploaded_file.name.lower()
        if name.endswith(".pdf"):
            text = extract_text_from_pdf_bytes(bts)
        elif name.endswith(".docx") or name.endswith(".doc"):
            text = extract_text_from_docx_bytes(bts)
        else:
            try:
                text = bts.decode()
            except:
                text = ""
    if manual_text:
        text += "\n" + manual_text
    text = text.strip()
    txt_low = text.lower()
    for sk in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(sk.lower()) + r'\b', txt_low):
            skills_found.append(sk)
    return text, list(dict.fromkeys(skills_found))

def recommend_by_overlap(skills, top_k=3, interests=[]):
    picks = []
    for c in careers:
        req = set([s.lower() for s in c.get("required_skills",[])])
        score = len(req & set([s.lower() for s in skills]))
        # interest boost
        for it in interests:
            if it.lower() in c["role"].lower() or it.lower() in c["description"].lower():
                score += 1
        picks.append((score, c))
    picks = sorted(picks, key=lambda x: x[0], reverse=True)
    res = []
    for score, c in picks[:top_k]:
        res.append({
            "role": c["role"],
            "score": int(score),
            "why": c.get("short_reason",""),
            "required_skills": c.get("required_skills",[])
        })
    return res

def simple_roadmap(role, skills):
    top_sk = skills[:3] if skills else ["core skills"]
    m1 = f"Month 1: Fundamentals — Learn {', '.join(top_sk)} basics + 1 small tutorial project."
    m2 = f"Month 2: Intermediate — Build a real mini-project using {top_sk[0]} and showcase on GitHub."
    m3 = f"Month 3: Portfolio & Prep — Polish project, write 1 case-study, start interview Qs."
    return "\n\n".join([m1,m2,m3])

# UI
st.subheader("Upload resume (PDF/DOCX) or paste short text")
uploaded_file = st.file_uploader("Upload resume", type=["pdf","docx","doc","txt"])
manual = st.text_area("Or paste short bio / skills (optional)", height=120)
interests_input = st.text_input("Interests (comma separated, e.g. ai,frontend)", "")

if st.button("Get Recommendations"):
    text, skills = get_text_and_skills(uploaded_file, manual)
    if not text and not skills:
        st.error("Kuch info dalo — resume upload ya skills paste karo.")
    else:
        st.success("Parsed! Skills found: " + (", ".join(skills) if skills else "None"))
        interests = [i.strip() for i in interests_input.split(",") if i.strip()]
        recs = recommend_by_overlap(skills, top_k=3, interests=interests)
        for r in recs:
            st.markdown(f"### {r['role']}  — score {r['score']}")
            st.write(r["why"])
            st.write("Required skills:", ", ".join(r["required_skills"]))
            if st.button(f"Generate simple roadmap for {r['role']}", key=r['role']):
                st.info(simple_roadmap(r['role'], r['required_skills']))
