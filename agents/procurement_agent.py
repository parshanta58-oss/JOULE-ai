import os
from dotenv import load_dotenv
load_dotenv()
from rag.rag_tool import search_company_documents


from tools.procurement_tool import (
    get_supplier_details,
    get_supplier_products,
    get_product_supplier,
    get_supplier_product_count,
    get_suppliers_by_country
    
)

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated


# Procurement tools
tools = [
    get_supplier_details,
    get_supplier_products,
    get_product_supplier,
    get_supplier_product_count,
    get_suppliers_by_country,
    search_company_documents
]


# Gemini LLM
llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

llm_with_tools = llm.bind_tools(tools)


# State
class ProcurementPipeline(TypedDict):
    messages: Annotated[list, add_messages]


# Procurement Agent
def procurement_agent(state: ProcurementPipeline):

    system_message = """
You are a Procurement Agent for an enterprise AI system.

Use SQL tools when the user asks about structured business data such as:
- suppliers
- supplier details
- supplier products
- product suppliers
- supplier counts
- suppliers by country
Use the company document search tool when the user asks about:
- procurement policies
- approval rules
- purchasing procedures
- supplier management policies
- SOPs
- company processes
Use both SQL tools and the company document search tool when the question requires both structured business data and company policy information.
Always use the appropriate tool instead of guessing.
"""

    messages = [
        {"role": "system", "content": system_message}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


# Tool Node
tool_node = ToolNode(tools)


# Build graph
graph = StateGraph(ProcurementPipeline)

graph.add_node("procurement_agent", procurement_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "procurement_agent")

graph.add_conditional_edges(
    "procurement_agent",
    tools_condition
)

graph.add_edge(
    "tools",
    "procurement_agent"
)


# Compile
procurement_app = graph.compile()

query=input("Enter your query :")

response=procurement_app.invoke(
    {
        "messages":[
        HumanMessage(content=query)
        ]
    }
)

print(response["messages"][-1].content)