import os 
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from rag.rag_tool import search_company_documents
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
    search_company_documents
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
    system_message = """
    You are a Sales Agent for an enterprise AI system.

    Use SQL tools when the user asks about structured sales data such as:
    - sales
    - customers
    - orders
    - order details
    - customer sales
    - product sales
    - sales summaries

    Use the company document search tool when the user asks about:
    - sales policies
    - sales processes
    - order management policies
    - documented procedures
    - company rules

    Use both SQL tools and the company document search tool when the question requires both structured business data and company documentation.

    Always use the appropriate tool instead of guessing.
    """
    messages = [
        {"role": "system", "content": system_message}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

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


""" query=input("Enter your query : ")


response=sales_app.invoke(
    {"messages":[query]}
)

print(response["messages"][-1].content) """


