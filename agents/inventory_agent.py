import os
from dotenv import load_dotenv

load_dotenv()

from tools.inventory_tool import (
    get_low_stock_products,
    get_warehouse_inventory,
    get_product_inventory,
    get_inventory_summary_by_warehouse,
    get_inventory_by_category,
    
)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from rag.rag_tool import search_company_documents

tools = [
    get_low_stock_products,
    get_warehouse_inventory,
    get_product_inventory,
    get_inventory_summary_by_warehouse,
    get_inventory_by_category,
    search_company_documents
]

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

llm_with_tools = llm.bind_tools(tools)


class InventoryPipeline(TypedDict):
    messages: Annotated[list, add_messages]


def inventory_agent(state: InventoryPipeline):
    system_message = """
    You are an Inventory Agent for an enterprise AI system.

    Use SQL tools when the user asks about structured inventory data such as:
    - inventory quantities
    - low-stock products
    - warehouse inventory
    - product inventory
    - inventory by category
    - warehouse summaries

    Use the company document search tool when the user asks about:
    - inventory management procedures
    - stock replenishment policies
    - inventory SOPs
    - stock handling rules
    - documented company processes

    Use both SQL tools and the company document search tool when the question requires both structured inventory data and company documentation.

    Always use the appropriate tool instead of guessing.
    """
    messages = [
        {"role": "system", "content": system_message}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


tool_node = ToolNode(tools)


graph = StateGraph(InventoryPipeline)

graph.add_node("inventory_agent", inventory_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "inventory_agent")

graph.add_conditional_edges(
    "inventory_agent",
    tools_condition
)

graph.add_edge(
    "tools",
    "inventory_agent"
)



inventory_app = graph.compile()

query=input("Enter your query :")

response=inventory_app.invoke(
    {"messages":[query]}
)

print(response["messages"][-1].content)

