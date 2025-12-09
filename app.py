import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='.', static_folder='.')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

# MongoDB connection
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_DBNAME = os.environ.get("MONGO_DBNAME")

conn_string = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/{MONGO_DBNAME}?retryWrites=true&w=majority"
client = MongoClient(conn_string)
db = client[MONGO_DBNAME]
employees = db.employees

# Unique indexes
employees.create_index([("employee_id", ASCENDING)], unique=True)
employees.create_index([("email", ASCENDING)], unique=True)

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

@app.route("/")
def home():
    return render_template("main.html")   # changed from index.html

@app.route("/add", methods=["POST"])
def add_employee():
    data = request.form
    employee = {
        "employee_id": data.get("employee_id", "").strip(),
        "first_name": data.get("first_name", "").strip(),
        "last_name": data.get("last_name", "").strip(),
        "nic_number": data.get("nic_number", "").strip(),
        "date_of_birth": parse_date(data.get("date_of_birth")),
        "contact_number": data.get("contact_number", "").strip(),
        "address": data.get("address", "").strip(),
        "department": data.get("department", "").strip(),
        "authentication": data.get("authentication", "User"),
        "email": data.get("email", "").strip().lower(),
        "date_of_joining": parse_date(data.get("date_of_joining")),
    }

    password = data.get("password", "")
    if not password:
        flash("Password is required", "danger")
        return redirect(url_for("home"))

    employee["password_hash"] = generate_password_hash(password)

    for field in ["employee_id", "first_name", "last_name", "email"]:
        if not employee[field]:
            flash(f"{field.replace('_', ' ').title()} is required.", "danger")
            return redirect(url_for("home"))

    try:
        employees.insert_one(employee)
    except Exception as e:
        flash(f"Error adding employee: {str(e)}", "danger")
        return redirect(url_for("home"))

    flash("Employee added successfully!", "success")
    return redirect(url_for("list_employees"))

@app.route("/employees")
def list_employees():
    docs = list(employees.find().sort("employee_id", ASCENDING))
    for d in docs:
        if d.get("date_of_birth"):
            d["date_of_birth"] = d["date_of_birth"].strftime("%Y-%m-%d")
        if d.get("date_of_joining"):
            d["date_of_joining"] = d["date_of_joining"].strftime("%Y-%m-%d")
    return render_template("list.html", employees=docs)

if __name__ == "__main__":
    app.run(debug=True)
