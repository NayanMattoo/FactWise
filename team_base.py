# team.py
import json
import os
from datetime import datetime
from base import TeamBase

class TeamManagement(TeamBase):
    def __init__(self, db_path='db'):
        self.db_path = db_path
        self.teams_file = os.path.join(db_path, 'teams.json')
        self.users_file = os.path.join(db_path, 'users.json')
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.teams_file):
            self.teams = []
        else:
            with open(self.teams_file, 'r') as f:
                self.teams = json.load(f)

        if not os.path.exists(self.users_file):
            self.users = []
        else:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)

    def save_data(self):
        with open(self.teams_file, 'w') as f:
            json.dump(self.teams, f)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def create_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = len(self.teams) + 1
        team_name = request_data['name']
        
        # Constraints validation
        if any(team['name'] == team_name for team in self.teams):
            raise ValueError("Team name must be unique")
        if len(team_name) > 64:
            raise ValueError("Team name can be max 64 characters")
        if 'description' in request_data and len(request_data['description']) > 128:
            raise ValueError("Description can be max 128 characters")
        
        new_team = {
            "id": team_id,
            "name": team_name,
            "description": request_data.get("description", ""),
            "creation_time": datetime.now().isoformat(),
            "admin": request_data["admin"],
            "users": [request_data["admin"]]
        }
        self.teams.append(new_team)
        self.save_data()
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams_list = [{
            "id": team["id"],
            "name": team["name"],
            "description": team["description"],
            "creation_time": team["creation_time"],
            "admin": team["admin"]
        } for team in self.teams]
        return json.dumps(teams_list)

    def describe_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data["id"]
        
        team = next((t for t in self.teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        
        return json.dumps({
            "id": team["id"],
            "name": team["name"],
            "description": team["description"],
            "creation_time": team["creation_time"],
            "admin": team["admin"]
        })

    def update_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data["id"]
        new_team_data = request_data["team"]
        
        team = next((t for t in self.teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        
        if "name" in new_team_data and any(t['name'] == new_team_data['name'] for t in self.teams if t["id"] != team_id):
            raise ValueError("Team name must be unique")
        if "name" in new_team_data and len(new_team_data["name"]) > 64:
            raise ValueError("Team name can be max 64 characters")
        if "description" in new_team_data and len(new_team_data["description"]) > 128:
            raise ValueError("Description can be max 128 characters")
        
        team.update(new_team_data)
        self.save_data()
        return json.dumps({})

    def add_users_to_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data["id"]
        new_users = request_data["users"]
        
        team = next((t for t in self.teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        if len(team["users"]) + len(new_users) > 50:
            raise ValueError("Cannot add more than 50 users to a team")
        
        team["users"].extend(new_users)
        self.save_data()
        return json.dumps({})

    def remove_users_from_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data["id"]
        users_to_remove = request_data["users"]
        
        team = next((t for t in self.teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        
        team["users"] = [user for user in team["users"] if user not in users_to_remove]
        self.save_data()
        return json.dumps({})

    def list_team_users(self, request: str):
        request_data = json.loads(request)
        team_id = request_data["id"]
        
        team = next((t for t in self.teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        
        users_list = [{"id": user, "name": user, "display_name": user} for user in team["users"]]
        return json.dumps(users_list)