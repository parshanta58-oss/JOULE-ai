import os
from dotenv import load_dotenv

load_dotenv()

from tools.finance_tool import (get_total_expenses,
                                get_department_expenses,
                                get_department_budgets,
                                get_invoice_status,
                                get_payment_summary)

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from rag.rag_tool import search_company_documents

tools = [
    get_total_expenses,
    get_department_expenses,
    get_payment_summary,
    get_invoice_status,
    get_department_budgets,
    search_company_documents
]

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

llm_with_tools = llm.bind_tools(tools)

class FinancePipeline(TypedDict):
    messages: Annotated[list, add_messages]

def finance_agent(state: FinancePipeline):
    system_message = """
    You are a Finance Agent for an enterprise AI system.

    Use SQL tools when the user asks about structured financial data such as:
    - expenses
    - department expenses
    - budgets
    - invoices
    - payments
    - financial summaries

    Use the company document search tool when the user asks about:
    - expense policies
    - invoice policies
    - payment policies
    - financial procedures
    - approval rules
    - documented company processes

    Use both SQL tools and the company document search tool when the question requires both structured financial data and company documentation.

    Always use the appropriate tool instead of guessing.
    """

    messages = [
        {"role": "system", "content": system_message}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

tool_node = ToolNode(tools)

graph = StateGraph(FinancePipeline)

graph.add_node("finance_agent", finance_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "finance_agent")

graph.add_conditional_edges(
    "finance_agent",
    tools_condition
)

graph.add_edge("tools", "finance_agent")

finance_app = graph.compile()

""" 
query=input("enter a query :")

response=finance_app.invoke(
    {"messages":[query]}
)

print(response["messages"][-1].content)
 """
