from datetime import datetime
from yards_py.core.base_entity import BaseEntity
from yards_py.domain.entities.league import League
from typing import Optional

from yards_py.core.annotate_args import annotate_args
from yards_py.domain.entities.matchup_preview import MatchupPreview, MatchupPreviewTeam
from yards_py.domain.entities.roster import Roster


@annotate_args
class UserLeaguePreview(BaseEntity):
    user_id: str
    league_name: str
    roster_name: str
    matchup: Optional[MatchupPreview]
    joined: datetime = datetime.now()

    def update_league(self, league: League):
        self.league_name = league.name

    def update_roster(self, roster: Roster):
        self.roster_name = roster.name
        if self.matchup and self.matchup.home and self.matchup.home.id == self.id:
            self.matchup.home.name = roster.name

        if self.matchup and self.matchup.away and self.matchup.away.id == self.id:
            self.matchup.away.name = roster.name

    @staticmethod
    def create(roster: Roster, league: League):
        preview = UserLeaguePreview(
            id=league.id,
            user_id=roster.id,
            league_name=league.name,
            roster_name=roster.name,
            matchup=MatchupPreview(
                home=MatchupPreviewTeam(
                    id=roster.id,
                    name=roster.name
                )
            ))

        return preview
