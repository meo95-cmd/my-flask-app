from flask import Flask, request, jsonify, render_template
import json, os, csv
from io import StringIO

app = Flask(__name__)
DATA_FILE = "data.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    task = {
        "No": data["No"],
        "date": data["date"],
        "device": data["device"],
        "problem": data["problem"],
        "cause": data["cause"],
        "solution": data["solution"],
        "person": data["person"],
        "priority": data["priority"],
        "comment": data["comment"],
    }
    tasks.append(task)
    save_tasks(tasks)
    return jsonify({"message": "Thêm thành công!"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/delete/<int:task_no>", methods=["DELETE"])
def delete_task(task_no):
    global tasks
    tasks = [task for task in tasks if int(task["No"]) != task_no]
    save_tasks(tasks)
    return jsonify({"message": "Đã xóa thành công!"})

@app.route("/edit/<int:task_no>", methods=["PUT"])
def edit_task(task_no):
    data = request.json
    for task in tasks:
        if int(task["No"]) == task_no:
            task.update({
                "date": data["date"],
                "device": data["device"],
                "problem": data["problem"],
                "cause": data["cause"],
                "solution": data["solution"],
                "person": data["person"],
                "priority": data["priority"],
                "comment": data["comment"],
            })
            break
    save_tasks(tasks)
    return jsonify({"message": "Đã cập nhật thành công!"})

@app.route("/export", methods=["GET"])
def export_csv():
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=["No", "date", "device", "problem", "cause", "solution", "person", "priority", "comment"])
    writer.writeheader()
    writer.writerows(tasks)
    output = si.getvalue()
    return output, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=tasks.csv"
    }

if __name__ == "__main__":
    app.run(debug=True)

