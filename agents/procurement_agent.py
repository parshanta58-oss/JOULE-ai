import os
from dotenv import load_dotenv

load_dotenv()

from tools.procurement_tool import (
    get_supplier_details,
    get_supplier_products,
    get_product_supplier,
    get_supplier_product_count,
    get_suppliers_by_country,
)

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
]


# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)


# State
class ProcurementPipeline(TypedDict):
    messages: Annotated[list, add_messages]


# Procurement Agent
def procurement_agent(state: ProcurementPipeline):
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


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
app = graph.compile()


# User input
input_text = input("Enter your Procurement query: ")

response = app.invoke(
    {
        "messages": [
            HumanMessage(content=input_text)
        ]
    }
)

print(response["messages"][-1].content)