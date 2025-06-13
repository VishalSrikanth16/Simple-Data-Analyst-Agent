import streamlit as st
from file_loader import *
from llama_agent import ask_llama
from visualizer import visualize
import tempfile
import os

st.set_page_config(page_title="🧠 Data Analyst Agent", layout="centered")

st.title("📊 AI-Powered Data Analyst Agent")

uploaded_file = st.file_uploader("Upload a data or document file", type=["csv", "xlsx", "xls", "pdf", "docx", "txt", "jpg", "jpeg", "png"])

if uploaded_file:
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        path = tmp_file.name

    filetype_detected = detect_file_type(path)
    st.info(f"Detected file type: `{filetype_detected}`")

    if filetype_detected in ["csv", "excel"]:
        df = extract_table(path)
        if df is not None:
            st.dataframe(df.head())
            user_q = st.text_input("💬 Ask a question about this data:")
            if user_q:
                prompt = f"Here is a table:\n{df.head(10).to_string()}\n\nUser question: {user_q}"
                with st.spinner("Getting answer from LLaMA..."):
                    result = ask_llama(prompt)
                st.success("Answer from LLaMA:")
                st.markdown(result)

            st.subheader("📈 Visualize Data")
            if st.checkbox("Show chart builder"):
                chart_type = st.selectbox("Chart type", ["bar", "line", "scatter"])
                x = st.selectbox("X-axis", df.columns)
                y = st.selectbox("Y-axis", df.columns)
                if st.button("Generate Chart"):
                    st.pyplot(visualize(df, chart_type=chart_type, x=x, y=y))

    elif filetype_detected == "pdf":
        content = extract_text_from_pdf(path)
    elif filetype_detected == "docx":
        content = extract_text_from_docx(path)
    elif filetype_detected == "txt":
        content = extract_text_from_txt(path)
    elif filetype_detected == "image":
        content = extract_text_from_image(path)
    else:
        st.error("Unsupported file type.")
        st.stop()

    if filetype_detected in ["pdf", "docx", "txt", "image"]:
        st.text_area("📄 Extracted Content", value=content[:1500], height=250)
        user_q = st.text_input("💬 Ask a question about this content:")
        if user_q:
            prompt = f"Content:\n{content[:1000]}\n\nUser question: {user_q}"
            with st.spinner("Thinking..."):
                result = ask_llama(prompt)
            st.success("Answer from LLaMA:")
            st.markdown(result)
