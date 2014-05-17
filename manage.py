#!/usr/bin/env python
import os
import sys
from app import create_app, db
from app.models import Player, Position, Team, Game, Gamelog
from flask.ext.script import Manager, Server, Shell


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#TODO: add different options
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, Player=Player, Position=Position,
        Team=Team, Game=Game, Gamelog=Gamelog)


@manager.command
def create_tbls():
    db.drop_all()
    db.create_all()
    populate()


@manager.command
def populate():
    Position.insert_positions()
    seven = Team(name="7th Time Still No Good", conference="Zhang")
    wb = Team(name="Wolf of Ballstreet", conference="Zhang")
    wt = Team(name="Witness This", conference="Zhang")
    db.session.add_all([seven, wb, wt])
    db.session.commit()


manager.add_command("shell", Shell(make_context=make_shell_context))

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


if __name__ == '__main__':
    manager.run()
