import os
from dotenv import load_dotenv

load_dotenv()

from tools.hr_tool import (
    get_employee_details,
    get_employee_attendance,
    get_employee_leaves,
    get_department_employees,
    get_employee_count_by_department,
)

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated


""" tools = [
    get_employee_details,
    get_employee_attendance,
    get_employee_leaves,
    get_department_employees,
    get_employee_count_by_department,
] """

tools = [
   
    get_employee_attendance,
    get_employee_count_by_department,
    get_department_employees,
    get_employee_details,
    get_employee_leaves
]


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)


class HRPipeline(TypedDict):
    messages: Annotated[list, add_messages]

def hr_agent(state: HRPipeline):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

tool_node = ToolNode(tools)

graph = StateGraph(HRPipeline)

graph.add_node("hr_agent", hr_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "hr_agent")

graph.add_conditional_edges(
    "hr_agent",
    tools_condition
)

graph.add_edge("tools", "hr_agent")

app = graph.compile()

input_text = input("Enter your HR query: ")

response = app.invoke({
    "messages": [
        HumanMessage(content=input_text)
    ]
})

print(response["messages"][-1].content)