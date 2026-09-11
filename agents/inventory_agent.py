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


tools = [
    get_low_stock_products,
    get_warehouse_inventory,
    get_product_inventory,
    get_inventory_summary_by_warehouse,
    get_inventory_by_category,
]

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

llm_with_tools = llm.bind_tools(tools)


class InventoryPipeline(TypedDict):
    messages: Annotated[list, add_messages]


def inventory_agent(state: InventoryPipeline):
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


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

