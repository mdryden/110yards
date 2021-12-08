
import os

import firebase_admin
from api.app.core.firestore_proxy import FirestoreProxy

from api.app.core.publisher import VirtualPubSubPublisher
from api.app.domain.commands.user.register_email import RegisterCommandExecutor, RegisterEmailCommand
from api.app.domain.entities.opponents import Opponents
from api.app.domain.entities.schedule import get_playoff_type_config
from api.app.domain.entities.scoring_info import ScoringInfo
from api.app.domain.entities.state import State
from api.app.domain.entities.switches import Switches
from api.app.domain.enums.position_type import get_position_type_config
from api.app.domain.repositories.public_repository import create_public_repository
from api.app.domain.repositories.user_repository import create_user_repository

DEV_PROJECT_ID = "yards-dev"


# ensure we are set up to use the emulator

os.environ["GCLOUD_PROJECT"] = DEV_PROJECT_ID
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:9000"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"

firebase_admin.initialize_app(options={"projectId": DEV_PROJECT_ID})

publisher = VirtualPubSubPublisher(DEV_PROJECT_ID)

public_repo = create_public_repository()
user_repo = create_user_repository()
firestore = FirestoreProxy(None)

default_switches = Switches()

print("If this script takes more than a few seconds, the emulator may not be running (or is not running on port 9000)")
print("In this case, press CTRL+C to stop, then run 'npm run start:emulators' in a different terminal and try again.")
print()
print("Configuring default switches...")
public_repo.set_switches(default_switches)
print("Done")

print("Configuring default state")
state = State.default()
public_repo.set_state(state)

opponents = Opponents.create({})
public_repo.set_opponents(opponents)
print("Done")

print("Creating default admin account...")
command = RegisterEmailCommand(display_name="admin@110yards.dev", email="admin@110yards.dev")
register_command_executor = RegisterCommandExecutor(user_repo, publisher, is_dev=True)
result = register_command_executor.execute(command)

if result.success:
    user = user_repo.get(result.user_id)
    user.is_admin = True
    user_repo.update(user)
print("Done")

count = 1
while count < 8:
    email = f"test{count}@test.com"
    print(f"Creating user '{email}'")
    command = RegisterEmailCommand(display_name=email, email=email)
    register_command_executor.execute(command)
    count += 1

print("Setting up admin stats...")
stats = {"active_league_count": 0, "league_count": 0, "verified_user_count": 0}
ref = firestore.document("admin/stats")
ref.set(stats)
print("Done")

print("Setting up playoff types...")
for item in get_playoff_type_config():
    ref = firestore.document(f"playoff-types/{item['id']}")
    ref.set(item)
print("Done")

print("Setting up position types...")
for item in get_position_type_config():
    ref = firestore.document(f"roster-positions/{item['id']}")
    ref.set(item)
print("Done")

print("Setting up scoring info...")
ref = firestore.document("public/scoring_info")
ref.set(ScoringInfo().dict())
print("Done")

print("Setup script complete")
