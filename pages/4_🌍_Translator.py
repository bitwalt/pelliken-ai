import asyncio

import streamlit as st

from chat.basic_chatbot import handle_chat
from chat.utils import load_prompt_models, setup_prompt_model_selection
from utils import init_page


def main():
    init_page(image_page=False)
    st.title("🌍 Translator")
    st.text("Translate text from one language to another using ChatGPT")

    # Prompt Selection
    prompt_models = load_prompt_models()
    prompt_model = prompt_models["🌍 Translator"]

    handle_chat(prompt_model)


if __name__ == "__main__":
    main()