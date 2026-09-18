import os
from dotenv import load_dotenv
from rag.rag_tool import search_company_documents
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
    get_employee_leaves,
    search_company_documents
]



llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

llm_with_tools=llm.bind_tools(tools)


class HRPipeline(TypedDict):
    messages: Annotated[list, add_messages]

def hr_agent(state: HRPipeline):

    system_message = """
    You are an HR Agent for an enterprise AI system.

    Use SQL tools when the user asks about structured HR data such as:
    - employees
    - employee details
    - attendance
    - leave records
    - departments
    - employee counts

    Use the company document search tool when the user asks about:
    - leave policies
    - attendance policies
    - HR procedures
    - employee rules
    - documented company processes

    Use both SQL tools and the company document search tool when the question requires both structured HR data and company documentation.

    Always use the appropriate tool instead of guessing.
    """
    messages=[
        {"role": "system", "content": system_message}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages":[response]}

tool_node=ToolNode(tools)

graph=StateGraph(HRPipeline)

graph.add_node("hr_agent", hr_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "hr_agent")

graph.add_conditional_edges(
    "hr_agent",
    tools_condition
)

graph.add_edge("tools", "hr_agent")

hr_app= graph.compile()

query=input("Enter your query : ")


response=hr_app.invoke(
    {"messages":[query]}
)

print(response["messages"][-1].content)
