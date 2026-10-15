import os
from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq

from agents.sales_agent import sales_app
from agents.finance_agent import finance_app
from agents.hr_agent import hr_app
from agents.procurement_agent import procurement_app
from agents.inventory_agent import inventory_app
from langchain_core.messages import HumanMessage,SystemMessage

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)


SYSTEM_PROMPT = """
You are the Supervisor Agent for an enterprise AI assistant.

Your job is to classify the user's request into exactly ONE of these domains:

- sales
- finance
- hr
- procurement
- inventory

Return ONLY the domain name.

Examples:

"What are our total sales?"
sales

"Show me invoice payment status"
finance

"Show employee 10 attendance"
hr

"Who supplies product 37?"
procurement

"Which products are low in stock?"
inventory
"""


def supervisor(query):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)

    return response.content
