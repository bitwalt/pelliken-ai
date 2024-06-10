import asyncio

import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

from chat import utils
from chat.streaming import StreamHandler
from lightning.utils import handle_payment


class ContextChatbot:
    def __init__(self):
        self.openai_model = utils.configure_openai()
        self.ln_processor = st.session_state.get("ln_processor", None)

    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        llm = ChatOpenAI(model_name=_self.openai_model, temperature=0, streaming=True)
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain

    @utils.enable_chat_history
    async def main(self, prompt_model):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, "user")
            with st.chat_message("assistant"):
                if self.ln_processor:
                    cfg = {"mode": "chat"}
                    payment_received = await handle_payment(self.ln_processor, cfg)
                    if payment_received:
                        st.balloons()

                        st_cb = StreamHandler(st.empty())
                        result = chain.invoke(
                            {"input": user_query}, {"callbacks": [st_cb]}
                        )
                        response = result["response"]
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
