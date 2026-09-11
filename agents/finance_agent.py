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

tools = [
    get_total_expenses,
    get_department_expenses,
    get_payment_summary,
    get_invoice_status,
    get_department_budgets
]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)

class FinancePipeline(TypedDict):
    messages: Annotated[list, add_messages]

def finance_agent(state: FinancePipeline):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }

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

app = graph.compile()


input_text = input("Enter your finance query: ")

response = app.invoke({
    "messages": [
        HumanMessage(content=input_text)
    ]
})

print(response["messages"][-1].content)


