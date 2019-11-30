from app import create_app, db, cli
from app.models import Player


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """
    When flask shell command runs, it will invoke this function and register
    the items returned by it in the shell session.
    """
    return {'db': db, 'Player': Player}
