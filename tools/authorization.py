
from tools.database import get_connection


def check_user_permission(username: str, required_role: str) -> dict:
    """
    Check whether a registered user has the required role.
    """

    if not username or not username.strip():
        return {
            "authorized": False,
            "message": "Username is required."
        }

    allowed_roles = {
        "ADMIN",
        "INVENTORY_MANAGER",
        "EMPLOYEE"
    }

    required_role = required_role.strip().upper()

    if required_role not in allowed_roles:
        return {
            "authorized": False,
            "message": "Invalid role requested."
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT role
            FROM app_users
            WHERE username = %s
            """,
            (username.strip(),)
        )

        result = cursor.fetchone()

        if result is None:
            return {
                "authorized": False,
                "message": "User does not exist."
            }

        user_role = result[0]

        if user_role not in {"ADMIN", required_role}:
            return {
                "authorized": False,
                "message": "User does not have the required permission."
            }

        return {
            "authorized": True,
            "username": username.strip(),
            "role": user_role,
            "message": "Permission granted."
        }

    finally:
        cursor.close()
        conn.close()



""" 

### TESTING #####

print(
    check_user_permission(
        "prashanth_test",
        "INVENTORY_MANAGER"
    )
)

print(
    check_user_permission(
        "unknown_user",
        "INVENTORY_MANAGER"
    )
)
 """