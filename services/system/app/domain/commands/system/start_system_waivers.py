

from services.system.app.di import create_publisher
from yards_py.core.publisher import Publisher

from yards_py.domain.entities.state import Locks, State
from datetime import datetime, timedelta
from yards_py.domain.repositories.public_repository import PublicRepository, create_public_repository
from fastapi import Depends
from yards_py.core.annotate_args import annotate_args
from yards_py.core.base_command_executor import BaseCommand, BaseCommandResult, BaseCommandExecutor
from firebase_admin.firestore import firestore
from google.cloud.firestore import Transaction


def create_start_system_waivers_command_executor(
    public_repo: PublicRepository = Depends(create_public_repository),
    publisher: Publisher = Depends(create_publisher),
):
    return StartSystemWaiversCommandExecutor(
        public_repo=public_repo,
        publisher=publisher,
    )


@annotate_args
class StartSystemWaiversCommand(BaseCommand):
    current_week_number: int


@annotate_args
class StartSystemWaiversResult(BaseCommandResult[StartSystemWaiversCommand]):
    state: State
    completed_week_number: int


class StartSystemWaiversCommandExecutor(BaseCommandExecutor[StartSystemWaiversCommand, StartSystemWaiversResult]):
    def __init__(
        self,
        public_repo: PublicRepository,
        publisher: Publisher,
    ):
        self.public_repo = public_repo
        self.publisher = publisher

    def on_execute(self, command: StartSystemWaiversCommand) -> StartSystemWaiversResult:
        @firestore.transactional
        def enable_waivers(transaction: Transaction):
            state = self.public_repo.get_state(transaction)
            state.waivers_active = True
            state.waivers_end = datetime.now().today() + timedelta(days=1)
            state.locks = Locks.reset()
            completed_week_number = command.current_week_number
            state.current_week = completed_week_number + 1

            self.public_repo.set_state(state, transaction)

            return StartSystemWaiversResult(command=command, state=state, completed_week_number=completed_week_number)

        transaction = self.public_repo.firestore.create_transaction()
        return enable_waivers(transaction)
