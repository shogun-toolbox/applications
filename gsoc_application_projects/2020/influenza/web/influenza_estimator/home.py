from datetime import timedelta, date
from pathlib import Path
from . import util
import pageviewapi
from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__, url_prefix='/home')
data = util.DataGateway()


@bp.route('/')
def display():
    estimates = data.get_incidence()
    estimates = util.calculate_count(estimates)
    return render_template('home.html', estimates=estimates)
