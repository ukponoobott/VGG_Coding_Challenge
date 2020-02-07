from flask import Flask, jsonify, request, session
import os
import sqlite3


DATABASE = "./database.db"


app = Flask(__name__)

app.secret_key = os.urandom(24)


if not os.path.exists(DATABASE):

    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING NOT NULL UNIQUE, password STRING NOT NULL)')

    conn.execute('CREATE TABLE projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, project_name STRING NOT NULL UNIQUE, '
                 'description STRING NOT NULL, completed INTEGER')
    conn.execute('CREATE TABLE actions (actions_id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER,'
                 ' FOREIGN KEY(project_id) REFERENCES projects(projects_id)CONSTRAINT fk_projects '
                 'description STRING, note STRING')
    conn.commit()


@app.route("/api/users/register", methods=["POST"])
def register():
    reg_details = request.get_json()
    username = reg_details["username"]
    password = reg_details["password"]

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
        con.commit()
        response = "Success"

    return response


@app.route("/api/users/auth")
def auth():
    pass


@app.route("/api/projects", methods=["GET", "POST"])
def projects():
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * from projects")
        rows = cur.fetchall()
        return jsonify(rows)

    elif request.method == "POST":
        project_details = request.get_json()
        project_name = project_details["name"]
        description = project_details["description"]
        completed = project_details["completed"]

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO projects(project_name, description, completed) VALUES (?, ?)', (project_name,
                        description, completed))
            con.commit()
            response = "Success"
            return jsonify(response)


@app.route("/api/projects/<int:project_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def project(project_id):
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM projects where project_id = %s", project_id)
        rows = cur.fetchone()
        return jsonify(rows)
    elif request.method == "PATCH":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE * FROM projects where project_id = %s", project_id)


@app.route("/api/projects/<int:project_id>/actions", methods=["GET", "POST"])
def project_actions(project_id):
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM actions where project_id = %s", project_id)
        rows = cur.fetchall()
        return jsonify(rows)

    elif request.method == "POST":
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


@app.route("/api/projects/<int:project_id>/actions/<int:action_id>", methods=["GET", "PUT", "DELETE"])
def project_actions_update(project_id, action_id):
    if request.method == "GET":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM actions where project_id = %s AND action_id = %s", (project_id, action_id))
        rows = cur.fetchone()
        return jsonify(rows)
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE * FROM actions where project_id = %s AND action_id = %s", (project_id, action_id))
    else:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=4000)
