from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import database

app = Flask(__name__, static_folder=".")
CORS(app)

ADMIN_PASSWORD = "admin123"

database.init_db()


# ========== PAGES ==========

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/admin")
def admin_page():
    return send_from_directory(".", "admin.html")


# ========== PRODUCTS ==========

@app.route("/api/products", methods=["GET"])
def list_products():
    return jsonify(database.get_all_products())


@app.route("/api/products/<int:pid>", methods=["GET"])
def get_product(pid):
    product = database.get_product_by_id(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    required = ["name", "price", "stock"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    pid = database.add_product(
        name=data["name"],
        description=data.get("description", ""),
        price=float(data["price"]),
        stock=int(data["stock"]),
        category=data.get("category", ""),
        image_url=data.get("image_url", "")
    )
    return jsonify({"id": pid}), 201


@app.route("/api/products/<int:pid>", methods=["PUT"])
def edit_product(pid):
    data = request.get_json()
    existing = database.get_product_by_id(pid)
    if not existing:
        return jsonify({"error": "Product not found"}), 404

    database.update_product(
        pid=pid,
        name=data.get("name", existing["name"]),
        description=data.get("description", existing["description"]),
        price=float(data.get("price", existing["price"])),
        stock=int(data.get("stock", existing["stock"])),
        category=data.get("category", existing["category"]),
        image_url=data.get("image_url", existing["image_url"])
    )
    return jsonify({"updated": pid})


@app.route("/api/products/<int:pid>", methods=["DELETE"])
def remove_product(pid):
    database.delete_product(pid)
    return jsonify({"deleted": pid})


# ========== ORDERS ==========

@app.route("/api/orders", methods=["POST"])
def place_order():
    data = request.get_json()

    # Validare câmpuri client
    required = ["customer_name", "customer_email", "items"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    items = data["items"]
    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    total = sum(item["price_at_purchase"] * item["quantity"] for item in items)

    # Creează comanda în baza de date
    order_id = database.create_order(
        customer_name=data["customer_name"],
        customer_email=data["customer_email"],
        customer_phone=data.get("customer_phone", ""),
        address=data.get("address", ""),
        city=data.get("city", ""),
        total_amount=total,
        items=items
    )

    # Scade stocul pentru fiecare produs comandat
    for item in items:
        database.decrement_stock(item["product_id"], item["quantity"])

    return jsonify({"order_id": order_id, "total": total}), 201


@app.route("/api/orders", methods=["GET"])
def list_orders():
    return jsonify(database.get_all_orders())


@app.route("/api/orders/<int:oid>", methods=["GET"])
def get_order(oid):
    order = database.get_order_with_items(oid)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)


# ========== ADMIN AUTH ==========

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    if data.get("password") == ADMIN_PASSWORD:
        return jsonify({"success": True})
    return jsonify({"success": False}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
