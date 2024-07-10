# project_board.py
import json
import os
from datetime import datetime
from base import ProjectBoardBase

class ProjectBoard(ProjectBoardBase):
    def __init__(self, db_path='db'):
        self.db_path = db_path
        self.boards_file = os.path.join(db_path, 'boards.json')
        self.tasks_file = os.path.join(db_path, 'tasks.json')
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.boards_file):
            self.boards = []
        else:
            with open(self.boards_file, 'r') as f:
                self.boards = json.load(f)

        if not os.path.exists(self.tasks_file):
            self.tasks = []
        else:
            with open(self.tasks_file, 'r') as f:
                self.tasks = json.load(f)

    def save_data(self):
        with open(self.boards_file, 'w') as f:
            json.dump(self.boards, f)
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f)

    def create_board(self, request: str):
        request_data = json.loads(request)
        board_id = len(self.boards) + 1
        board_name = request_data['name']
        
        # Constraints validation
        if any(board['name'] == board_name for board in self.boards if board['team_id'] == request_data['team_id']):
            raise ValueError("Board name must be unique for a team")
        if len(board_name) > 64:
            raise ValueError("Board name can be max 64 characters")
        if 'description' in request_data and len(request_data['description']) > 128:
            raise ValueError("Description can be max 128 characters")
        
        new_board = {
            "id": board_id,
            "name": board_name,
            "description": request_data.get("description", ""),
            "team_id": request_data["team_id"],
            "creation_time": request_data["creation_time"],
            "status": "OPEN"
        }
        self.boards.append(new_board)
        self.save_data()
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        request_data = json.loads(request)
        board_id = request_data["id"]
        
        board = next((b for b in self.boards if b["id"] == board_id), None)
        if not board:
            raise ValueError("Board not found")
        if any(task["board_id"] == board_id and task["status"] != "COMPLETE" for task in self.tasks):
            raise ValueError("You can only close boards with all tasks marked as COMPLETE")
        
        board["status"] = "CLOSED"
        board["end_time"] = datetime.now().isoformat()
        self.save_data()
        return json.dumps({})

    def add_task(self, request: str) -> str:
        request_data = json.loads(request)
        task_id = len(self.tasks) + 1
        title = request_data['title']
        board_id = request_data['board_id']
        
        # Constraints validation
        if any(task['title'] == title for task in self.tasks if task['board_id'] == board_id):
            raise ValueError("Task title must be unique for a board")
        if len(title) > 64:
            raise ValueError("Task title can be max 64 characters")
        if 'description' in request_data and len(request_data['description']) > 128:
            raise ValueError("Description can be max 128 characters")
        
        board = next((b for b in self.boards if b["id"] == board_id), None)
        if not board or board["status"] != "OPEN":
            raise ValueError("Can only add task to an OPEN board")
        
        new_task = {
            "id": task_id,
            "title": title,
            "description": request_data.get("description", ""),
            "user_id": request_data["user_id"],
            "board_id": board_id,
            "creation_time": request_data["creation_time"],
            "status": "OPEN"
        }
        self.tasks.append(new_task)
        self.save_data()
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str):
        request_data = json.loads(request)
        task_id = request_data["id"]
        status = request_data["status"]
        
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            raise ValueError("Task not found")
        
        task["status"] = status
        self.save_data()
        return json.dumps({})

    def list_boards(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data["id"]
        
        boards = [{"id": b["id"], "name": b["name"]} for b in self.boards if b["team_id"] == team_id and b["status"] == "OPEN"]
        return json.dumps(boards)

    def export_board(self, request: str) -> str:
        request_data = json.loads(request)
        board_id = request_data["id"]
        
        board = next((b for b in self.boards if b["id"] == board_id), None)
        if not board:
            raise ValueError("Board not found")
        
        tasks = [t for t in self.tasks if t["board_id"] == board_id]
        
        output = f"Board: {board['name']}\nDescription: {board['description']}\nStatus: {board['status']}\nTasks:\n"
        for task in tasks:
            output += f"  - {task['title']} ({task['status']}): {task['description']}\n"
        
        out_file = os.path.join('out', f"board_{board_id}.txt")
        with open(out_file, 'w') as f:
            f.write(output)
        
        return json.dumps({"out_file": out_file})

# Create the necessary directories if they don't exist
if not os.path.exists('db'):
    os.makedirs('db')
if not os.path.exists('out'):
    os.makedirs('out')