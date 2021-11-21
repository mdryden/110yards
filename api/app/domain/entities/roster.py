from __future__ import annotations
from datetime import datetime
from functools import cmp_to_key

from api.app.domain.entities.waiver_bid import WaiverBid
from api.app.domain.enums.position_type import PositionType
from api.app.domain.entities.league_position import LeaguePosition
from typing import Dict, List, Optional, Union
from api.app.core.annotate_args import annotate_args
from api.app.core.base_entity import BaseEntity


@annotate_args
class Roster(BaseEntity):
    name: str
    draft_budget: Optional[int]
    current_matchup: Optional[str]
    positions: Dict[str, LeaguePosition] = {}
    record: str = "0-0"
    points_for: float = 0.0
    points_against: float = 0.0
    transaction_count: int = 0
    last_week_result = "-"
    waiver_budget: int = 100
    active_player_count: int = 0
    this_week_points_for: float = 0.0
    this_week_bench_points_for: float = 0.0
    waiver_bids: List[WaiverBid] = []
    processed_waiver_bids: List[WaiverBid] = []
    wins: int = 0
    losses: int = 0
    ties: int = 0
    wl_points: int = 0
    rank: int = 1
    name_changes_banned: bool = False

    def find_player_position(self, player_id: str) -> Union[LeaguePosition, None]:
        for position_id in self.positions:
            position = self.positions[position_id]
            if position.player and position.player.id == player_id:
                return position

    def calculate_score(self) -> float:
        score = 0.0

        for position_id in self.positions:
            position = self.positions[position_id]

            if position.is_starting_position_type():
                score += position.game_score

        return score

    def calculate_bench_score(self) -> float:
        score = 0.0

        for position_id in self.positions:
            position = self.positions[position_id]

            if not position.is_starting_position_type():
                score += position.game_score

        return score

    def count_position_player(self, type: PositionType, ignore_reserve=True) -> int:
        return len([
            position for position in self.positions.values() if
            position.player and position.player.position == type
            and (not ignore_reserve or not position.is_reserve_type())
        ])

    def count_qbs(self) -> int:
        return self.count_position_player(PositionType.qb)

    def count_rbs(self) -> int:
        return self.count_position_player(PositionType.rb)

    def count_kickers(self) -> int:
        return self.count_position_player(PositionType.k)

    @staticmethod
    def calculate_wl_points(roster: Roster) -> float:
        return (roster.wins * 2) + roster.ties

    @staticmethod
    def format_record(roster: Roster) -> str:
        if roster.ties:
            return f"{roster.wins}-{roster.losses}-{roster.ties}"
        else:
            return f"{roster.wins}-{roster.losses}"

    @staticmethod
    def sort(rosters: List[Roster]):
        return sorted(rosters, key=cmp_to_key(Roster.compare))

    @staticmethod
    def compare(roster1: Roster, roster2: Roster):
        if roster1.wl_points > roster2.wl_points:
            return -1

        if roster1.wl_points < roster2.wl_points:
            return 1

        if roster1.points_for > roster2.points_for:
            return -1

        if roster1.points_for < roster2.points_for:
            return 1

        roster1_diff = roster1.points_for - roster1.points_against
        roster2_diff = roster2.points_for - roster2.points_against

        if roster1_diff > roster2_diff:
            return -1

        if roster1_diff < roster2_diff:
            return 1

        # tied!
        tiebreak = int((datetime.now() - datetime(1, 1, 1)).total_seconds())

        if tiebreak % 2 == 0:
            return 1
        else:
            return -1
