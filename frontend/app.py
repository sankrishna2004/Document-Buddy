import streamlit as st
import requests

st.title("PDF Question Answering App")

file = st.file_uploader("PDF File", type="pdf")

if st.button("Upload file") and file is not None:
    files = {'file': file}
    response = requests.post("http://localhost:8000/upload", files=files)

    if response.status_code == 200:
        data = response.json()
        hash_id = data.get("pdf_id")
        message = data.get("message", "Upload successful.")

        st.session_state.file_uploaded = True
        st.session_state.pdf_id = hash_id

        st.success(message)  # ✅ Use message from JSON response
        st.write(f"PDF ID: {hash_id}")
    else:
        st.error("File upload failed")

if st.session_state.get("file_uploaded", False):
    question = st.text_input("Ask a question about the PDF")
    if st.button("Get Answer") and question:
        response = requests.post(
            "http://localhost:8000/query",
            data={"question": question, "hash_id": st.session_state.pdf_id},
            stream=True
        )
        if response.status_code == 200:
            output_placeholder = st.empty()
            full_response = ""

            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    full_response += chunk
                    output_placeholder.write(full_response)
        else:
            st.error("Failed to get answer")
