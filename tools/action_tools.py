from langchain_core.tools import tool
from tools.database import get_connection
from langgraph.types import interrupt

@tool
def create_replenishment_request(product_id: int, quantity: int):
    """
    Create a pending replenishment request for a product.
    """

    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than 0."
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_id, product_name
        FROM products
        WHERE product_id = %s
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        conn.close()

        return {
            "success": False,
            "message": f"Product {product_id} does not exist."
        }


    cursor.execute(
        """
        INSERT INTO replenishment_requests
            (product_id, quantity)
        VALUES
            (%s, %s)
        RETURNING request_id, status, requested_at
        """,
        (product_id, quantity)
    )

    request = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "success": True,
        "request_id": request[0],
        "product_id": product[0],
        "product_name": product[1],
        "quantity": quantity,
        "status": request[1],
        "requested_at": str(request[2])
    }



@tool
def review_replenishment_request(
    request_id: int,
    decision: str,
    reviewed_by: str
):
    """
    Approve or reject a pending replenishment request.
    """

    # Validate the decision
    decision = decision.strip().upper()

    if decision not in ["APPROVED", "REJECTED"]:
        return {
            "success": False,
            "message": "Decision must be APPROVED or REJECTED."
        }

    if request_id <= 0:
        return {
            "success": False,
            "message": "Request ID must be greater than 0."
        }

    if not reviewed_by.strip():
        return {
            "success": False,
            "message": "Reviewer name cannot be empty."
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE replenishment_requests
            SET status = %s,
                reviewed_by = %s,
                reviewed_at = CURRENT_TIMESTAMP
            WHERE request_id = %s
              AND status = 'PENDING'
            RETURNING request_id, status, reviewed_by, reviewed_at
            """,
            (decision, reviewed_by.strip(), request_id)
        )

        result = cursor.fetchone()

        if result is None:
            conn.rollback()
            return {
                "success": False,
                "message": (
                    "Request not found or it has already been reviewed."
                )
            }

        conn.commit()

        return {
            "success": True,
            "request_id": result[0],
            "status": result[1],
            "reviewed_by": result[2],
            "reviewed_at": str(result[3])
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()




@tool
def get_pending_replenishment_requests():
    """
    Retrieve all replenishment requests awaiting review.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                rr.request_id,
                rr.product_id,
                p.product_name,
                rr.quantity,
                rr.status,
                rr.requested_at
            FROM replenishment_requests rr
            JOIN products p
                ON rr.product_id = p.product_id
            WHERE rr.status = 'PENDING'
            ORDER BY rr.requested_at DESC
            """
        )

        rows = cursor.fetchall()

        requests = []

        for row in rows:
            requests.append({
                "request_id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "quantity": row[3],
                "status": row[4],
                "requested_at": str(row[5])
            })

        return {
            "success": True,
            "count": len(requests),
            "requests": requests
        }

    except Exception:
        raise

    finally:
        cursor.close()
        conn.close()



""" result = get_pending_replenishment_requests.invoke({})

print(result) """


""" 
print("\n--- Test 1: Approve request ---")
result = review_replenishment_request.invoke({
    "request_id": 2,
    "decision": "APPROVED",
    "reviewed_by": "admin"
})
print(result)

print("\n--- Test 2: Invalid decision ---")
result = review_replenishment_request.invoke({
    "request_id": 2,
    "decision": "MAYBE",
    "reviewed_by": "admin"
})
print(result)

print("\n--- Test 3: Review the same request again ---")
result = review_replenishment_request.invoke({
    "request_id": 2,
    "decision": "REJECTED",
    "reviewed_by": "admin"
})
print(result)
 """



@tool
def request_human_review(request_id: int, decision: str):
    """
    Pause the workflow and request explicit human confirmation
    before approving or rejecting a replenishment request.
    """

    decision = decision.strip().upper()

    if decision not in ["APPROVED", "REJECTED"]:
        return {
            "success": False,
            "message": "Decision must be APPROVED or REJECTED."
        }

    # Pause the LangGraph workflow until a human responds.
    human_response = interrupt({
        "type": "replenishment_review",
        "request_id": request_id,
        "decision": decision,
        "message": (
            f"Confirm {decision.lower()} for replenishment "
            f"request {request_id}."
        )
    })

    # Require an explicit confirmation after resuming.
    if (
        not isinstance(human_response, dict)
        or human_response.get("confirmed") is not True
    ):
        return {
            "success": False,
            "message": "Human confirmation was not provided."
        }

    reviewed_by = human_response.get("reviewed_by", "").strip()

    if not reviewed_by:
        return {
            "success": False,
            "message": "Reviewer name is required."
        }

    
    return review_replenishment_request.invoke({
        "request_id": request_id,
        "decision": decision,
        "reviewed_by": reviewed_by
    })
