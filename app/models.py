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

    @hybrid_property
    def fga(self):
        return sum(g.fga for g in self.gamelogs)

    @fga.expression
    def fga(cls):
        return select(func[sum(Gamelog.fga)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def fgm(self):
        return sum(g.fgm for g in self.gamelogs)

    @fgm.expression
    def fgm(cls):
        return select(func[sum(Gamelog.fgm)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def threes_a(self):
        return sum(g.threes_a for g in self.gamelogs)

    @threes_a.expression
    def threes_a(cls):
        return select(func[sum(Gamelog.threes_a)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def threes_m(self):
        return sum(g.threes_m for g in self.gamelogs)

    @threes_m.expression
    def threes_m(cls):
        return select(func[sum(Gamelog.threes_m)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def rebs(self):
        return sum(g.rebs for g in self.gamelogs)

    @rebs.expression
    def rebs(cls):
        return select(func[sum(Gamelog.rebs)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def asts(self):
        return sum(g.asts for g in self.gamelogs)

    @asts.expression
    def asts(cls):
        return select(func[sum(Gamelog.asts)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def stls(self):
        return sum(g.stls for g in self.gamelogs)

    @stls.expression
    def stls(cls):
        return select(func[sum(Gamelog.stls)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def blks(self):
        return sum(g.blks for g in self.gamelogs)

    @blks.expression
    def blks(cls):
        return select(func[sum(Gamelog.blks)]) .\
                where(Player.id == cls.id)

    @hybrid_property
    def tos(self):
        return sum(g.tos for g in self.gamelogs)

    @tos.expression
    def tos(cls):
        return select(func[sum(Gamelog.tos)]) .\
                where(Player.id == cls.id)

    @staticmethod
    def add_player(name, team, positions):
        try:
            player = Player.query.filter_by(name=name).first()
            if player is None:
                teamid = Team.query.filter_by(name=team).first().id
                pos = []
                for num in positions:
                    pos.append(Position.query.filter_by(id=num).first())
                assert teamid

                player = Player(name=name, team_id=teamid, positions=pos)
        except AssertionError:
            print "Team didn't exist"
            db.rollback()
        else:
            db.session.add(player)
            db.session.commit()

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
        return '%s' % (self.name)


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    conference = db.Column(db.String(120), nullable=False)
    players = db.relationship('Player', backref='team', lazy='dynamic')
    gm = db.Column(db.String(120), nullable=False)

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

    @staticmethod
    def add_game(**kwargs):
        teams = kwargs["teams"]
        court = int(kwargs["court"])
        time = datetime.strptime(kwargs["time"], "%m/%d/%Y %H:%M%p")
        t1 = Team.query.filter_by(name=str(teams[0])).first()
        t2 = Team.query.filter_by(name=str(teams[1])).first()
        try:
            game = Game(teams=[t1, t2], court=court, date=time)
        except AttributeError:
            print "A team didn't exist"
            db.rollback()
        else:
            # everything went ok? finish the db actions
            db.session.add_all([t1, t2, game])
            db.session.commit()

    # update to handle any number of game updates:
    # e.g. time, date, scores, etc etc
    @staticmethod
    def update_game(court, time, winning_nm, win_scr, los_scr):
        try:
            assert int(win_scr) > int(los_scr)
            game = Game.query.filter_by(date=datetime.strptime(time,
                                        "%m/%d/%Y %H:%M%p")).\
                   filter_by(court=int(court)).first()
            winner = game.teams.filter_by(name=winning_nm).first()
            loser = game.teams.filter(Team.name != winning_nm).first()
            game.win_id = winner.id
            game.los_id = loser.id
            game.win_scr = int(win_scr)
            game.los_scr = int(los_scr)
        except AttributeError:
            print "Seems like the game didn't exist"
            db.rollback()
        except AssertionError:
            print "Winning score gotta be higher, son"
            db.rollback()
        except ValueError:
            print "You sure you entered numbers?"
            db.rollback()
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
    pid = db.Column(db.Integer, db.ForeignKey('players.id'))
    gid = db.Column(db.Integer, db.ForeignKey('games.id'))
    fga = db.Column(db.Integer, default=0)
    fgm = db.Column(db.Integer, default=0)
    threes_a = db.Column(db.Integer, default=0)
    threes_m = db.Column(db.Integer, default=0)
    rebs = db.Column(db.Integer, default=0)
    asts = db.Column(db.Integer, default=0)
    stls = db.Column(db.Integer, default=0)
    blks = db.Column(db.Integer, default=0)
    tos = db.Column(db.Integer, default=0)
    starter = db.Column(db.Boolean, default=False)

    @staticmethod
    def add_gamestats(date, name, fga, fgm, threesa, threesm,
                      rebs, asts, stls, blks, tos, start):
        try:
            assert fga > fgm, threesa > threesm
            player = Player.query.filter_by(name=name).first()
            team = Team.query.filter_by(id=player.team_id).first()
            game_id = team.games.filter_by(date=datetime.strptime(date,
                                           "%m/%d/%Y %H:%M%p")).first().id

            if game_id is None:
                raise ValueError
            log = Gamelog(pid=player.id, gid=game_id, fga=fga, fgm=fgm,
                          threes_a=threesa, threes_m=threesm, rebs=rebs,
                          asts=asts, stls=stls, blks=blks, tos=tos, starter=start)
        except AttributeError:
            print "No such player exists!"
            db.session.rollback()
        except ValueError:
            print "Didn't have a game at this time"
            db.session.rollback()
        except AssertionError:
            print "Check your math"
            db.session.rollback()
        else:
            db.session.add(log)
            db.session.commit()
