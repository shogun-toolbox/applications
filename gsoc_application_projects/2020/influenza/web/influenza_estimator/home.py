from datetime import timedelta, date
from pathlib import Path

import pageviewapi
from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/')
def display():
    estimates = 0
    return render_template('home.html', estimates=estimates)
