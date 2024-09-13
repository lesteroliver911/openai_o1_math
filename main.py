import streamlit as st
from openai import OpenAI

def load_custom_css():
    with open("style.css", "r") as css_file:
        st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)

def create_user_interface():
    st.title("∑ MathSolver")
    st.write("Welcome to **MathSolver**! Enter your OpenAI API key, select a model, and input your math query below.")
    api_key = st.text_input("🔑 OpenAI API Key", type="password")
    model_options = ["o1-mini", "o1-preview"]
    selected_model = st.selectbox("🧠 Select Model", model_options)
    query = st.text_area("✍️ Math Query", height=150)
    return api_key, query, selected_model

def process_query(api_key, query, model):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": query}],
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def show_result(result):
    st.markdown("### 📚 Solution:")
    if "```" in result:
        st.markdown(result)
    else:
        st.write(result)

def run_math_solver():
    st.set_page_config(page_title="MathSolver with Openai O1 Models", page_icon="∑")
    load_custom_css()
    
    api_key, query, model = create_user_interface()
    
    if st.button("Solve ➤"):
        if not api_key.strip():
            st.warning("Please enter your OpenAI API key.")
        elif not query.strip():
            st.warning("Please enter a math query.")
        else:
            with st.spinner('Calculating...'):
                solution = process_query(api_key, query, model)
                if solution:
                    show_result(solution)

if __name__ == "__main__":
    run_math_solver()