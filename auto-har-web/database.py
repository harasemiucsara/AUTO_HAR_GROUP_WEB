import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            category TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT,
            address TEXT,
            city TEXT,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_at_purchase REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


# ========== PRODUCTS ==========

def add_product(name, description, price, stock, category, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO products (name, description, price, stock, category, image_url)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (name, description, price, stock, category, image_url)
    )
    pid = cursor.lastrowid
    conn.commit()
    conn.close()
    return pid


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, stock, category, image_url, created_at FROM products ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_product(r) for r in rows]


def get_product_by_id(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, stock, category, image_url, created_at FROM products WHERE id = ?", (pid,))
    row = cursor.fetchone()
    conn.close()
    return _row_to_product(row) if row else None


def update_product(pid, name, description, price, stock, category, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE products
           SET name=?, description=?, price=?, stock=?, category=?, image_url=?
           WHERE id=?""",
        (name, description, price, stock, category, image_url, pid)
    )
    conn.commit()
    conn.close()


def delete_product(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
    conn.commit()
    conn.close()


def decrement_stock(pid, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?", (amount, pid, amount))
    conn.commit()
    conn.close()


# ========== ORDERS ==========

def create_order(customer_name, customer_email, customer_phone, address, city, total_amount, items):
    """
    items = list of dicts: [{"product_id": int, "quantity": int, "price_at_purchase": float}, ...]
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO orders (customer_name, customer_email, customer_phone, address, city, total_amount)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (customer_name, customer_email, customer_phone, address, city, total_amount)
    )
    order_id = cursor.lastrowid

    for item in items:
        cursor.execute(
            """INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
               VALUES (?, ?, ?, ?)""",
            (order_id, item["product_id"], item["quantity"], item["price_at_purchase"])
        )

    conn.commit()
    conn.close()
    return order_id


def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_name, customer_email, total_amount, status, created_at FROM orders ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": r[0], "customer_name": r[1], "customer_email": r[2],
        "total_amount": r[3], "status": r[4], "created_at": r[5]
    } for r in rows]


def get_order_with_items(oid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.customer_name, o.customer_email, o.customer_phone,
               o.address, o.city, o.total_amount, o.status, o.created_at
        FROM orders o WHERE o.id = ?
    """, (oid,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    order = {
        "id": row[0], "customer_name": row[1], "customer_email": row[2],
        "customer_phone": row[3], "address": row[4], "city": row[5],
        "total_amount": row[6], "status": row[7], "created_at": row[8],
        "items": []
    }

    cursor.execute("""
        SELECT oi.product_id, oi.quantity, oi.price_at_purchase, p.name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (oid,))
    for r in cursor.fetchall():
        order["items"].append({
            "product_id": r[0], "quantity": r[1],
            "price_at_purchase": r[2], "product_name": r[3]
        })

    conn.close()
    return order


# ========== UTILS ==========

def _row_to_product(row):
    return {
        "id": row[0], "name": row[1], "description": row[2],
        "price": row[3], "stock": row[4], "category": row[5],
        "image_url": row[6], "created_at": row[7]
    }
