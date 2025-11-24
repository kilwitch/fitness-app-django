# home/chatbot.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


# Keep only last 4 messages for faster inference
class LimitedHistory(InMemoryChatMessageHistory):
    def add_message(self, message):
        super().add_message(message)
        self.messages = self.messages[-4:]  

store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = LimitedHistory()
    return store[session_id]


# ---------- FASTER MODEL ----------
llm = ChatOllama(
    model="gemma2:2b",  
    temperature=0.4,
    num_predict=180,              
)

# ---------- IMPROVED PROMPT ----------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a fitness assistant. Respond in short, simple sentences. "
     "Do NOT use markdown. No bold, no bullets, no emojis."),
    ("user", "{question}")
])

# pipeline
chain = prompt | llm | StrOutputParser()

# chatbot with memory
chatbot = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="question",
    history_messages_key="history",
)
