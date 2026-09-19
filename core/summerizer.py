from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import httpx

import os 

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
        max_retries=0,
    )


def _safe_llm_call(chain, payload, fallback_text: str):
    try:
        return chain.invoke(payload)
    except httpx.HTTPStatusError as exc:
        if exc.response is not None and exc.response.status_code == 429:
            return fallback_text
        raise


def analyze_transcript(transcript: str) -> dict:
    """Generate all meeting outputs with one Mistral request."""
    llm = get_llm()
    output_parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Analyze the meeting transcript and return only valid JSON with these keys: "
                "title (string, max 8 words), summary (array of concise bullet strings), "
                "action_items (array of strings), key_decisions (array of strings), "
                "open_questions (array of strings). Use empty arrays when none are found.\n"
                "{format_instructions}",
            ),
            ("human", "{text}"),
        ]
    )
    chain = prompt | llm | output_parser
    fallback = {
        "title": "Analysis unavailable",
        "summary": ["Mistral API rate limit exceeded. Please retry later."],
        "action_items": [],
        "key_decisions": [],
        "open_questions": [],
    }

    return _safe_llm_call(
        chain,
        {
            "text": transcript[:50000],
            "format_instructions": output_parser.get_format_instructions(),
        },
        fallback,
    )


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )

    return splitter.split_text(transcript)

def summarize(transcript : str) -> str:
    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages(
        [
        ("system", "Summarize this portion of a meeting transcript concisely."),
        ("human", "{text}"),
    ]
    )

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    try:
        chunk_summaries = [_safe_llm_call(map_chain, {"text": chunk}, "[Skipped due to API rate limit]") for chunk in chunks]
    except httpx.HTTPStatusError as exc:
        if exc.response is not None and exc.response.status_code == 429:
            return "Summary unavailable: Mistral API rate limit exceeded. Please wait a few minutes and retry."
        raise

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are an expert meeting summarizer. Combine these partial summaries "
            "into one final professional meeting summary in bullet points.",
        ),
        ("human", "{text}"),
    ]
    )

    combined_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser()
    )

    try:
        return _safe_llm_call(combined_chain, combined, "Summary unavailable: Mistral API rate limit exceeded. Please wait a few minutes and retry.")
    except httpx.HTTPStatusError as exc:
        if exc.response is not None and exc.response.status_code == 429:
            return "Summary unavailable: Mistral API rate limit exceeded. Please wait a few minutes and retry."
        raise

def generate_title(transcipt : str) -> str:
    llm = get_llm()

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
        ChatPromptTemplate.from_messages([
             (
                "system",
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
        ])
        | llm
        |StrOutputParser()
    )

    try:
        return _safe_llm_call(title_chain, transcipt[:2000], "Title unavailable: Mistral API rate limit exceeded. Please wait a few minutes and retry.")
    except httpx.HTTPStatusError as exc:
        if exc.response is not None and exc.response.status_code == 429:
            return "Title unavailable: Mistral API rate limit exceeded. Please wait a few minutes and retry."
        raise



