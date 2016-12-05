import logging

from flask import (
    Flask
)

logger = logging.getLogger('dispatcher')

app = Flask(__name__)

