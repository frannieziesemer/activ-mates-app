from flask import Blueprint, jsonify, request
from activmatesApp.models import Activity


# instance of blueprint
apis = Blueprint("apis", __name__)


# JSON API route
# here i can set a route to create an api url
# within the function i will create a dictionary using the db data and return this dictionary as json (jsonify)


@apis.route("/api/get_activities")
def api_all():
    # here the lat, lng, and radius is called from the API url created in js file
    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))
    radius = int(request.args.get("radius"))
    # explanation of request.args.get():
    # https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

    activites = Activity.get_activities_within_radius(lat=lat, lng=lng, radius=radius)
    output = []
    for item in activites:
        output.append(item.to_dict())
    return jsonify(output)
