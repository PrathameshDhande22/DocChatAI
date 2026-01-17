from functools import lru_cache
import os
from typing import Literal

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain.chat_models import BaseChatModel
from langchain_mistralai import ChatMistralAI

type Providers = Literal[
    "Gemini 2.5 Flash", "Qwen 3", "Mistral Large 3", "GPT OSS 120b"
]


@lru_cache(maxsize=10)
def getLLMModel(provider: Providers) -> BaseChatModel:
    match provider:
        case "Gemini 2.5 Flash":
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                },
                temperature=0.2,
                max_retries=3,
                thinking_budget=0,
            )
        case "Qwen 3":
            huggingfacepipline = HuggingFacePipeline.from_model_id(
                model_id="Qwen/Qwen3-0.6B", task="text-generation"
            )
            return ChatHuggingFace(llm=huggingfacepipline, verbose=True, temperture=0.7)
        case "Mistral Large 3":
            return ChatMistralAI(
                model_name="mistral-large-2512",
                temperature=0.2,
                api_key=os.getenv("MISTRAL_API_KEY"),
                max_retries=3,
            )
        case "GPT OSS 120b":
            return ChatGroq(
                model="openai/gpt-oss-120b",
                api_key=os.getenv("GROQ_API_KEY"),
                max_retries=3,
                temperature=0.2,
            )
        case _:
            raise Exception("Implement the Provider First")
