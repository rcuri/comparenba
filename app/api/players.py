from flask import jsonify, request
from app.api import bp
from app.models import Player


@bp.route('/players/<int:id>', methods=['GET'])
def get_player_id(id):
    return jsonify(Player.query.get_or_404(id).to_dict())

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

@bp.route('/players/<string:player_name>', methods=['GET'])
def get_player_name(player_name):
    player = Player.query.filter_by(player_name=player_name.replace('+', ' ')).first_or_404()
    return jsonify(player.to_dict())
