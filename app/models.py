from app import db
from flask import url_for
from app.search import add_to_index, remove_from_index, query_index
from passlib.apps import custom_app_context as pwd_context


class SearchableMixin(object):
    """
    Mixin SearchableMixin that gives any model with mixin attached the
    ability to automatically manage an associated full-text index.
    """
    @classmethod
    def search(cls, expression, page, per_page):
        """
        Extend query_index function in order to replace list of object IDs
        with actual objects.
        """
        ids, total, res = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0, 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        # Return results in order from more relevant to less relevant
        # This is done by using CASE SQL statement to ensure results from
        # database are the same order as the order of IDs returned
        return cls.query.filter(cls.id.in_(ids)).order_by(
                db.case(when, value=cls.id)), total, res

    @classmethod
    def before_commit(cls, session):
        """
        Method will respond to SQLAlchemy event triggered before a commit
        takes place. We save objects that will be added, modified, or
        deleted in order to update Elasticsearch index after commit.
        """
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        """
        Method will respond to SQLAlchemy event triggered after a commit
        takes place. After successful commit, we update the Elasticsearch
        index with changes saved in before_commit.
        """
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """Refresh an index will all the data from database."""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# Event handlers to make SQLAlchemy call the before_commit and after_commit
# methods before and after a commit, respectively
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class PaginatedAPIMixin(object):
    """
    Mixin PaginatedAPIMixin to represent any collection of resources using
    pagination logic.
    """
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """
        Produce a dictionary from a collection of resources.
        'query' is a Flask-SQLAlchemy query object.
        'page' represents the current page.
        'per_page' represents the number of results to return per page.
        'endpoint' is the API endpoint for a particular view function.
        """
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

    @staticmethod
    def search_to_dict(query):
        """Return results from an elasticsearch query object as a dict."""
        # TODO Add _meta and _links
        resources = query[0]
        total = query[1]
        data = {
            'items': [item.to_dict() for item in resources],
            'total': total
        }
        return data


class Player(SearchableMixin, PaginatedAPIMixin, db.Model):
    """
    NBA Player model.

    SearchableMixin gives Player model ability to
    automatically manage an associated full-text index. The __searchable__
    variable indicates which fields are to be indexed.

    PaginatedAPIMixin gives Player model ability to represent a group of
    players as a collection of paginated results.
    """
    __searchable__ = ['player_name']
    id = db.Column(db.Integer, primary_key=True)
    player_image = db.Column(db.String(50), nullable=True)
    player_name = db.Column(db.String(100), index=True)
    position = db.Column(db.String(100))
    first_nba_season = db.Column(db.SmallInteger, nullable=True)
    field_goal_made = db.Column(db.Float(31), nullable=True)
    field_goal_attempted = db.Column(db.Float(31), nullable=True)
    field_goal_pct = db.Column(db.Float(21), nullable=True)
    three_pt_made = db.Column(db.Float(31), nullable=True)
    three_pt_attempted = db.Column(db.Float(31), nullable=True)
    three_pt_pct = db.Column(db.Float(21), nullable=True)
    free_throw_made = db.Column(db.Float(31), nullable=True)
    free_throw_attempted = db.Column(db.Float(31), nullable=True)
    free_throw_pct = db.Column(db.Float(21), nullable=True)
    true_stg_pct = db.Column(db.Float(21), nullable=True)
    points = db.Column(db.Float(21), nullable=True)
    off_reb = db.Column(db.Float(21), nullable=True)
    def_reb = db.Column(db.Float(21), nullable=True)
    tot_reb = db.Column(db.Float(21), nullable=True)
    assists = db.Column(db.Float(21), nullable=True)
    steals = db.Column(db.Float(21), nullable=True)
    blocks = db.Column(db.Float(21), nullable=True)
    turnovers = db.Column(db.Float(21), nullable=True)

    def to_dict(self):
        """
        Return a dictionary representation of a Player resource in order to
        structure data in a JSON format.
        """
        data = {
            'id': self.id,
            'player_name': self.player_name,
            'player_image': self.player_image,
            'positions': self.position,
            'first_nba_season': self.first_nba_season,
            'shooting': {
                'field_goal_made': self.field_goal_made,
                'field_goal_attempted': self.field_goal_attempted,
                'field_goal_pct': self.field_goal_pct,
                'three_pt_made': self.three_pt_made,
                'three_pt_attempted': self.three_pt_attempted,
                'three_pt_pct': self.three_pt_pct,
                'free_throw_made': self.free_throw_made,
                'free_throw_attempted': self.free_throw_attempted,
                'free_throw_pct': self.free_throw_pct,
                'true_stg_pct': self.true_stg_pct,
                'points': self.points
            },
            'off_reb': self.off_reb,
            'def_reb': self.def_reb,
            'tot_reb': self.tot_reb,
            'assists': self.assists,
            'steals': self.steals,
            'blocks': self.blocks,
            'turnovers': self.turnovers,
            '_links': {
                'self': url_for('api.get_player_id', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        """
        When client passes a player representation as a dictionary in a
        request, parse it and convert it to a Player object.
        """
        for field in  Player.__table__.columns.keys():
            if field != 'id' and field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        """Represent a Player instance using their full name."""
        return '<Player: {}>'.format(self.player_name)


class User(db.Model):
    """
    Registered User model. Password functions to help authenticate user when
    accessing restricted resources.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        """Hash password with provided hashing function (pwd_context.hash)."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """
        Decrypt password using provided hashing function (pwd_context.verify)
        to verify password.
        """
        return pwd_context.verify(password, self.password_hash)
