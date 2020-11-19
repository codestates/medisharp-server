from flask import Blueprint

#from ..models import Site

users = Blueprint('users', __name__)

from . import view

# @users.url_value_preprocessor
# def post_login('/<string:email>', values):
    #query = Site.query.filter_by(subdomain=values.pop('site_subdomain'))
    #g.site = query.first_or_404()
