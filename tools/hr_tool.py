from tools.database import get_connection


def get_employee_details(employee_id):
    """
    Get detailed information about a specific employee.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            e.employee_id,
            e.employee_name,
            e.email,
            e.phone,
            e.job_title,
            d.department_name,
            e.joining_date,
            e.salary,
            e.employment_status
        FROM employees e
        JOIN departments d
            ON e.department_id = d.department_id
        WHERE e.employee_id = %s;
    """

    cursor.execute(query, (employee_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is None:
        return None

    return {
        "employee_id": result[0],
        "employee_name": result[1],
        "email": result[2],
        "phone": result[3],
        "job_title": result[4],
        "department_name": result[5],
        "joining_date": result[6],
        "salary": result[7],
        "employment_status": result[8]
    }


def get_employee_attendance(employee_id):
    """
    Get attendance records for a specific employee.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            a.attendance_id,
            a.employee_id,
            e.employee_name,
            a.attendance_date,
            a.attendance_status,
            a.check_in,
            a.check_out
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.employee_id
        WHERE a.employee_id = %s
        ORDER BY a.attendance_date DESC;
    """

    cursor.execute(query, (employee_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "attendance_id": row[0],
            "employee_id": row[1],
            "employee_name": row[2],
            "attendance_date": row[3],
            "attendance_status": row[4],
            "check_in": row[5],
            "check_out": row[6]
        }
        for row in results
    ]

def get_employee_leaves(employee_id):
    """
    Get leave records for a specific employee.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            l.leave_id,
            l.employee_id,
            e.employee_name,
            l.leave_type,
            l.start_date,
            l.end_date,
            l.leave_status,
            l.reason
        FROM leave_records l
        JOIN employees e
            ON l.employee_id = e.employee_id
        WHERE l.employee_id = %s
        ORDER BY l.start_date DESC;
    """

    cursor.execute(query, (employee_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "leave_id": row[0],
            "employee_id": row[1],
            "employee_name": row[2],
            "leave_type": row[3],
            "start_date": row[4],
            "end_date": row[5],
            "leave_status": row[6],
            "reason": row[7]
        }
        for row in results
    ]


def get_department_employees(department_id):
    """
    Get all employees belonging to a specific department.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            e.employee_id,
            e.employee_name,
            e.email,
            e.job_title,
            d.department_name,
            e.employment_status
        FROM employees e
        JOIN departments d
            ON e.department_id = d.department_id
        WHERE e.department_id = %s
        ORDER BY e.employee_id;
    """

    cursor.execute(query, (department_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "employee_id": row[0],
            "employee_name": row[1],
            "email": row[2],
            "job_title": row[3],
            "department_name": row[4],
            "employment_status": row[5]
        }
        for row in results
    ]

def get_employee_count_by_department():
    """
    Get the number of employees in each department.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            d.department_id,
            d.department_name,
            COUNT(e.employee_id) AS employee_count
        FROM departments d
        LEFT JOIN employees e
            ON d.department_id = e.department_id
        GROUP BY
            d.department_id,
            d.department_name
        ORDER BY employee_count DESC;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "department_id": row[0],
            "department_name": row[1],
            "employee_count": row[2]
        }
        for row in results
    ]