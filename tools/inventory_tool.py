from tools.database import get_connection


def get_low_stock_products():
    """
    Get products whose inventory quantity is at or below the reorder level.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            i.inventory_id,
            p.product_id,
            p.product_name,
            p.category,
            w.warehouse_id,
            w.warehouse_name,
            i.quantity,
            i.reorder_level
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        WHERE i.quantity <= i.reorder_level
        ORDER BY i.quantity ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {"message": "No low-stock products found"}

    return [
        {
            "inventory_id": row[0],
            "product_id": row[1],
            "product_name": row[2],
            "category": row[3],
            "warehouse_id": row[4],
            "warehouse_name": row[5],
            "quantity": row[6],
            "reorder_level": row[7]
        }
        for row in rows
    ]

def get_warehouse_inventory(warehouse_id):
    """
    Get inventory details for all products in a specific warehouse.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            i.inventory_id,
            p.product_id,
            p.product_name,
            p.category,
            i.quantity,
            i.reorder_level,
            i.last_updated
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        WHERE i.warehouse_id = %s
        ORDER BY i.quantity ASC;
    """

    cursor.execute(query, (warehouse_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {"message": f"No inventory found for warehouse {warehouse_id}"}

    return [
        {
            "inventory_id": row[0],
            "product_id": row[1],
            "product_name": row[2],
            "category": row[3],
            "quantity": row[4],
            "reorder_level": row[5],
            "last_updated": str(row[6])
        }
        for row in rows
    ]

def get_product_inventory(product_id):
    """
    Get inventory details for a specific product across warehouses.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            w.warehouse_id,
            w.warehouse_name,
            w.city,
            i.quantity,
            i.reorder_level,
            i.last_updated
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        JOIN warehouses w
            ON i.warehouse_id = w.warehouse_id
        WHERE p.product_id = %s
        ORDER BY w.warehouse_id;
    """

    cursor.execute(query, (product_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {"message": f"No inventory found for product {product_id}"}

    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "category": row[2],
            "warehouse_id": row[3],
            "warehouse_name": row[4],
            "warehouse_city": row[5],
            "quantity": row[6],
            "reorder_level": row[7],
            "last_updated": str(row[8])
        }
        for row in rows
    ]

def get_inventory_summary_by_warehouse():
    """
    Get inventory summary for each warehouse.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            w.warehouse_id,
            w.warehouse_name,
            w.city,
            COUNT(i.inventory_id) AS product_count,
            COALESCE(SUM(i.quantity), 0) AS total_quantity,
            COUNT(
                CASE
                    WHEN i.quantity <= i.reorder_level
                    THEN 1
                END
            ) AS low_stock_items
        FROM warehouses w
        LEFT JOIN inventory i
            ON w.warehouse_id = i.warehouse_id
        GROUP BY
            w.warehouse_id,
            w.warehouse_name,
            w.city
        ORDER BY w.warehouse_id;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "warehouse_id": row[0],
            "warehouse_name": row[1],
            "city": row[2],
            "product_count": row[3],
            "total_quantity": row[4],
            "low_stock_items": row[5]
        }
        for row in rows
    ]

def get_inventory_by_category():
    """
    Get total inventory quantity grouped by product category.
    """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.category,
            COUNT(DISTINCT p.product_id) AS product_count,
            COALESCE(SUM(i.quantity), 0) AS total_quantity
        FROM products p
        LEFT JOIN inventory i
            ON p.product_id = i.product_id
        GROUP BY p.category
        ORDER BY total_quantity DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "category": row[0],
            "product_count": row[1],
            "total_quantity": row[2]
        }
        for row in rows
    ]