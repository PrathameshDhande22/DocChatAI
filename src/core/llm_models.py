import os
from typing import Literal

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain.chat_models import BaseChatModel


def getLLMModel(provider: Literal["HuggingFace", "Google"]) -> BaseChatModel:
    match provider:
        case "Google":
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                },
                temperature=0.2,
                max_retries=3,
                thinking_budget=1000,
                include_thoughts=True,
            )
        case "HuggingFace":
            huggingfacepipline = HuggingFacePipeline.from_model_id(
                model_id="Qwen/Qwen3-0.6B", task="text-generation"
            )
            return ChatHuggingFace(llm=huggingfacepipline, verbose=True, temperture=0.7)
        case _:
            raise Exception("Implement the Provider First")
