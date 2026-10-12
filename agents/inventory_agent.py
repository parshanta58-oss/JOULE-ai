import os
from dotenv import load_dotenv
load_dotenv()
from tools.authorization import check_user_permission
from tools.authentication import authenticate_user

from tools.inventory_tool import (
    get_low_stock_products,
    get_warehouse_inventory,
    get_product_inventory,
    get_inventory_summary_by_warehouse,
    get_inventory_by_category,
    
)

from tools.action_tools import (
    create_replenishment_request,
    get_pending_replenishment_requests,
    request_human_review,

)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from rag.rag_tool import search_company_documents
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

tools = [
    get_low_stock_products,
    get_warehouse_inventory,
    get_product_inventory,
    get_inventory_summary_by_warehouse,
    get_inventory_by_category,
    search_company_documents,
    create_replenishment_request,
    request_human_review,
    get_pending_replenishment_requests,
]

llm=ChatGroq(
    model="openai/gpt-oss-120b", api_key=""
)

llm_with_tools = llm.bind_tools(tools)


class InventoryPipeline(TypedDict):
    messages: Annotated[list, add_messages]


def inventory_agent(state: InventoryPipeline):
    system_message = """
    You are an Inventory Agent for an enterprise AI system.

    Use SQL tools when the user asks about structured inventory data such as:
    - inventory quantities
    - low-stock products
    - warehouse inventory
    - product inventory
    - inventory by category
    - warehouse summaries

    Use the company document search tool when the user asks about:
    - inventory management procedures
    - stock replenishment policies
    - inventory SOPs
    - stock handling rules
    - documented company processes

    Use both SQL tools and the company document search tool when the question requires both structured inventory data and company documentation.

    Always use the appropriate tool instead of guessing.

    Use create_replenishment_request tool only when the user 
    explicitly requests creating a replenishment request.
    Never claim a request was created unless the tool returns success.

    Before creating a request, validate the product ID and ensure the requested quantity is greater than zero.

    Never claim that a replenishment request was created unless the Action Tool returns success: True.

    A newly created replenishment request must remain in PENDING status until reviewed.
    Never claim that a request was approved or rejected unless the review tool confirms the operation succeeded.

    Do not review a request that has already been reviewed.

    Do not invent request IDs, product details, quantities, or tool results.

    The reviewed_by field must not be treated as proof of an authenticated user's identity.
    For approving or rejecting replenishment requests:
    - Never update a request's status directly.
    - Use request_human_review to request human confirmation.
    - Do not claim approval or rejection until the tool confirms success.
    - Never bypass the human-review step.
    """
    messages = [
        {"role": "system", "content": system_message}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


tool_node = ToolNode(tools)


graph = StateGraph(InventoryPipeline)

graph.add_node("inventory_agent", inventory_agent)
graph.add_node("tools", tool_node)

graph.add_edge(START, "inventory_agent")

graph.add_conditional_edges(
    "inventory_agent",
    tools_condition
)

graph.add_edge(
    "tools",
    "inventory_agent"
)



from langgraph.types import Command

DB_URI = os.getenv("DATABASE_URL")

if not DB_URI:
    raise ValueError("DATABASE_URL is not set in your .env file")

checkpointer_context = PostgresSaver.from_conn_string(DB_URI)
checkpointer = checkpointer_context.__enter__()

checkpointer.setup()

inventory_app = graph.compile(checkpointer=checkpointer)

# Keep the same thread ID to resume the interrupted workflow.
thread_id = "inventory-review-test-001"

config = {
    "configurable": {
        "thread_id": thread_id
    }
}

mode = input("Enter mode (new/resume): ").strip().lower()

if mode == "new":
    query = input("Enter your query: ")

    response = inventory_app.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config
    )



elif mode == "resume":
    confirmation = input(
        "Confirm the pending action? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        reviewer = input("Enter reviewer username: ").strip()

        # Step 1: Verify the user's password.
        password = input("Enter password: ")

        auth_result = authenticate_user(reviewer, password)

        if not auth_result["authenticated"]:
            print("Authentication failed:", auth_result["message"])
            raise SystemExit(1)

        # Step 2: Check the verified user's role.
        permission = check_user_permission(
            auth_result["username"],
            "INVENTORY_MANAGER"
        )

        if not permission["authorized"]:
            print("Authorization denied:", permission["message"])
            raise SystemExit(1)

        # Step 3: Resume using the verified identity.
        resume_value = {
            "confirmed": True,
            "reviewed_by": auth_result["username"]
        }

    else:
        resume_value = {"confirmed": False}

    response = inventory_app.invoke(
        Command(resume=resume_value),
        config=config
    )


else:
    print("Invalid mode. Enter 'new' or 'resume'.")
    raise SystemExit(1)


interrupts = response.get("__interrupt__", ())

if interrupts:
    review_details = interrupts[0].value

    print("\n--- HUMAN REVIEW REQUIRED ---")
    print(review_details["message"])
    print(
        "\nWorkflow is paused. Restart the program "
        "and choose 'resume' to continue."
    )
else:
    print("\n--- AGENT RESPONSE ---")
    print(response["messages"][-1].content)

