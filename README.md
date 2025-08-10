

# Smart-Career-Recommendation-System

# 🎯 Smart Career Recommendation System (AI + Skills & Interests)

A Streamlit-based AI application that recommends personalized career paths for students and professionals based on their **skills, interests, and live job market trends**.  
It also generates **skill gap analysis** and a **learning roadmap** to help users upskill effectively.

---

## 🚀 Features
- **Resume Parsing** – Extract skills & keywords from PDF/DOCX resumes  
- **Interests Survey** – Understand user preferences & passions  
- **AI Recommendations** – Suggest best-fit career paths with demand score  
- **Skill Gap Analysis** – Highlight missing skills for chosen career  
- **Dynamic Roadmap** – AI-generated 3–6 month upskilling plan with free resources  
- **Live Job Trends** – Integrates job market data for relevance  
- **Gamified Progress Tracker** – Visual milestones & badges

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **NLP:** spaCy, Sentence Transformers
- **AI:** Google Generative AI / OpenAI API
- **Data:** Job trends APIs (e.g., Google Trends, LinkedIn Jobs)
- **Deployment:** Streamlit Cloud / Google Cloud Run

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/<your-username>/career-reco.git
cd career-reco

# Create virtual environment
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
