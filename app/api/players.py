from flask import jsonify, request, url_for
from app.api import bp
from app.api.auth import auth
from app.models import Player
from app.api.errors import bad_request
from app import db


@bp.route('/players/<int:id>', methods=['GET'])
def get_player_id(id):
    return jsonify(Player.query.get_or_404(id).to_dict())

@bp.route('/players/<string:player_name>', methods=['GET'])
def get_player_name(player_name):
    player = Player.query.filter_by(player_name=player_name.replace('+', ' ')).first_or_404()
    return jsonify(player.to_dict())

@bp.route('/players/index/', methods=['GET'])
def get_all_players():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    data = Player.to_collection_dict(Player.query, page, per_page, 'api.get_all_players')
    return jsonify(data)

@bp.route('/players/index/<string:startswith>', methods=['GET'])
def get_player_list_letter(startswith):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    data = Player.to_collection_dict(
                    Player.query.filter(Player.player_name.startswith(startswith)),
                    page, per_page, 'api.get_player_list_letter', startswith=startswith)
    return jsonify(data)

@bp.route('/players/search/<string:player_name>', methods=['GET'])
def search_players(player_name):
    per_page = 1000
    page = 1
    players = Player.search_to_dict(Player.search(player_name, page, per_page))
    return jsonify(players)

@bp.route('/players/delete/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_player(id):
    player = Player.query.filter_by(id=id).first_or_404()
    data = player.to_dict()
    db.session.delete(player)
    db.session.commit()
    return jsonify(data)

@bp.route('/players', methods=['POST'])
@auth.login_required
def add_player():
    data = request.get_json() or {}
    if 'player_name' not in data:
        return bad_request('Must include player_name field')
    player = Player()
    player.from_dict(data)
    db.session.add(player)
    db.session.commit()
    response = jsonify(player.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_player_id', id=player.id)
    return response

@bp.route('/players/update/<int:id>', methods=['PUT'])
@auth.login_required
def update_player(id):
    player = Player.query.get_or_404(id)
    data = request.get_json() or {}
    player.from_dict(data)
    db.session.commit()
    return jsonify(player.to_dict())
