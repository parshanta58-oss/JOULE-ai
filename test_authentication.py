
from getpass import getpass
from tools.authentication import register_user, authenticate_user

username = "prashanth_auth_test"
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
