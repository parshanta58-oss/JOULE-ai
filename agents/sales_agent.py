import os 
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

from langchain_google_genai import ChatGoogleGenerativeAI

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

from tools.sales_tools import (
    get_sales_summary,
    get_top_customers,
    get_customer_sales,
    get_order_details,
    get_sales_by_product,
    )

tools=[
    get_sales_summary,
    get_top_customers,
    get_customer_sales,
    get_order_details,
    get_sales_by_product,
]

llm_with_tools=llm.bind_tools(tools)

from langgraph.graph import StateGraph ,START ,END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

class SalesPipeline(TypedDict):
    messages: Annotated[list, add_messages]


tool_node = ToolNode(tools)

def sales_agent(state: SalesPipeline):

    print("\n ***** Sales Agent is thinking...*****")

    response = llm_with_tools.invoke(state["messages"])

    if response.tool_calls:
        print(" Tool requested:")
        for tool_call in response.tool_calls:
            print("   →", tool_call["name"], tool_call["args"])
    else:
        print(" ******No tool required. Generating final answer.***** ")

    return {
        "messages": [response]
    }

graph = StateGraph(SalesPipeline)

graph.add_node("sales_agent", sales_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "sales_agent")

graph.add_conditional_edges(
    "sales_agent",
    tools_condition
)

graph.add_edge("tools", "sales_agent")

sales_app = graph.compile()





