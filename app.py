# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS expenses (category TEXT, amount REAL)")
    conn.commit()
    conn.close()

@app.route("/track", methods=["POST"])
def track():
    category = request.json["category"].lower()
    amount = float(request.json["amount"])
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))
    conn.commit()
    c.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
    total = c.fetchone()[0] or amount
    conn.close()
    return jsonify({"total_spent": total})

@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("SELECT category, amount FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return jsonify({"expenses": [{"category": row[0], "amount": row[1]} for row in expenses]})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)