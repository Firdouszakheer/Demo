import streamlit as st
import os

from parser import read_pdf, read_docx, read_pptx
from utils import chunk_text
from retriever import create_vector_store, search
from llm import ask_llm
from storage import save_index, load_index

st.set_page_config(page_title="DocBrain", layout="wide")

# 🎨 Neon Style
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.stButton>button {
    background-color: #00ffff;
    color: black;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 DocBrain Pro")

# 📂 MULTI FILE UPLOAD
files = st.file_uploader("Upload Documents", type=["pdf","docx","pptx"], accept_multiple_files=True)

# LOAD SAVED INDEX
index, chunks = load_index()

if files:
    all_text = ""

    for file in files:
        if file.name.endswith(".pdf"):
            all_text += read_pdf(file)
        elif file.name.endswith(".docx"):
            all_text += read_docx(file)
        else:
            all_text += read_pptx(file)

    chunks = chunk_text(all_text)
    index = create_vector_store(chunks)

    save_index(index, chunks)

    st.success("Documents processed & saved!")

# TABS
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Summary", "📝 Quiz"])

# 💬 CHAT
with tab1:
    query = st.text_input("Ask your documents")

    if query and index:
        results = search(query, index, chunks)
        context = "\n".join(results)

        answer = ask_llm(context, query)

        st.write("### 🤖 Answer")
        st.write(answer)

# 📄 SUMMARY
with tab2:
    if st.button("Generate Summary") and chunks:
        text = " ".join(chunks[:20])
        st.write(ask_llm(text, task="summary"))

# 📝 QUIZ (INTERACTIVE)
with tab3:
    if st.button("Generate Quiz") and chunks:
        quiz_text = ask_llm(" ".join(chunks[:20]), task="quiz")

        questions = quiz_text.split("Q")[1:]

        score = 0

        for i, q in enumerate(questions):
            parts = q.split("\n")
            question = parts[0]

            options = parts[1:5]
            answer = parts[-1].replace("Answer:", "").strip()

            user_ans = st.radio(f"Q{i+1}: {question}", options, key=i)

            if st.button(f"Check {i}"):
                if answer in user_ans:
                    st.success("Correct!")
                    score += 1
                else:
                    st.error(f"Wrong! Correct: {answer}")

        st.write(f"Score: {score}/5")