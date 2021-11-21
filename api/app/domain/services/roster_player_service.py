

from api.app.domain.enums.position_type import PositionType
from api.app.domain.entities.league_transaction import LeagueTransaction
from api.app.domain.repositories.league_transaction_repository import LeagueTransactionRepository, create_league_transaction_repository
from api.app.domain.repositories.league_roster_repository import LeagueRosterRepository, create_league_roster_repository
from api.app.domain.entities.roster import Roster
from typing import Tuple

from api.app.domain.entities.league_position import LeaguePosition
from api.app.domain.entities.owned_player import OwnedPlayer
from api.app.domain.entities.player import Player
from api.app.domain.repositories.league_owned_player_repository import (
    LeagueOwnedPlayerRepository, create_league_owned_player_repository)
from fastapi.param_functions import Depends
from google.cloud.firestore_v1.transaction import Transaction


def create_roster_player_service(
        league_owned_player_repo: LeagueOwnedPlayerRepository = Depends(create_league_owned_player_repository),
        roster_repo: LeagueRosterRepository = Depends(create_league_roster_repository),
        league_transaction_repo: LeagueTransactionRepository = Depends(create_league_transaction_repository),
):
    return RosterPlayerService(
        league_owned_player_repo,
        roster_repo=roster_repo,
        league_transaction_repo=league_transaction_repo)


class RosterPlayerService:
    def __init__(
        self,
        league_owned_player_repo: LeagueOwnedPlayerRepository,
        roster_repo: LeagueRosterRepository,
        league_transaction_repo: LeagueTransactionRepository,
    ):
        self.league_owned_player_repo = league_owned_player_repo
        self.roster_repo = roster_repo
        self.league_transaction_repo = league_transaction_repo

    def find_position_for(self, player: Player, roster: Roster) -> LeaguePosition:

        # this might just be for drafting - but I think we only want to auto-assign a position which is an active roster slot (eg: not bye, not ir)
        positions = list(roster.positions.values())
        positions.sort(key=lambda x: int(x.id))

        for position in positions:
            if not position.position_type.is_active_position_type():
                continue

            if position.player:
                continue

            if position.position_type.is_eligible_for(player.position):
                return position

    def assign_player_to_roster(
        self,
        league_id: str,
        roster: Roster,
        player: Player,
        transaction: Transaction = None,
        target_position: LeaguePosition = None,
        record_transaction: bool = False,
        waiver_bid: int = None
    ) -> Tuple[bool, str]:
        position = target_position or self.find_position_for(player, roster)

        if not position:
            return False, "Unable to find position for player"

        if player.position == PositionType.qb and roster.count_qbs() == 1 and not self.dropping(PositionType.qb, target_position):
            return False, "Rosters are limited to 1 quarterback"

        if player.position == PositionType.rb and roster.count_rbs() == 1 and not self.dropping(PositionType.rb, target_position):
            return False, "Rosters are limited to 1 running back"

        if player.position == PositionType.k and roster.count_kickers() == 1 and not self.dropping(PositionType.k, target_position):
            return False, "Rosters are limited to 1 kicker"

        self.assign_player_to_roster_position(league_id, roster, player, position, transaction, record_transaction=record_transaction, waiver_bid=waiver_bid)

        return True, None

    def dropping(self, type: PositionType, target_position: LeaguePosition) -> bool:
        return target_position.player and target_position.player.position == type

    def assign_player_to_roster_position(
            self,
            league_id: str,
            roster: Roster,
            player: Player,
            position: LeaguePosition,
            transaction: Transaction = None,
            record_transaction: bool = False,
            waiver_bid: int = None,
    ):
        drop_player: Player = None
        if position.player:
            drop_player = position.player
            self.league_owned_player_repo.delete(league_id, drop_player.id, transaction)

        position.player = player
        owned_player = OwnedPlayer.create(roster.id, player)
        roster.active_player_count += 1

        self.league_owned_player_repo.set(league_id, owned_player, transaction)
        self.roster_repo.set(league_id, roster, transaction)

        if record_transaction:
            if drop_player:
                drop_transaction = LeagueTransaction.drop_transaction(league_id, roster, drop_player)
                self.league_transaction_repo.create(league_id, drop_transaction, transaction)

            if waiver_bid is not None:
                add_transaction = LeagueTransaction.waiver_claim_transaction(league_id, roster, player, waiver_bid)
            else:
                add_transaction = LeagueTransaction.add_transaction(league_id, roster, player)
            self.league_transaction_repo.create(league_id, add_transaction, transaction)

    def remove_player_from_roster(
        self,
        league_id: str,
        roster: Roster,
        player_id: str,
        transaction: Transaction = None
    ):

        for position_id in roster.positions:
            position = roster.positions[position_id]
            if not position.player or position.player.id != player_id:
                continue

            position.player = None

        active_filled_positions = [position for position in roster.positions.values() if position.player and position.position_type.is_active_position_type()]
        roster.active_player_count = len(active_filled_positions)

        self.league_owned_player_repo.delete(league_id, player_id, transaction)
        self.roster_repo.set(league_id, roster, transaction)
