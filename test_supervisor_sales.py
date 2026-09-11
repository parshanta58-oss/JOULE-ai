from agents.supervisor import supervisor
from agents.sales_agent import sales_app
from langchain_core.messages import HumanMessage


query = "What are the total sales?"

decision = supervisor(query)

print("Supervisor decision:", decision)

if decision == "sales":
    response = sales_app.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        }
    )

    print("\nFinal Answer:")
    print(response["messages"][-1].content)