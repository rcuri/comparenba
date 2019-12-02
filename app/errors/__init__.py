from flask import Blueprint

# Errors blueprint
bp = Blueprint('errors', __name__)

from app.errors import handlers
