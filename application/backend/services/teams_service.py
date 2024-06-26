from fastapi import HTTPException

from db.crud import teams_crud


class TeamService:
    @staticmethod
    def get_all_teams(db):
        return teams_crud.get_teams(db)

    @staticmethod
    def get_team(db, team_id):
        team = teams_crud.get_team(db, team_id)
        if not team:
            raise HTTPException(
                status_code=404, detail=f"Team with id {team_id} not found"
            )
        return team

    @staticmethod
    def get_team_projects(db, team_id):
        TeamService.get_team(db, team_id)

        return teams_crud.get_team_projects(db, team_id)
