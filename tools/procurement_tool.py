from tools.database import get_connection


def get_supplier_details(supplier_id):
    """
    Get detailed information about a specific supplier.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            supplier_id,
            supplier_name,
            email,
            phone,
            city,
            country
        FROM suppliers
        WHERE supplier_id = %s;
    """

    cursor.execute(query, (supplier_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return {"error": f"Supplier {supplier_id} not found"}

    return {
        "supplier_id": result[0],
        "supplier_name": result[1],
        "email": result[2],
        "phone": result[3],
        "city": result[4],
        "country": result[5],
    }

def get_supplier_products(supplier_id):
    """
    Get all products supplied by a specific supplier.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.unit_price
        FROM products p
        WHERE p.supplier_id = %s
        ORDER BY p.product_id;
    """

    cursor.execute(query, (supplier_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {"message": f"No products found for supplier {supplier_id}"}

    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "category": row[2],
            "unit_price": float(row[3])
        }
        for row in rows
    ]

def get_product_supplier(product_id):
    """
    Get the supplier information for a specific product.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            s.supplier_id,
            s.supplier_name,
            s.email,
            s.phone,
            s.city,
            s.country
        FROM products p
        JOIN suppliers s
            ON p.supplier_id = s.supplier_id
        WHERE p.product_id = %s;
    """

    cursor.execute(query, (product_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return {"error": f"Product {product_id} not found"}

    return {
        "product_id": result[0],
        "product_name": result[1],
        "supplier_id": result[2],
        "supplier_name": result[3],
        "supplier_email": result[4],
        "supplier_phone": result[5],
        "supplier_city": result[6],
        "supplier_country": result[7],
    }

def get_supplier_product_count():
    """
    Get the number of products supplied by each supplier.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            s.supplier_id,
            s.supplier_name,
            COUNT(p.product_id) AS product_count
        FROM suppliers s
        LEFT JOIN products p
            ON s.supplier_id = p.supplier_id
        GROUP BY s.supplier_id, s.supplier_name
        ORDER BY product_count DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "supplier_id": row[0],
            "supplier_name": row[1],
            "product_count": row[2]
        }
        for row in rows
    ]

def get_suppliers_by_country():
    """
    Get the number of suppliers in each country.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            country,
            COUNT(*) AS supplier_count
        FROM suppliers
        GROUP BY country
        ORDER BY supplier_count DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "country": row[0],
            "supplier_count": row[1]
        }
        for row in rows
    ]