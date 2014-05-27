#!/usr/bin/env python
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask.ext.script import Manager, Server, Shell
from app import create_app, db
from app.models import Player, Position, Team, Game, Gamelog

#TODO: add different options
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def create_tbls():
    if os.path.exists('dev-db.sqlite'):
        db.drop_all()
    db.create_all()
    populate()


@manager.command
def populate():
    Position.insert_positions()

    with app.open_resource('./testing/data/teams.json') as teamdata:
        team_dict = json.load(teamdata)['teams']
        team_models = []
        for t in team_dict:
            team_models.append(Team(name=t['name'],
                                    conference=t['conference'],
                                    gm=t['gm']))
        populate_teams(team_models)
    populate_players()
    populate_games()


def make_shell_context():
    return dict(app=app, db=db, Player=Player, Position=Position,
                Team=Team, Game=Game, Gamelog=Gamelog)


def populate_teams(teams=None):
    db.session.add_all(teams)
    db.session.commit()


def populate_players(teams=None, players=None):
    if teams is None:
        teams = Team.query.all()

    if players is None:
        players = ['Jack Li', 'Taotao Zhang', 
                   'Justin Choi', 'Yilei Yang',
                   'Tony Lian', 'YJ Gahng',
                   'Wayne Tie', 'Ruben Ornelas',
                   'Jesse Smith', 'Keenan Pontoni',
                   'Saul Vaca', 'James McGhee']

    while len(players) > 0:
        for t in teams:
            if len(players) > 0:
                Player.add_player(players.pop(), t.name, [3,4])



def populate_games():
    pass


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
