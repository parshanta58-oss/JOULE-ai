from agents.supervisor import supervisor
from agents.finance_agent import finance_app
from langchain_core.messages import HumanMessage

query = input("Enter your query: ")

decision = supervisor(query)

print("Supervisor decision:", decision)

if decision == "finance":
    response = finance_app.invoke(
        {"messages": [HumanMessage(content=query)]}
    )

    print("\nFinal Answer:")
    print(response["messages"][-1].content)