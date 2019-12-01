from flask import jsonify, request, url_for
from app.api import bp
from app.api.auth import auth
from app.models import Player
from app.api.errors import bad_request
from app import db, cache


@bp.route('/players/<int:id>', methods=['GET'])
@cache.cached()
def get_player_id(id):
    """
    Queries database for player corresponding to provided primary key (id)
    in URL and returns JSON response if found. Otherwise, returns a 404 error.
    """
    return jsonify(Player.query.get_or_404(id).to_dict())


# TODO change this to elasticsearch to account for players with same name
@bp.route('/players/<string:player_name>', methods=['GET'])
def get_player_name(player_name):
    """
    Queries database for player corresponding to provided player name in URL
    and returns player as JSON response if found. Otherwise, returns 404
    error.
    """
    player = Player.query.filter_by(
        player_name=player_name.replace('+', ' ')).first_or_404()
    return jsonify(player.to_dict())


@bp.route('/players/index/', methods=['GET'])
@cache.cached()
def get_all_players():
    """
    Queries database for the entire player table, paginates results, and
    returns JSON response.
    """
    page = request.args.get('page', 1, type=int)
    per_page = max(request.args.get('per_page', 50, type=int), 10)
    data = Player.to_collection_dict(
        Player.query, page, per_page, 'api.get_all_players')
    return jsonify(data)


@bp.route('/players/index/<string:startswith>', methods=['GET'])
def get_player_list_letter(startswith):
    """
    Queries database for all the players whose first name begins with the
    'startswith' character. Returns paginated results as JSON response.
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    data = Player.to_collection_dict(
        Player.query.filter(Player.player_name.startswith(startswith[0])),
        page, per_page, 'api.get_player_list_letter',
        startswith=startswith[0])
    return jsonify(data)


@bp.route('/players/search/<string:player_name>', methods=['GET'])
def search_players(player_name):
    """
    Queries elasticsearch server for 'player_name' parameter. Returns list of
    players matching query, along with total matches found, as a JSON
    response.
    """
    per_page = 1000
    page = 1
    players = Player.search_to_dict(
        Player.search(player_name, page, per_page))
    return jsonify(players)


@bp.route('/players/delete/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_player(id):
    """
    Requires user authentication (username:password) in order to access
    function.

    If authenticated:
    Deletes player resource specified by primary key (id) in URL if player
    matching ID is found and returns deleted player JSON representation. If
    player not found, returns 404 error response.

    If not authenticated:
    Returns a 401 error response.
    """
    player = Player.query.filter_by(id=id).first_or_404()
    data = player.to_dict()
    db.session.delete(player)
    db.session.commit()
    return jsonify(data)


@bp.route('/players', methods=['POST'])
@auth.login_required
def add_player():
    """
    Requires user authentication (username:password) in order to access
    function.

    If authenticated:
    Accepts player representation in JSON format from client, provided in
    request body. If mandatory fields (player_name) are not present, returns
    a bad_request error. Otherwise, creates a player object and adds it to
    database. Returns the newly created player representation, with 201
    status code and a Location header with the URL of the new resource.

    If not authenticated:
    Returns a 401 error response.
    """
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
    """
    Requires user authentication (username:password) in order to access
    function.

    If authenticated:
    Queries database by player's primary key (id) in URL and returns 404 error
    if player not found. Otherwise, use Player's from_dict() method to
    import data provided by the client, and commit the change to the
    database. Returns the updated player representation to the client with
    a 200 status code.

    If not authenticated:
    Returns a 401 error response.
    """
    player = Player.query.get_or_404(id)
    data = request.get_json() or {}
    player.from_dict(data)
    db.session.commit()
    return jsonify(player.to_dict())
