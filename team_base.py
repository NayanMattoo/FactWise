from flask import Flask, request, jsonify
from user import UserManagement
from team import TeamManagement
from project_board import ProjectBoardManagement

app = Flask(__name__)

user_management = UserManagement()
team_management = TeamManagement()
project_board_management = ProjectBoardManagement()

@app.route('/users', methods=['POST'])
def create_user():
    request_data = request.get_json()
    try:
        response = user_management.create_user(json.dumps(request_data))
        return jsonify(json.loads(response)), 201
    except ValueError as e:
        return str(e), 400

@app.route('/users', methods=['GET'])
def list_users():
    response = user_management.list_users()
    return jsonify(json.loads(response))

@app.route('/users/<user_id>', methods=['GET'])
def describe_user(user_id):
    try:
        response = user_management.describe_user(json.dumps({"id": user_id}))
        return jsonify(json.loads(response))
    except ValueError as e:
        return str(e), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    request_data = request.get_json()
    try:
        response = user_management.update_user(json.dumps({"id": user_id, "user": request_data}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

@app.route('/users/<user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    try:
        response = user_management.get_user_teams(json.dumps({"id": user_id}))
        return jsonify(json.loads(response))
    except ValueError as e:
        return str(e), 404

@app.route('/teams', methods=['POST'])
def create_team():
    request_data = request.get_json()
    try:
        response = team_management.create_team(json.dumps(request_data))
        return jsonify(json.loads(response)), 201
    except ValueError as e:
        return str(e), 400

@app.route('/teams', methods=['GET'])
def list_teams():
    response = team_management.list_teams()
    return jsonify(json.loads(response))

@app.route('/teams/<team_id>', methods=['GET'])
def describe_team(team_id):
    try:
        response = team_management.describe_team(json.dumps({"id": team_id}))
        return jsonify(json.loads(response))
    except ValueError as e:
        return str(e), 404

@app.route('/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    request_data = request.get_json()
    try:
        response = team_management.update_team(json.dumps({"id": team_id, "team": request_data}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

@app.route('/teams/<team_id>/users', methods=['POST'])
def add_users_to_team(team_id):
    request_data = request.get_json()
    try:
        response = team_management.add_users_to_team(json.dumps({"id": team_id, "users": request_data["users"]}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

@app.route('/teams/<team_id>/users', methods=['DELETE'])
def remove_users_from_team(team_id):
    request_data = request.get_json()
    try:
        response = team_management.remove_users_from_team(json.dumps({"id": team_id, "users": request_data["users"]}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

@app.route('/teams/<team_id>/users', methods=['GET'])
def list_team_users(team_id):
    try:
        response = team_management.list_team_users(json.dumps({"id": team_id}))
        return jsonify(json.loads(response))
    except ValueError as e:
        return str(e), 404

@app.route('/boards', methods=['POST'])
def create_board():
    request_data = request.get_json()
    try:
        response = project_board_management.create_board(json.dumps(request_data))
        return jsonify(json.loads(response)), 201
    except ValueError as e:
        return str(e), 400

@app.route('/boards/<board_id>/close', methods=['POST'])
def close_board(board_id):
    try:
        response = project_board_management.close_board(json.dumps({"id": board_id}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

@app.route('/boards/<board_id>/tasks', methods=['POST'])
def add_task(board_id):
    request_data = request.get_json()
    try:
        response = project_board_management.add_task(json.dumps(request_data))
        return jsonify(json.loads(response)), 201
    except ValueError as e:
        return str(e), 400

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task_status(task_id):
    request_data = request.get_json()
    try:
        response = project_board_management.update_task_status(json.dumps({"id": task_id, "status": request_data["status"]}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

@app.route('/teams/<team_id>/boards', methods=['GET'])
def list_boards(team_id):
    try:
        response = project_board_management.list_boards(json.dumps({"id": team_id}))
        return jsonify(json.loads(response))
    except ValueError as e:
        return str(e), 404

@app.route('/boards/<board_id>/export', methods=['POST'])
def export_board(board_id):
    try:
        response = project_board_management.export_board(json.dumps({"id": board_id}))
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)