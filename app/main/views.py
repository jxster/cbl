from flask import render_template, flash, redirect
from sqlalchemy import asc, desc
from . import main
from .. import db
from ..models import Player, Position, Team, Game


@main.route('/')
def home():
    teams = Team.query.all()
    return render_template('home.html', teams=teams)


@main.route('/standings')
@main.route('/teams')
def standings():
    teams = Team.query.order_by(desc(Team.wins)).all()
    return render_template('standings.html', teams=teams)


@main.route('/teams/<team_name>')
def team(team_name):
    team = Team.query.filter_by(name=team_name).first()
    games = team.games.all()
    for g in games:
        g.opponent = g.get_opponent(team.id)
    players = team.players.all()
    return render_template('team.html', players=players, games=games,
                           id=team.id, name=team_name)


@main.route('/schedule')
def schedule():
    games = Game.query.all()
    return render_template('schedule.html', games=games)
