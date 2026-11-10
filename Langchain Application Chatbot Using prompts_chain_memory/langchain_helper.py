# Yahan LangChain ke 4 components hain: Model, Prompt, Chain, Memory

from groq import Groq
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


def get_models(api_key):
    """Groq se sirf wo chat models laata hai jo aapki key pe chalte hain."""
    ids = [m.id for m in Groq(api_key=api_key).models.list().data]
    # audio, safety aur Arabic-only models list se hata dein
    skip = ("whisper", "tts", "guard", "prompt-", "compound", "orpheus", "allam")
    good = [i for i in ids if not any(s in i for s in skip)]
    return sorted(good, key=lambda i: (not i.startswith("llama"), i))


def create_chain(api_key, model):
    """Chain banata hai jo memory ke sath baat karti hai."""

    # 1) MODEL - Groq ka LLM
    llm = ChatGroq(groq_api_key=api_key, model=model, temperature=0.7)

    # 2) PROMPT - model ko batata hai kaise jawab dena hai
    prompt = PromptTemplate(
        input_variables=["history", "question"],
        template=(
            "Tum ek friendly AI assistant ho. Jawab short aur clear do.\n"
            "Hamesha sirf Roman Urdu ya English mein likho. "
            "Arabic ya Urdu script kabhi mat likho.\n\n"
            "Purani baatein:\n{history}\n\n"
            "User: {question}\n"
            "AI:"
        ),
    )

    # 3) MEMORY - pichli baatein yaad rakhti hai
    memory = ConversationBufferMemory(memory_key="history")

    # 4) CHAIN - model + prompt + memory ko jorta hai
    return LLMChain(llm=llm, prompt=prompt, memory=memory)


def ask(chain, question):
    """Chain se jawab lo."""
    return chain.predict(question=question)


# This langchain code is Updated ,So we use these things.
# Old LangChain	Updated LangChain
# PromptTemplate	ChatPromptTemplate
# LLMChain	Runnable sequence (\|)
# ConversationBufferMemory	InMemoryChatMessageHistory
# chain.predict()	chain.invoke()
# input_variables	Automatically inferred from prompt
# {history} as text	MessagesPlaceholder