from agents.sales_agent import sales_app
from langchain_core.messages import HumanMessage


query = "What are the total sales?"

response = sales_app.invoke(
    {
        "messages": [
            HumanMessage(content=query)
        ]
    }
)

print(response["messages"][-1].content)