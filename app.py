from flask import Flask, jsonify, request, session
from flask_bcrypt import generate_password_hash, check_password_hash
import os
import sqlite3


DATABASE = "./database.db"


app = Flask(__name__)

app.secret_key = os.urandom(24)


if not os.path.exists(DATABASE):

    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY '
                 'AUTOINCREMENT, username STRING NOT NULL UNIQUE, password STRING NOT NULL)')
    conn.commit()
    conn.close()


@app.route("/api/users/register", methods=["POST"])
def register():
    """Create a new user requesting user registration details"""
    reg_details = request.get_json()
    username = reg_details["username"]
    password = reg_details["password"]
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
        con.commit()
        response = "Success"

    return response, 201


@app.route("/api/users/auth", methods=["POST"])
def auth():
    login_details = request.get_json()
    username = login_details["username"]
    password = login_details["password"]
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users where username = ? AND password = ?", (username, password))
    account = cur.fetchone()
    a = dict([("user_id", account[0]), ("username", account[1]), ("password", account[2])])
    session["username"] = a["username"]
    if account:
        return jsonify(a)
    # session["username"] =
    else:
        response = "Invalid Username/Password"
        return jsonify(response)


@app.route("/api/projects", methods=["GET", "POST"])
def projects():
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * from projects")
        rows = cur.fetchall()
        return jsonify(rows), 200

    elif request.method == "POST":
        con = sqlite3.connect(DATABASE)
        con.execute('CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'project_name STRING NOT NULL UNIQUE, description STRING NOT NULL, completed INTEGER)')
        con.commit()
        con.close()

        project_details = request.get_json()
        project_name = project_details["project_name"]
        description = project_details["description"]
        completed = project_details["completed"]

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO projects(project_name, description, completed) VALUES (?, ?, ?)', (project_name,
                        description, completed))
            con.commit()
            response = "Success, New project added"
            return jsonify(response), 201


@app.route("/api/projects/<int:project_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def project(project_id):
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM projects where project_id = {}".format(project_id))
        rows = cur.fetchone()
        return jsonify(rows)

    elif request.method == "PATCH":
        completed = request.get_json("completed")
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("UPDATE projects SET completed = ? "
                    "where project_id = ?", (completed, project_id))
        con.commit()
        response = "Updated project status (Completed)"
        return jsonify(response)

    elif request.method == "PUT":
        update_project = request.get_json()
        project_name = update_project["project_name"]
        description = update_project["description"]
        completed = update_project["completed"]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("UPDATE projects SET project_name = ?, description = ?, completed = ? "
                    "where project_id = ?", (project_name, description, completed, project_id))
        con.commit()
        response = "Updated project"
        return jsonify(response)

    elif request.method == "DELETE":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM projects where project_id = {}".format(project_id))
        con.commit()
        response = "Project Deleted"
        return jsonify(response)


@app.route("/api/projects/<int:project_id>/actions", methods=["GET", "POST"])
def project_actions(project_id):
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM actions where project_id =  {}".format(project_id))
        rows = cur.fetchall()
        return jsonify(rows)

    elif request.method == "POST":
        con = sqlite3.connect(DATABASE)
        con.execute("CREATE TABLE IF NOT EXISTS actions (actions_id INTEGER PRIMARY "
                    "KEY AUTOINCREMENT, description STRING, note STRING, project_id INTEGER, "
                    "FOREIGN KEY(project_id) REFERENCES projects(project_id))")
        con.commit()
        con.close()

        action_data = request.get_json()
        description = action_data["description"]
        note = action_data["note"]
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO actions(project_id, description, note) VALUES (?, ?, ?)', (project_id,
                        description, note))
            con.commit()
            response = "Success"
        return jsonify(response)


@app.route("/api/actions")
def all_actions():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM actions")
    rows = cur.fetchall()
    return jsonify(rows)


@app.route("/api/projects/<int:project_id>/actions/<int:actions_id>", methods=["GET", "PUT", "DELETE"])
def project_actions_update(project_id, actions_id):
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM actions where project_id = {} AND actions_id = {}".format(project_id, actions_id))
        rows = cur.fetchone()
        return jsonify(rows), 200

    elif request.method == "PUT":
        update_actions = request.get_json()
        description = update_actions["description"]
        note = update_actions["note"]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("UPDATE projects SET description = ?, note = ?,"
                    "where project_id = ? AND actions_id = ?", (description, note, project_id, actions_id))
        con.commit()
        response = "Updated action for project"
        return jsonify(response)

    elif request.method == "DELETE":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM actions where project_id = {} AND actions_id = {}".format(project_id, actions_id))
        con.commit()
        response = "Deleted action from project"
        return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
