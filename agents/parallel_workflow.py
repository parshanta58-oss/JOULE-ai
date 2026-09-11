from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from agents.sales_agent import sales_app
from agents.finance_agent import finance_app
from agents.hr_agent import hr_app
from agents.procurement_agent import procurement_app
from agents.inventory_agent import inventory_app
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

class ParallelState(TypedDict):
    messages: Annotated[list, add_messages]
    sales_result: str
    finance_result: str
    inventory_result: str


def run_sales(state: ParallelState):
    response = sales_app.invoke({
        "messages": state["messages"]
    })

    return {
        "sales_result": response["messages"][-1].content
    }

def run_finance(state: ParallelState):
    response = finance_app.invoke({
        "messages": state["messages"]
    })

    return {
        "finance_result": response["messages"][-1].content
    }

def run_hr(state: ParallelState):
    response = hr_app.invoke({
        "messages": state["messages"]
    })

    return {
        "hr_result": response["messages"][-1].content
    }

def run_procurement(state: ParallelState):
    response = procurement_app.invoke({
        "messages": state["messages"]
    })

    return {
        "procurement_result": response["messages"][-1].content
    }

def run_inventory(state: ParallelState):
    response = inventory_app.invoke({
        "messages": state["messages"]
    })

    return {
        "inventory_result": response["messages"][-1].content
    }


def aggregator(state: ParallelState):
    prompt = f"""
    You are a business report aggregator.

    Combine the results from the five domain agents into one
    clear and concise response.

    SALES:
    {state["sales_result"]}

    FINANCE:
    {state["finance_result"]}

    HR:
    {state["hr_result"]}

    PROCUREMENT:
    {state["procurement_result"]}

    INVENTORY:
    {state["inventory_result"]}

    Provide a unified business summary.
    """

    response = llm.invoke(prompt)

    return {
        "messages": [response]
    }


graph = StateGraph(ParallelState)

graph.add_node("sales", run_sales)
graph.add_node("finance", run_finance)
graph.add_node("hr", run_hr)
graph.add_node("procurement", run_procurement)
graph.add_node("inventory", run_inventory)
graph.add_node("aggregator", aggregator)

graph.add_edge(START, "sales")
graph.add_edge(START, "finance")
graph.add_edge(START, "hr")
graph.add_edge(START, "procurement")
graph.add_edge(START, "inventory")

graph.add_edge("sales", "aggregator")
graph.add_edge("finance", "aggregator")
graph.add_edge("hr", "aggregator")
graph.add_edge("procurement", "aggregator")
graph.add_edge("inventory", "aggregator")

graph.add_edge("aggregator", END)

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

app = graph.compile()