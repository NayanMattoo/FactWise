# user.py
import json
import os
from datetime import datetime
from base import UserBase

class UserManagement(UserBase):
    def __init__(self, db_path='db'):
        self.db_path = db_path
        self.users_file = os.path.join(db_path, 'users.json')
        self.teams_file = os.path.join(db_path, 'teams.json')
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.users_file):
            self.users = []
        else:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)

        if not os.path.exists(self.teams_file):
            self.teams = []
        else:
            with open(self.teams_file, 'r') as f:
                self.teams = json.load(f)

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
        with open(self.teams_file, 'w') as f:
            json.dump(self.teams, f)

    def create_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = len(self.users) + 1
        user_name = request_data['name']
        
        # Constraints validation
        if any(user['name'] == user_name for user in self.users):
            raise ValueError("User name must be unique")
        if len(user_name) > 64:
            raise ValueError("User name can be max 64 characters")
        if 'display_name' in request_data and len(request_data['display_name']) > 64:
            raise ValueError("Display name can be max 64 characters")
        
        new_user = {
            "id": user_id,
            "name": user_name,
            "display_name": request_data.get("display_name", ""),
            "creation_time": datetime.now().isoformat()
        }
        self.users.append(new_user)
        self.save_data()
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users_list = [{
            "id": user["id"],
            "name": user["name"],
            "display_name": user["display_name"],
            "creation_time": user["creation_time"]
        } for user in self.users]
        return json.dumps(users_list)

    def describe_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data["id"]
        
        user = next((u for u in self.users if u["id"] == user_id), None)
        if not user:
            raise ValueError("User not found")
        
        return json.dumps({
            "id": user["id"],
            "name": user["name"],
            "display_name": user["display_name"],
            "creation_time": user["creation_time"]
        })

    def update_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data["id"]
        new_user_data = request_data["user"]
        
        user = next((u for u in self.users if u["id"] == user_id), None)
        if not user:
            raise ValueError("User not found")
        
        if "name" in new_user_data:
            raise ValueError("User name cannot be updated")
        if "display_name" in new_user_data and len(new_user_data["display_name"]) > 128:
            raise ValueError("Display name can be max 128 characters")
        
        user.update(new_user_data)
        self.save_data()
        return json.dumps({})

    def get_user_teams(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data["id"]
        
        user_teams = [team for team in self.teams if user_id in team["users"]]
        teams_list = [{
            "id": team["id"],
            "name": team["name"],
            "description": team["description"],
            "creation_time": team["creation_time"]
        } for team in user_teams]
        return json.dumps(teams_list)