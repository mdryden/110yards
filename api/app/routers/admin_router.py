
from typing import Optional
from api.app.core.auth import require_role
from api.app.core.role import Role
from api.app.core.sim_state import SimState
from api.app.domain.commands.system.update_active_players import (
    UpdateActivePlayersCommand, UpdateActivePlayersCommandExecutor,
    update_active_players_command_executor)
from api.app.domain.commands.system.update_games import UpdateGamesCommand, UpdateGamesCommandExecutor, create_update_games_command_executor
from api.app.domain.services.league_problems_service import (
    LeagueProblemsService, create_league_problems_service)
from api.app.routers.api_router import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

router = APIRouter(prefix="/admin")


@router.get("/problems")
@require_role(Role.admin)
async def problems(
    request: Request,
    league_problems_service: LeagueProblemsService = Depends(create_league_problems_service)
):
    return league_problems_service.get_leagues_with_problems()


@router.post("/update_players")
@require_role(Role.admin)
async def update_players(
    request: Request,
    command_executor: UpdateActivePlayersCommandExecutor = Depends(update_active_players_command_executor)
):
    command = UpdateActivePlayersCommand()
    return command_executor.execute(command)


@router.post("/update_games")
@require_role(Role.admin)
async def update_games(
    request: Request,
    sim_state: Optional[SimState] = None,
    command_executor: UpdateGamesCommandExecutor = Depends(create_update_games_command_executor)
):
    command = UpdateGamesCommand(sim_state=sim_state)
    return command_executor.execute(command)
