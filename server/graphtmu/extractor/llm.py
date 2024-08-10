from typing import List

from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import RootModel
from pydantic.dataclasses import dataclass

# https://python.langchain.com/v0.2/docs/how_to/chat_model_caching
set_llm_cache(SQLiteCache(database_path="graphtmu.langchain.db"))


@dataclass
class KeywordsOutput:
    keywords: List[str]


# https://python.langchain.com/v0.2/docs/how_to/structured_output
def get_keywords(text: str, model="gpt-4o-2024-08-06") -> KeywordsOutput:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            "Your task is to extract a list of keywords from a provided block of text "
            "and output it in JSON List format."
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ])
    llm = ChatOpenAI(model=model).with_structured_output(
        schema=KeywordsOutput,
        strict=True,
    )
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return RootModel[KeywordsOutput].model_validate(result).root


def get_embeddings(
    texts: List[str], model="text-embedding-3-small", dimensions=512
) -> List[List[float]]:
    llm = OpenAIEmbeddings(model=model, dimensions=dimensions)
    result = llm.embed_documents(texts)
    return result
