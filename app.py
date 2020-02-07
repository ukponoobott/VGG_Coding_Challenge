from flask import Flask, jsonify, request, session
import os
import sqlite3


DATABASE = "./database.db"


app = Flask(__name__)

app.secret_key = os.urandom(24)


if not os.path.exists(DATABASE):

    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, password STRING)')
    conn.execute('CREATE TABLE projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, project_name STRING, '
                 'description STRING')
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
        cur.execute("select * from projects")
        rows = cur.fetchall()
        return jsonify(rows)

    elif request.method == "POST":
        project_details = request.get_json()
        project_name = project_details["name"]
        description = project_details["description"]

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO projects(project_name, description) VALUES (?, ?)', (project_name, description))
            con.commit()
            response = "Success"
            return jsonify(response)

    else:
        pass


@app.route("/api/projects/<int:projectId>", methods=["GET", "PATCH", "PUT", "DELETE"])
def project(projectId):
    if request.method == "GET":
        if request.method == "GET":
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("SE * from projects")
            rows = cur.fetchall()
            return jsonify(rows)
    elif request.method == "PATCH":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass


@app.route("/api/projects/<int:projectId>/actions", methods=["GET", "POST"])
def project_actions(projectId):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    else:
        pass


@app.route("/api/actions")
def all_actions():
    pass


@app.route("/api/projects/<int:projectId>/actions/<int:actionId>", methods=["GET", "PUT", "DELETE"])
def project_actions_update(projectId, actionId):
    if request.method == "GET":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=4000)
