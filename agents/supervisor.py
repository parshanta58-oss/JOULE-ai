import os
from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq

from agents.sales_agent import sales_app
from agents.finance_agent import finance_app
from agents.hr_agent import hr_app
from agents.procurement_agent import procurement_app
from agents.inventory_agent import inventory_app
from langchain_core.messages import HumanMessage,SystemMessage

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)


SYSTEM_PROMPT = """
You are the Supervisor Agent for an enterprise AI assistant.

Your job is to classify the user's request into exactly ONE of these domains:

- sales
- finance
- hr
- procurement
- inventory

Return ONLY the domain name.

Examples:

"What are our total sales?"
sales

"Show me invoice payment status"
finance

"Show employee 10 attendance"
hr

"Who supplies product 37?"
procurement

"Which products are low in stock?"
inventory
"""


def supervisor(query):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)

    return response.content


query = input("Enter your query: ")

decision = supervisor(query)

print("Supervisor decision:", decision)

if decision == "sales":
    response =sales_app.invoke(
        {"messages": [HumanMessage(content=query)]}
    )

elif decision == "finance":
    response = finance_app.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
elif decision == "hr":
    response = hr_app.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
elif decision == "procurement":
    response = procurement_app.invoke(
        {"messages": [HumanMessage(content=query)]}
)
elif decision == "inventory":
    response = inventory_app.invoke(
        {"messages": [HumanMessage(content=query)]}
)
else:
    print("Agent not connected yet.")
    exit()

print("\nFinal Answer:")
print(response["messages"][-1].content)