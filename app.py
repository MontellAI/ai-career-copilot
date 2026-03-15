import streamlit as st
from rag.chain import CareerCopilotChain
from utils.skill_analyzer import SkillAnalyzer

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 AI Career Copilot")
st.caption("LLM-powered career guidance — grounded in real job market data, not hallucinations.")

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio("", ["Overview", "Career Paths", "Skills to Learn", "Job Market", "Roadmap"])

# Main input form
with st.form("profile_form"):
    st.subheader("Your Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        goal = st.text_input("Target Role", placeholder="e.g. AI/ML Engineer, LLM Engineer")
        experience = st.selectbox("Experience Level", ["Student", "0-2 years", "2-5 years", "5+ years"])
    
    with col2:
        current_skills = st.text_area("Current Skills", placeholder="Python, SQL, some ML basics...")
        interests = st.text_area("Interests / Focus Areas", placeholder="RAG, agents, fine-tuning...")
    
    submitted = st.form_submit_button("Analyze & Generate Roadmap")

if submitted:
    with st.spinner("Retrieving relevant context and generating your roadmap..."):
        chain = CareerCopilotChain()
        analyzer = SkillAnalyzer()
        
        user_profile = {
            "goal": goal,
            "experience": experience,
            "skills": current_skills,
            "interests": interests
        }
        
        result = chain.run(user_profile)
        skill_gaps = analyzer.analyze(current_skills, goal)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Skill Gap Analysis")
            for skill, score in skill_gaps.items():
                st.progress(score / 100, text=f"{skill}: {score}%")
        
        with col2:
            st.subheader("Recommended Roadmap")
            st.markdown(result["roadmap"])
        
        st.subheader("Career Path Recommendation")
        st.markdown(result["career_advice"])
        
        with st.expander("Retrieved Context (Sources)"):
            for doc in result["source_documents"]:
                st.markdown(f"**Source:** {doc.metadata.get('source', 'Knowledge Base')}")
                st.markdown(doc.page_content[:300] + "...")
                st.divider()
