
from typing import Optional
from services.api.app.config.settings import Settings, get_settings
from yards_py.domain.entities.user import User
from services.api.app.domain.enums.login_type import LoginType
from services.api.app.domain.repositories.user_repository import UserRepository, create_user_repository
from fastapi import Depends
from yards_py.core.annotate_args import annotate_args
from yards_py.core.base_command_executor import BaseCommand, BaseCommandResult, BaseCommandExecutor
from firebase_admin import auth
from firebase_admin.exceptions import InvalidArgumentError
from firebase_admin.auth import UserRecord
from yards_py.core.logging import Logger
from yards_py.core.publisher import Publisher
from services.api.app.di import create_publisher


def create_register_email_command_executor(
    user_repository: UserRepository = Depends(create_user_repository),
    publisher: Publisher = Depends(create_publisher),
    settings: Settings = Depends(get_settings),
):
    return RegisterCommandExecutor(user_repository, publisher, settings.is_dev())


@annotate_args
class RegisterEmailCommand(BaseCommand):
    display_name: str
    email: str


@annotate_args
class RegisterEmailResult(BaseCommandResult[RegisterEmailCommand]):
    user_id: Optional[str]


class RegisterCommandExecutor(BaseCommandExecutor[RegisterEmailCommand, RegisterEmailResult]):

    def __init__(self, user_repository: UserRepository, publisher: Publisher, is_dev: bool):
        self.user_repository = user_repository
        self.publisher = publisher
        self.is_dev = is_dev

    def on_execute(self, command: RegisterEmailCommand) -> RegisterEmailResult:

        existing = self.user_repository.get_by_email(command.email)

        if existing:
            return RegisterEmailResult(command=command, error="A user with that email already exists")

        try:
            result = auth.create_user(display_name=command.display_name, email=command.email)  # type: UserRecord
        except auth.EmailAlreadyExistsError:
            return RegisterEmailResult(command=command, error="A user with that email already exists")
        except InvalidArgumentError as ex:
            message = ex.args[0] if hasattr(ex, "args") and len(ex.args) > 0 else "Unable to create user account (validation error)"
            Logger.warn(message, exc_info=ex)
            return RegisterEmailResult(command=command, error=message)
        except Exception as ex:
            Logger.error("Create user call failed", exc_info=ex)
            return RegisterEmailResult(command=command, error="Unable to create user account (unknown error)")

        if self.is_dev:
            # In live, this is handled by a background cloud function triggered after the registration
            user = User(id=result.uid, display_name=command.display_name, email=command.email, login_type=LoginType.EMAIL, confirmed=True)
            self.user_repository.create(user)

        return RegisterEmailResult(command=command, user_id=result.uid)
