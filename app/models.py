from app import db
from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
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


class Player(PaginatedAPIMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
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
            data = {
                'id': self.id,
                'player_name': self.player_name,
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
                'turnovers': self.turnovers
            }
            return data
