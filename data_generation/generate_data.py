from faker import Faker
import psycopg2
from datetime import date, timedelta
fake = Faker()

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "joule_ai_db",
    "user": "joule_ai_user",
    "password": "joule_ai_password",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def generate_departments(cursor):
    departments = [
        "Sales",
        "Finance",
        "HR",
        "Procurement",
        "Inventory",
    ]

    department_ids = []

    for department_name in departments:
        cursor.execute(
            """
            INSERT INTO departments (department_name)
            VALUES (%s)
            RETURNING department_id;
            """,
            (department_name,)
        )

        department_id = cursor.fetchone()[0]
        department_ids.append(department_id)

    return department_ids


def generate_employees(cursor, department_ids, count=20):
    employee_ids = []

    job_titles = [
        "Sales Executive",
        "Sales Manager",
        "Finance Analyst",
        "HR Executive",
        "Procurement Specialist",
        "Inventory Manager",
    ]

    for _ in range(count):

        employee_name = fake.name()
        email = fake.unique.email()
        phone = fake.phone_number()[:20]
        job_title = fake.random_element(job_titles)

        department_id = fake.random_element(department_ids)

        joining_date = fake.date_between(
            start_date="-5y",
            end_date="today"
        )

        salary = fake.random_int(
            min=30000,
            max=150000
        )

        cursor.execute(
            """
            INSERT INTO employees
            (
                employee_name,
                email,
                phone,
                job_title,
                department_id,
                joining_date,
                salary,
                employment_status
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING employee_id;
            """,
            (
                employee_name,
                email,
                phone,
                job_title,
                department_id,
                joining_date,
                salary,
                "ACTIVE"
            )
        )

        employee_id = cursor.fetchone()[0]
        employee_ids.append(employee_id)

    return employee_ids
def generate_customers(cursor, count=1000):
    customer_ids = []

    for _ in range(count):

        customer_name = fake.company()
        email = fake.unique.email()
        phone = fake.phone_number()[:20]
        city = fake.city()
        country = "India"

        cursor.execute(
            """
            INSERT INTO customers
            (
                customer_name,
                email,
                phone,
                city,
                country
            )
            VALUES
            (%s, %s, %s, %s, %s)
            RETURNING customer_id;
            """,
            (
                customer_name,
                email,
                phone,
                city,
                country
            )
        )

        customer_id = cursor.fetchone()[0]
        customer_ids.append(customer_id)

    return customer_ids

def generate_suppliers(cursor, count=30):
    supplier_ids = []

    for _ in range(count):

        supplier_name = fake.company()
        email = fake.unique.email()
        phone = fake.phone_number()[:20]
        city = fake.city()
        country = "India"

        cursor.execute(
            """
            INSERT INTO suppliers
            (
                supplier_name,
                email,
                phone,
                city,
                country
            )
            VALUES
            (%s, %s, %s, %s, %s)
            RETURNING supplier_id;
            """,
            (
                supplier_name,
                email,
                phone,
                city,
                country
            )
        )

        supplier_id = cursor.fetchone()[0]
        supplier_ids.append(supplier_id)

    return supplier_ids


def generate_products(cursor, supplier_ids, count=200):
    product_ids = []

    product_names = [
        "Enterprise Laptop",
        "Business Laptop",
        "Cloud Server",
        "Database Server",
        "Barcode Scanner",
        "Network Router",
        "Office Monitor",
        "Wireless Keyboard",
        "Wireless Mouse",
        "Enterprise Printer",
        "Storage Drive",
        "Security Camera",
    ]

    categories = [
        "Computers",
        "Servers",
        "Networking",
        "Accessories",
        "Office Equipment",
        "Security",
    ]

    for _ in range(count):

        product_name = fake.random_element(product_names)
        category = fake.random_element(categories)
        supplier_id = fake.random_element(supplier_ids)

        unit_price = fake.random_int(
            min=1000,
            max=500000
        )

        cursor.execute(
            """
            INSERT INTO products
            (
                product_name,
                category,
                supplier_id,
                unit_price
            )
            VALUES
            (%s, %s, %s, %s)
            RETURNING product_id;
            """,
            (
                product_name,
                category,
                supplier_id,
                unit_price
            )
        )

        product_id = cursor.fetchone()[0]
        product_ids.append(product_id)

    return product_ids

def generate_warehouses(cursor):
    warehouses = [
        ("Bangalore Central Warehouse", "Bangalore"),
        ("Mumbai Distribution Center", "Mumbai"),
        ("Delhi Storage Facility", "Delhi"),
    ]

    warehouse_ids = []

    for warehouse_name, city in warehouses:

        cursor.execute(
            """
            INSERT INTO warehouses
            (
                warehouse_name,
                city
            )
            VALUES
            (%s, %s)
            RETURNING warehouse_id;
            """,
            (
                warehouse_name,
                city
            )
        )

        warehouse_id = cursor.fetchone()[0]
        warehouse_ids.append(warehouse_id)

    return warehouse_ids


def generate_inventory(cursor, product_ids, warehouse_ids):
    inventory_count = 0

    for product_id in product_ids:

        warehouse_id = fake.random_element(warehouse_ids)

        quantity = fake.random_int(
            min=10,
            max=1000
        )

        reorder_level = fake.random_int(
            min=20,
            max=200
        )

        cursor.execute(
            """
            INSERT INTO inventory
            (
                product_id,
                warehouse_id,
                quantity,
                reorder_level,
                last_updated
            )
            VALUES
            (%s, %s, %s, %s, %s);
            """,
            (
                product_id,
                warehouse_id,
                quantity,
                reorder_level,
                fake.date_time_this_year()
            )
        )

        inventory_count += 1

    return inventory_count

def generate_orders(cursor, customer_ids, count=5000):
    order_ids = []

    order_statuses = [
        "PENDING",
        "CONFIRMED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED"
    ]

    for _ in range(count):

        customer_id = fake.random_element(customer_ids)

        order_date = fake.date_between(
            start_date="-1y",
            end_date="today"
        )

        order_status = fake.random_element(order_statuses)

        total_amount = fake.random_int(
            min=5000,
            max=1000000
        )

        created_at = fake.date_time_this_year()

        cursor.execute(
            """
            INSERT INTO orders
            (
                customer_id,
                order_date,
                order_status,
                total_amount,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s)
            RETURNING order_id;
            """,
            (
                customer_id,
                order_date,
                order_status,
                total_amount,
                created_at
            )
        )

        order_id = cursor.fetchone()[0]
        order_ids.append(order_id)

    return order_ids

def generate_order_items(cursor, order_ids, product_ids):
    order_item_count = 0

    for order_id in order_ids:

        number_of_items = fake.random_int(
            min=1,
            max=5
        )

        selected_products = fake.random_elements(
            elements=product_ids,
            length=number_of_items,
            unique=True
        )

        for product_id in selected_products:

            quantity = fake.random_int(
                min=1,
                max=20
            )

            cursor.execute(
                """
                SELECT unit_price
                FROM products
                WHERE product_id = %s;
                """,
                (product_id,)
            )

            unit_price = cursor.fetchone()[0]

            line_total = quantity * unit_price

            cursor.execute(
                """
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    line_total
                )
                VALUES
                (%s, %s, %s, %s, %s);
                """,
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    line_total
                )
            )

            order_item_count += 1

    return order_item_count

def generate_invoices(cursor, order_data):
    invoice_ids = []

    invoice_statuses = [
        "PAID",
        "UNPAID",
        "PARTIALLY_PAID",
        "OVERDUE"
    ]

    for order_id, customer_id, order_date, total_amount in order_data:

        # Create invoices for roughly 80% of orders
        if fake.random_int(min=1, max=100) > 80:
            continue

        invoice_date = order_date

        due_date = invoice_date + timedelta(days=30)

        invoice_status = fake.random_element(
            invoice_statuses
        )

        cursor.execute(
            """
            INSERT INTO invoices
            (
                order_id,
                customer_id,
                invoice_date,
                due_date,
                invoice_amount,
                invoice_status,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            RETURNING invoice_id;
            """,
            (
                order_id,
                customer_id,
                invoice_date,
                due_date,
                total_amount,
                invoice_status,
                fake.date_time_this_year()
            )
        )

        invoice_id = cursor.fetchone()[0]
        invoice_ids.append(invoice_id)

    return invoice_ids


def generate_payments(cursor, invoice_data):
    payment_ids = []

    payment_methods = [
        "BANK_TRANSFER",
        "CREDIT_CARD",
        "UPI",
        "CHEQUE"
    ]

    payment_statuses = [
        "COMPLETED",
        "PENDING",
        "FAILED"
    ]

    for invoice_id, customer_id, invoice_date, invoice_amount in invoice_data:

        # Around 70% of invoices receive a payment
        if fake.random_int(min=1, max=100) > 70:
            continue

        payment_date = fake.date_between(
            start_date=invoice_date,
            end_date="today"
        )

        # Payment can be partial or full
        payment_amount = fake.random_int(
            min=1000,
            max=int(invoice_amount)
        )

        payment_method = fake.random_element(
            payment_methods
        )

        payment_status = fake.random_element(
            payment_statuses
        )

        cursor.execute(
            """
            INSERT INTO payments
            (
                invoice_id,
                customer_id,
                payment_date,
                payment_amount,
                payment_method,
                payment_status,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            RETURNING payment_id;
            """,
            (
                invoice_id,
                customer_id,
                payment_date,
                payment_amount,
                payment_method,
                payment_status,
                fake.date_time_this_year()
            )
        )

        payment_id = cursor.fetchone()[0]
        payment_ids.append(payment_id)

    return payment_ids       

def generate_expenses(cursor, employee_data, count=3000):
    expense_ids = []

    expense_categories = [
        "TRAVEL",
        "MEALS",
        "OFFICE_SUPPLIES",
        "SOFTWARE",
        "TRAINING",
        "TRANSPORTATION",
        "ACCOMMODATION"
    ]

    expense_statuses = [
        "APPROVED",
        "PENDING",
        "REJECTED"
    ]

    for _ in range(count):

        employee_id, department_id = fake.random_element(
            employee_data
        )

        expense_date = fake.date_between(
            start_date="-1y",
            end_date="today"
        )

        expense_category = fake.random_element(
            expense_categories
        )

        description = fake.sentence(
            nb_words=8
        )

        expense_amount = fake.random_int(
            min=500,
            max=100000
        )

        expense_status = fake.random_element(
            expense_statuses
        )

        created_at = fake.date_time_this_year()

        cursor.execute(
            """
            INSERT INTO expenses
            (
                employee_id,
                department_id,
                expense_date,
                expense_category,
                description,
                expense_amount,
                expense_status,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING expense_id;
            """,
            (
                employee_id,
                department_id,
                expense_date,
                expense_category,
                description,
                expense_amount,
                expense_status,
                created_at
            )
        )

        expense_id = cursor.fetchone()[0]
        expense_ids.append(expense_id)

    return expense_ids

def generate_budgets(cursor, department_ids):
    budget_ids = []

    for department_id in department_ids:

        for month in range(1, 13):

            budget_amount = fake.random_int(
                min=500000,
                max=5000000
            )

            cursor.execute(
                """
                INSERT INTO budgets
                (
                    department_id,
                    budget_year,
                    budget_month,
                    budget_amount,
                    created_at
                )
                VALUES
                (%s, %s, %s, %s, %s)
                RETURNING budget_id;
                """,
                (
                    department_id,
                    2026,
                    month,
                    budget_amount,
                    fake.date_time_this_year()
                )
            )

            budget_id = cursor.fetchone()[0]
            budget_ids.append(budget_id)

    return budget_ids

def generate_leave_records(cursor, employee_ids, count=500):
    leave_ids = []

    leave_types = [
        "CASUAL",
        "SICK",
        "ANNUAL",
        "MATERNITY",
        "PATERNITY",
        "EMERGENCY"
    ]

    leave_statuses = [
        "APPROVED",
        "PENDING",
        "REJECTED"
    ]

    for _ in range(count):

        employee_id = fake.random_element(employee_ids)

        start_date = fake.date_between(
            start_date="-1y",
            end_date="today"
        )

        leave_days = fake.random_int(
            min=1,
            max=15
        )

        end_date = start_date + timedelta(
            days=leave_days - 1
        )

        leave_type = fake.random_element(
            leave_types
        )

        leave_status = fake.random_element(
            leave_statuses
        )

        reason = fake.sentence(
            nb_words=8
        )

        created_at = fake.date_time_this_year()

        cursor.execute(
            """
            INSERT INTO leave_records
            (
                employee_id,
                leave_type,
                start_date,
                end_date,
                leave_status,
                reason,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            RETURNING leave_id;
            """,
            (
                employee_id,
                leave_type,
                start_date,
                end_date,
                leave_status,
                reason,
                created_at
            )
        )

        leave_id = cursor.fetchone()[0]
        leave_ids.append(leave_id)

    return leave_ids

def generate_attendance(cursor, employee_ids):
    attendance_count = 0

    attendance_statuses = [
        "PRESENT",
        "PRESENT",
        "PRESENT",
        "ABSENT",
        "LATE",
        "HALF_DAY"
    ]

    start_date = fake.date_between(
        start_date="-180d",
        end_date="-179d"
    )

    end_date =date.today()

    current_date = start_date

    while current_date <= end_date:

        # Monday = 0, Sunday = 6
        if current_date.weekday() < 5:

            for employee_id in employee_ids:

                attendance_status = fake.random_element(
                    attendance_statuses
                )

                check_in = None
                check_out = None

                if attendance_status == "PRESENT":

                    check_in = fake.time(
                        pattern="%H:%M:%S"
                    )

                    check_out = fake.time(
                        pattern="%H:%M:%S"
                    )

                elif attendance_status == "LATE":

                    check_in = fake.time(
                        pattern="%H:%M:%S"
                    )

                    check_out = fake.time(
                        pattern="%H:%M:%S"
                    )

                elif attendance_status == "HALF_DAY":

                    check_in = fake.time(
                        pattern="%H:%M:%S"
                    )

                    check_out = fake.time(
                        pattern="%H:%M:%S"
                    )

                cursor.execute(
                    """
                    INSERT INTO attendance
                    (
                        employee_id,
                        attendance_date,
                        attendance_status,
                        check_in,
                        check_out,
                        created_at
                    )
                    VALUES
                    (%s, %s, %s, %s, %s, %s)
                    RETURNING attendance_id;
                    """,
                    (
                        employee_id,
                        current_date,
                        attendance_status,
                        check_in,
                        check_out,
                        fake.date_time_this_year()
                    )
                )

                cursor.fetchone()

                attendance_count += 1

        current_date += timedelta(days=1)

    return attendance_count

def generate_support_tickets(cursor, customer_ids, employee_ids, count=2000):
    ticket_ids = []

    issue_categories = [
        "PAYMENT",
        "DELIVERY",
        "PRODUCT",
        "TECHNICAL",
        "ACCOUNT",
        "ORDER",
        "OTHER"
    ]

    priorities = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]

    ticket_statuses = [
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED"
    ]

    for _ in range(count):

        customer_id = fake.random_element(customer_ids)
        assigned_employee_id = fake.random_element(employee_ids)

        ticket_date = fake.date_between(
            start_date="-1y",
            end_date="today"
        )

        issue_category = fake.random_element(
            issue_categories
        )

        priority = fake.random_element(
            priorities
        )

        ticket_status = fake.random_element(
            ticket_statuses
        )

        subject = fake.sentence(
            nb_words=6
        )

        description = fake.paragraph(
            nb_sentences=2
        )

        resolution = None
        resolved_date = None

        if ticket_status == "RESOLVED":

            resolution = fake.sentence(
                nb_words=10
            )

            resolved_date = fake.date_between(
                start_date=ticket_date,
                end_date="today"
            )

        created_at = fake.date_time_this_year()

        cursor.execute(
            """
            INSERT INTO support_tickets
            (
                customer_id,
                assigned_employee_id,
                ticket_date,
                issue_category,
                priority,
                ticket_status,
                subject,
                description,
                resolution,
                resolved_date,
                created_at
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING ticket_id;
            """,
            (
                customer_id,
                assigned_employee_id,
                ticket_date,
                issue_category,
                priority,
                ticket_status,
                subject,
                description,
                resolution,
                resolved_date,
                created_at
            )
        )

        ticket_id = cursor.fetchone()[0]
        ticket_ids.append(ticket_id)

    return ticket_ids

# Actual execution starts here
connection = get_connection()
cursor = connection.cursor()

try:

    cursor.execute(
        "SELECT customer_id FROM customers;"
    )

    customer_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.execute(
        "SELECT employee_id FROM employees;"
    )

    employee_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    ticket_ids = generate_support_tickets(
        cursor,
        customer_ids,
        employee_ids,
        count=2000
    )

    connection.commit()

    print(f"Created {len(ticket_ids)} support tickets")

except Exception as error:

    connection.rollback()
    print("Error:", error)

finally:

    cursor.close()
    connection.close()