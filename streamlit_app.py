import streamlit as st
import requests

st.set_page_config(page_title="AI Shopping Assistant", layout="wide")
st.title("🛍️ AI Shopping Assistant")
st.markdown("Ask anything about products and get smart recommendations")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
query = st.chat_input("Ask something like 'Best phone under 20000'")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"query": query}
        )

        data = response.json()
        answer = data.get("answer", "")
        products = data.get("results", [])

    except Exception as e:
        answer = "Error connecting to backend"
        products = []

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)

        if products:
            st.markdown("### 🛒 Recommended Products")

            cols = st.columns(3)

            for i, product in enumerate(products[:3]):
                with cols[i]:
                    st.markdown(f"""
                    **{product.get('name', 'N/A')}**

                    💰 Price: ₹{product.get('price', 'N/A')}  
                    📦 Category: {product.get('category', 'N/A')}

                    📝 {product.get('description', '')[:100]}...
                    """)

    st.session_state.messages.append({"role": "assistant", "content": answer})