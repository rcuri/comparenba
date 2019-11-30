from flask import current_app
from elasticsearch_dsl import Search


def add_to_index(index, model):
    """Add NBA player name to elasticsearch index."""
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Remove NBA player name from elasticsearch index."""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """
    Search elasticsearch index according to provided query.

    List will be returned with paginated search results; total search results
    found will be returned; elasticsearch dict 'search' will be returned in
    case you want to parse more information in the future.
    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': 1000})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total'], search
