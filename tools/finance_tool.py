from tools.database import get_connection


def get_total_expenses():
    """
    Get the total amount of all expenses.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COALESCE(SUM(expense_amount), 0)
        FROM expenses;
    """

    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "total_expenses": result[0]
    }

def get_department_expenses():
    """
    Get the total expenses for each department.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            d.department_id,
            d.department_name,
            COALESCE(SUM(e.expense_amount), 0) AS total_expenses
        FROM departments d
        LEFT JOIN expenses e
            ON d.department_id = e.department_id
        GROUP BY
            d.department_id,
            d.department_name
        ORDER BY total_expenses DESC;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "department_id": row[0],
            "department_name": row[1],
            "total_expenses": row[2]
        }
        for row in results
    ]

def get_department_budgets():
    """
    Get the total budget allocated to each department.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            d.department_id,
            d.department_name,
            COALESCE(SUM(b.budget_amount), 0) AS total_budget
        FROM departments d
        LEFT JOIN budgets b
            ON d.department_id = b.department_id
        GROUP BY
            d.department_id,
            d.department_name
        ORDER BY total_budget DESC;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "department_id": row[0],
            "department_name": row[1],
            "total_budget": row[2]
        }
        for row in results
    ]

def get_invoice_status():
    """
    Get the number of invoices and total invoice amount grouped by invoice status.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            invoice_status,
            COUNT(*) AS invoice_count,
            COALESCE(SUM(invoice_amount), 0) AS total_amount
        FROM invoices
        GROUP BY invoice_status
        ORDER BY invoice_status;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "invoice_status": row[0],
            "invoice_count": row[1],
            "total_amount": row[2]
        }
        for row in results
    ]

def get_payment_summary():
    """
    Get the number of payments and total payment amount grouped by payment status.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            payment_status,
            COUNT(*) AS payment_count,
            COALESCE(SUM(payment_amount), 0) AS total_amount
        FROM payments
        GROUP BY payment_status
        ORDER BY payment_status;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "payment_status": row[0],
            "payment_count": row[1],
            "total_amount": row[2]
        }
        for row in results
    ]