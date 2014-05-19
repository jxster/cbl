from . import db
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.hybrid import hybrid_property

player_pos = db.Table('player_positions',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id')),
    db.Column('position_id', db.Integer, db.ForeignKey('positions.id'))
)

team_games = db.Table('team_games',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    positions = db.relationship('Position',
                                secondary=player_pos,
                                backref=db.backref('players', lazy='dynamic'),
                                lazy='dynamic')
    gamelogs = db.relationship('Gamelog', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player %r>' % (self.name)


class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    @staticmethod
    def insert_positions():
        positions = {
            1: 'Point Guard',
            2: 'Shooting Guard',
            3: 'Small Forward',
            4: 'Power Forward',
            5: 'Center'
        }
        for p in positions:
            position = Position.query.filter_by(id=p).first()
            if position is None:
                position = Position(id=p, name=positions[p])
            db.session.add(position)
        db.session.commit()

    def __repr__(self):
        return '%r' % (self.name)


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    conference = db.Column(db.String(120), nullable=False)
    players = db.relationship('Player', backref='team', lazy='dynamic')

    @hybrid_property
    def wins(self):
        return self.games.filter_by(win_id=self.id).count()

    @wins.expression
    def wins(cls):
        return select([func.count(Game.id)]) .\
                where(Game.win_id == cls.id)

    # TODO fix this property
    @hybrid_property
    def losses(self):
        return self.games.filter_by(los_id=self.id).count()

    @losses.expression
    def losses(cls):
        return select([func.count(Game.id)]) .\
                where(Game.los_id == cls.id)

    def __repr__(self):
        return '<Team %r>' % (self.name)


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    court = db.Column(db.Integer)
    win_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    los_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    win_scr = db.Column(db.Integer, default=0)
    los_scr = db.Column(db.Integer, default=0)
    teams = db.relationship('Team',
                            secondary=team_games,
                            backref=db.backref('games', lazy='dynamic'),
                            lazy='dynamic')
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    # change to use **kwargs
    @staticmethod
    def add_game(team1, team2, court, time):
        t1 = Team.query.filter_by(name=team1).first()
        t2 = Team.query.filter_by(name=team2).first()
        try:
            game = Game(teams=[t1, t2], court=court,
                        date=datetime.strptime(time, "%m/%d/%Y %H:%M%p"))
        except AttributeError:
            print "A team didn't exist"
        else:
            # everything went ok? finish the db actions
            db.session.add_all([t1, t2, game])
            db.session.commit()

    # update to handle any number of game updates:
    # e.g. time, date, scores, etc etc
    def update_game(self, winning_nm, win_scr, los_scr):
        try:
            assert int(win_scr) > int(los_scr)
            game = Game.query.filter_by(id=self.id).first()
            winner = self.teams.filter_by(name=winning_nm).first()
            loser = self.teams.filter(Team.name != winning_nm).first()
            game.win_id = winner.id
            game.los_id = loser.id
            game.win_scr = int(win_scr)
            game.los_scr = int(los_scr)
        except AssertionError:
            print "Winning score gotta be higher, son"
        except ValueError:
            print "You sure you entered numbers?"
        else:
            # everything went ok? finish the db actions
            db.session.add(game)
            db.session.commit()

    # helper function for instances of games, used in team view
    def get_opponent(self, teamid):
        return self.teams.filter(Team.id != teamid).first().name


class Gamelog(db.Model):
    __tablename__ = 'gamelogs'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    fga = db.Column(db.Integer, default=0)
    fgm = db.Column(db.Integer, default=0)
    threes_a = db.Column(db.Integer, default=0)
    threes_m = db.Column(db.Integer, default=0)
    rebs = db.Column(db.Integer, default=0)
    asts = db.Column(db.Integer, default=0)
    stls = db.Column(db.Integer, default=0)
    blks = db.Column(db.Integer, default=0)
    tos = db.Column(db.Integer, default=0)
    pts = db.Column(db.Integer, default=0)
    starter = db.Column(db.Boolean, default=False)
