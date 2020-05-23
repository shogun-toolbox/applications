import json

from flask import Blueprint

from . import util

bp = Blueprint('api', __name__, url_prefix='/api/v1.0')

data = util.DataGateway()


@bp.route('/all/current/', methods=['GET'])
def get_all_current():
    ans = data.get_incidence()
    return json.dumps(ans)


@bp.route('/all/weekly/estimate/<int:year>/<int:week>/', methods=['GET'])
def get_all_weekly_estimate(year, week):
    ans = data.get_incidence(year=year, week=week)
    return json.dumps(ans)


@bp.route('/all/weekly/incidence/<int:year>/<int:week>/', methods=['GET'])
def get_all_weekly_incidence(year, week):
    ans = data.get_incidence(year=year, week=week, category='incidence')
    return json.dumps(ans)


@bp.route('/specific/current/<string:country>', methods=['GET'])
def get_specific_current(country):
    ans = data.get_incidence(countries=[country])
    return json.dumps(ans)


@bp.route('/specific/weekly/estimate/<int:year>/<int:week>/<string:country>',
          methods=['GET'])
def get_specific_weekly_estimate(year, week, country):
    ans = data.get_incidence(year=year, week=week, countries=[country])
    return json.dumps(ans)


@bp.route('/specific/weekly/incidence/<int:year>/<int:week>/<string:country>',
          methods=['GET'])
def get_specific_weekly_current(year, week, country):
    ans = data.get_incidence(year=year, week=week, countries=[country],
                             category='incidence')
    return json.dumps(ans)
