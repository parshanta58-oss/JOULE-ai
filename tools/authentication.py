
from pwdlib import PasswordHash
from tools.database import get_connection
""" from getpass import getpass """

password_hasher = PasswordHash.recommended()


def register_user(username: str, password: str) -> dict:
    """Register a user and store only their password hash."""

    username = username.strip()
    """ role = role.strip().upper() """
    role = "EMPLOYEE"

    if not username or not password:
        return {
            "success": False,
            "message": "Username and password are required."
        }

    if len(password) < 12:
        return {
            "success": False,
            "message": "Password must be at least 12 characters."
        }


    password_hash = password_hasher.hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO app_users (username, role, password_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING
            RETURNING user_id, username, role
            """,
            (username, role, password_hash)
        )

        user = cursor.fetchone()

        if user is None:
            conn.rollback()
            return {
                "success": False,
                "message": "Username already exists."
            }

        conn.commit()

        return {
            "success": True,
            "user_id": user[0],
            "username": user[1],
            "role": user[2]
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def authenticate_user(username: str, password: str) -> dict:
    """Verify a user's password against the stored hash."""

    if not username or not password:
        return {
            "authenticated": False,
            "message": "Username and password are required."
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT username, role, password_hash
            FROM app_users
            WHERE username = %s
            """,
            (username.strip(),)
        )

        user = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    if user is None or not user[2]:
        return {
            "authenticated": False,
            "message": "Invalid username or password."
        }

    try:
        password_is_valid = password_hasher.verify(password, user[2])
    except Exception:
        password_is_valid = False

    if not password_is_valid:
        return {
            "authenticated": False,
            "message": "Invalid username or password."
        }

    return {
        "authenticated": True,
        "username": user[0],
        "role": user[1],
        "message": "Authentication successful."
    }

""" 


username = input("Enter your username : ")
password = getpass("Create a test password (minimum 12 characters): ")

result = register_user(
    username=username,
    password=password,
    role="INVENTORY_MANAGER"
)
print("Registration:", result)

if result.get("success"):
    login_password = getpass("Enter the password again: ")
    print("Correct password:", authenticate_user(username, login_password))

    print(
        "Wrong password:",
        authenticate_user(username, "definitely-wrong-password")
    )
else:
    print("Registration did not succeed. Check the message above.")
 """

"""     if role not in {"ADMIN", "INVENTORY_MANAGER", "EMPLOYEE"}:
        return {
            "success": False,
            "message": "Invalid role."
        } """