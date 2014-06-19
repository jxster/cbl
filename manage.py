#!/usr/bin/env python
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import Player, Position, Team, Game, Gamelog

#TODO: add different options
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    # migrate database to latest revision
    upgrade()


@manager.command
def create_tbls():
    if os.path.exists('dev-db.sqlite'):
        db.drop_all()
    db.create_all()


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

    with app.open_resource('./testing/data/players.json') as playerdata:
        player_dict = json.load(playerdata)['players']
        for p in player_dict:
            Player.add_player(name=p['name'],
                              team=p['team'],
                              positions=p['positions'])
    populate_games()
    populate_stats()

def make_shell_context():
    return dict(app=app, db=db, Player=Player, Position=Position,
                Team=Team, Game=Game, Gamelog=Gamelog)


def populate_teams(teams=None):
    db.session.add_all(teams)
    db.session.commit()


def populate_games():
    with app.open_resource('./testing/data/games.json') as gamedata:
        games = json.load(gamedata)['games']
        for g in games:
            Game.add_game(teams=g['teams'],
                          court=int(g['court']),
                          time=g['time'])
            scrs = g['score'].split(' ')
            Game.update_game(int(g['court']), g['time'],
                             g['winner'], scrs[0], scrs[1])


def populate_stats():
    with app.open_resource('./testing/data/stats.json') as statsdata:
        games_dict = json.load(statsdata)['gamelogs']
        for g in games_dict:
            Gamelog.add_gamestats(date=g['date'], name=g['name'], fga=g['fga'],
                                  fgm=g['fgm'], threesa=g['3pt_a'], threesm=g['3pt_m'],
                                  rebs=g['rebs'], asts=g['asts'], stls=g['stls'],
                                  blks=g['blks'], tos=g['tos'], start=g['start'])


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
