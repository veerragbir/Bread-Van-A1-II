import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import Resident, Driver, Street, Schedule, StopRequest
from App.main import create_app
from App.controllers import initialize  # only keep initialize if you still call it

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>

# user_cli = AppGroup('user', help='User object commands') 

# # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(username, password):
#     create_user(username, password)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli

'''
Resident Commands
'''

resident_cli = AppGroup('resident', help='Resident object commands')

@resident_cli.command("create", help="Creates a resident")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("street_id", type=int, default=1)

def create_resident_command(username, password, street_id):
    resident = Resident(username=username, password=password, street_id=street_id)
    db.session.add(resident)
    db.session.commit()
    print(f'Resident {username} created on street {street_id}!')

@resident_cli.command("list", help="Lists residents in the database")
@click.argument("format", default="string")

def list_resident_command(format):
    residents = Resident.query.all()
    if format == 'string':
        print([f"{r.id}: {r.username} on street {r.street_id}" for r in residents])
    else:
        print([{"id": r.id, "username": r.username, "street_id": r.street_id} for r in residents])

app.cli.add_command(resident_cli)

'''
Driver Commands
'''

driver_cli = AppGroup('driver', help='Driver object commands')

@driver_cli.command("add", help="Add a new driver")
@click.argument("username")
@click.argument("password")

def add_driver(username, password):
    driver = Driver(username=username, password=password, status="Idle")
    db.session.add(driver)
    db.session.commit()
    print(f"Driver {username} added!")

@driver_cli.command("status", help="Check driver status")
@click.argument("driver_id", type=int)

def driver_status(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        print({
            "id": driver.id,
            "username": driver.username,
            "status": driver.status,
            "location": driver.location
        })
    else:
        print("Driver not found")

app.cli.add_command(driver_cli)

'''
Street Commands
'''

street_cli = AppGroup('street', help='Street object commands')

@street_cli.command("add", help="Add a new street")
@click.argument("name")

def add_street(name):
    street = Street(name=name)
    db.session.add(street)
    db.session.commit()
    print(f"Street {name} added!")

app.cli.add_command(street_cli)

'''
Schedule Commands
'''

schedule_cli = AppGroup('schedule', help='Schedule object commands')

@schedule_cli.command("add", help="Schedule a drive")
@click.argument("driver_id", type=int)
@click.argument("street_id", type=int)
@click.argument("scheduled_time")

def add_schedule(driver_id, street_id, scheduled_time):
    driver = Driver.query.get(driver_id)
    street = Street.query.get(street_id)
    if not driver:
        print("Driver not found")
        return
    if not street:
        print("Street not found")
        return

    schedule = Schedule(driver_id=driver_id, street_id=street_id, scheduled_time=scheduled_time)
    db.session.add(schedule)
    db.session.commit()
    print(f"Scheduled: Driver {driver.username} -> Street {street.name} at {scheduled_time}")

app.cli.add_command(schedule_cli)

'''
StopRequest Commands
'''

stop_request_cli = AppGroup('stop', help='StopRequest commands')

@stop_request_cli.command("add", help="Create a stop request for a resident")
@click.argument("resident_id", type=int)
@click.argument("schedule_id", type=int)
@click.argument("note", default="")

def add_stop_request(resident_id, schedule_id, note):
    resident = Resident.query.get(resident_id)
    schedule = Schedule.query.get(schedule_id)
    if not resident:
        print("Resident not found")
        return
    if not schedule:
        print("Schedule not found")
        return

    stop_request = StopRequest(resident_id=resident_id, schedule_id=schedule_id, note=note)
    db.session.add(stop_request)
    db.session.commit()
    print(f"Stop request created for Resident {resident.username} on Schedule {schedule.id}")

app.cli.add_command(stop_request_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")

def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)