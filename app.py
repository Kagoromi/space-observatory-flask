from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import requests
import database
import api_service

app = Flask(__name__)
app.secret_key = "space_observatory_secret_key"

# Init SQLite DB
database.init_db()

# Web Interface

@app.route("/")
def home():
    # Task 1 and 15: Home page
    return render_template("index.html")

@app.route("/search")
def search():
    # Task 3: Input query check
    query = request.args.get("query", "").strip()
    
    if not query or len(query) < 2:
        return render_template("index.html", error="Enter query with at least 2 symbols.")
    
    # Task 4: Network and response error handling
    try:
        results = api_service.search_external_api(query)
    except requests.exceptions.Timeout:
        return render_template("index.html", error="API timeout reached.")
    except requests.exceptions.RequestException:
        return render_template("index.html", error="NASA service unavailable.")
    
    if not results:
        return render_template("index.html", error=f"Nothing found for {query}.")
    
    # Task 5: Render results in template
    return render_template("results.html", results=results, query=query)

@app.route("/save", methods=["POST"])
def save_item():
    # Task 6 and 7: Save item via POST and prevent duplicate entries
    external_id = request.form.get("external_id")
    title = request.form.get("title")
    center = request.form.get("center")
    date_created = request.form.get("date_created")
    
    if database.get_item_by_external_id(external_id):
        flash("Item already exists in database.", "warning")
        return redirect(url_for("saved"))
    
    database.add_item(external_id, title, center, date_created)
    flash("Item saved successfully.", "success")
    return redirect(url_for("saved"))

@app.route("/saved")
def saved():
    # Task 8 and 11: Saved items page with local search filter
    search_query = request.args.get("search", "").strip()
    items = database.get_all_items(search_query)
    return render_template("saved.html", items=items, search_query=search_query)

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    # Task 9: Edit record notes
    item = database.get_item_by_id(item_id)
    if not item:
        return render_template("index.html", error="Item not found."), 404
        
    if request.method == "POST":
        notes = request.form.get("notes", "").strip()
        title = request.form.get("title", "").strip()
        center = request.form.get("center", "").strip()
        database.update_item(item_id, notes, title, center)
        flash("Record updated successfully.", "success")
        return redirect(url_for("saved"))
        
    return render_template("edit.html", item=item)

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    # Task 10: Delete item via POST
    database.delete_item(item_id)
    flash("Item deleted from database.", "info")
    return redirect(url_for("saved"))

# REST API Endpoints (Task 12 and 13)

@app.route("/api/items", methods=["GET"])
def api_get_items():
    items = database.get_all_items()
    return jsonify([dict(item) for item in items]), 200

@app.route("/api/items/<int:item_id>", methods=["GET"])
def api_get_item(item_id):
    item = database.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(dict(item)), 200

@app.route("/api/items", methods=["POST"])
def api_create_item():
    data = request.get_json() or {}
    if not data.get("title") or not data.get("external_id"):
        return jsonify({"error": "Title and external_id required"}), 400
    
    success = database.add_item(
        external_id=data.get("external_id"),
        title=data.get("title"),
        center=data.get("center", "Custom REST"),
        date_created=data.get("date_created", "2026-01-01"),
        notes=data.get("notes", "Created via REST API")
    )
    
    if not success:
        return jsonify({"error": "Item with this external_id already exists"}), 400
        
    return jsonify({"message": "Item created successfully"}), 201

@app.route("/api/items/<int:item_id>", methods=["PATCH", "PUT"])
def api_update_item(item_id):
    item = database.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
        
    data = request.get_json() or {}
    notes = data.get("notes", item["notes"])
    title = data.get("title", item["title"])
    center = data.get("center", item["center"])
    
    database.update_item(item_id, notes, title, center)
    return jsonify({"message": "Item updated successfully"}), 200

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def api_delete_item(item_id):
    item = database.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
        
    database.delete_item(item_id)
    return jsonify({"message": "Item deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)