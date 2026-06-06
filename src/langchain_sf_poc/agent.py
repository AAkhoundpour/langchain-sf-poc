from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from langchain_sf_poc.agent_logger import AgentDebugLogger
from langchain_sf_poc.config import settings
from langchain_sf_poc.tools import tools


def build_agent():
    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a Salesforce assistant. "
            "Use the available tools when you need Salesforce data. "
            "Do not make up Salesforce records."
        ),
    )


def ask_agent(user_prompt: str):
    agent = build_agent()

    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_prompt}]},
        config={
            "callbacks": [AgentDebugLogger()],
            "recursion_limit": 10,
        },
    )

    return result
