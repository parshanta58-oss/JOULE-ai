from tools.database import get_connection

def get_sales_summary(start_date=None, end_date=None):

    connection = get_connection()
    cursor = connection.cursor()

    if start_date and end_date:

        query = """
            SELECT
                COUNT(*) AS total_orders,
                COALESCE(SUM(total_amount), 0) AS total_sales
            FROM orders
            WHERE order_date BETWEEN %s AND %s;
        """

        cursor.execute(query, (start_date, end_date))

    else:

        query = """
            SELECT
                COUNT(*) AS total_orders,
                COALESCE(SUM(total_amount), 0) AS total_sales
            FROM orders;
        """

        cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "total_orders": result[0],
        "total_sales": result[1]
    }

# we'll keep the data and time 


def get_top_customers(limit=10):

    connection=get_connection()
    cursor=connection.cursor()

    query="""

SELECT
            c.customer_id,
            c.customer_name,
            SUM(o.total_amount) AS total_sales
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        GROUP BY
            c.customer_id,
            c.customer_name
        ORDER BY total_sales DESC
        LIMIT %s;
    """


    cursor.execute(query,(limit,))

    results=cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {"customer_id":row[0],
         "customer_name":row[1],
         "total_sales":row[2]}
    for row in results
    ]



def get_customer_sales(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            c.customer_id,
            c.customer_name,
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(o.total_amount), 0) AS total_sales
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
        WHERE c.customer_id = %s
        GROUP BY
            c.customer_id,
            c.customer_name;
    """

    cursor.execute(query, (customer_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is None:
        return None

    return {
        "customer_id": result[0],
        "customer_name": result[1],
        "total_orders": result[2],
        "total_sales": result[3]
    }

def get_order_details(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            o.order_id,
            o.order_date,
            o.order_status,
            c.customer_id,
            c.customer_name,
            p.product_id,
            p.product_name,
            oi.quantity,
            oi.unit_price,
            oi.line_total
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE o.order_id = %s
        ORDER BY oi.order_item_id;
    """

    cursor.execute(query, (order_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    if not results:
        return None

    return {
        "order_id": results[0][0],
        "order_date": results[0][1],
        "order_status": results[0][2],
        "customer_id": results[0][3],
        "customer_name": results[0][4],
        "items": [
            {
                "product_id": row[5],
                "product_name": row[6],
                "quantity": row[7],
                "unit_price": row[8],
                "line_total": row[9]
            }
            for row in results
        ]
    }


def get_sales_by_product(limit=10):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.line_total) AS total_sales
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name,
            p.category
        ORDER BY total_sales DESC
        LIMIT %s;
    """

    cursor.execute(query, (limit,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "category": row[2],
            "units_sold": row[3],
            "total_sales": row[4]
        }
        for row in results
    ]