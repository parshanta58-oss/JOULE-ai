from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from agents.supervisor import supervisor
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from agents.sales_agent import sales_app
from agents.finance_agent import finance_app
from agents.hr_agent import hr_app
from agents.procurement_agent import procurement_app
from agents.inventory_agent import inventory_app

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str


def supervisor_node(state: SupervisorState):
    query = state["messages"][-1].content

    decision = supervisor(query)

    return {
        "next_agent": decision
    }

def route_to_agent(state: SupervisorState):
    return state["next_agent"]

def run_sales(state: SupervisorState):
    response = sales_app.invoke({
        "messages": state["messages"]
    })
    return {
        "messages": response["messages"][-1:]
    }


def run_finance(state: SupervisorState):
    response = finance_app.invoke({
        "messages": state["messages"]
    })
    return {
        "messages": response["messages"][-1:]
    }


def run_hr(state: SupervisorState):
    response = hr_app.invoke({
        "messages": state["messages"]
    })
    return {
        "messages": response["messages"][-1:]
    }


def run_procurement(state: SupervisorState):
    response = procurement_app.invoke({
        "messages": state["messages"]
    })
    return {
        "messages": response["messages"][-1:]
    }


def run_inventory(state: SupervisorState):
    response = inventory_app.invoke({
        "messages": state["messages"]
    })
    return {
        "messages": response["messages"][-1:]
    }

graph = StateGraph(SupervisorState)

graph.add_node("supervisor", supervisor_node)

graph.add_node("sales", run_sales)
graph.add_node("finance", run_finance)
graph.add_node("hr", run_hr)
graph.add_node("procurement", run_procurement)
graph.add_node("inventory", run_inventory)

graph.add_edge(START, "supervisor")


graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "sales": "sales",
        "finance": "finance",
        "hr": "hr",
        "procurement": "procurement",
        "inventory": "inventory",
    }
)

graph.add_edge("sales", END)
graph.add_edge("finance", END)
graph.add_edge("hr", END)
graph.add_edge("procurement", END)
graph.add_edge("inventory", END)


app = graph.compile()

query = input("Enter your query: ")

response = app.invoke(
    {
        "messages": [
            HumanMessage(content=query)
        ]
    }
)

print("\nFinal Answer:")
print(response["messages"][-1].content)