import streamlit as st
import requests

st.set_page_config(page_title="AI Receipt Analyzer", page_icon="🧾")

st.title("📸 AI Receipt Analyzer")
st.write("Powered by Groq LPU™ Inference")

uploaded_file = st.file_uploader("Upload a receipt (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Receipt Preview", width=300)
    
    if st.button("Analyze Receipt"):
        with st.spinner("AI is thinking at light speed..."):
            # Prepare file for API
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            # Send to FastAPI backend
            try:
                response = requests.post("http://127.0.0.1:8000/process", files=files, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    
                    # Display results nicely
                    col1, col2 = st.columns(2)
                    col1.metric("Merchant", data.get("merchant"))
                    col2.metric("Total", f"{data.get('currency')} {data.get('total')}")
                    
                    st.json(data)
                else:
                    st.error("Error: Backend is not responding.")
            except Exception as e:
                st.error(f"Connection Error: {e}")