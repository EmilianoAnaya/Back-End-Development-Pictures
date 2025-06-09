from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    pictures = {}
    for picture in data:
        pictures[picture["id"]] = picture["pic_url"]
    return pictures, 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if id is None:
        return {"error message" : "There's no ID"}, 404

    try:
        id_formatted = int(id)
        for picture in data:
            if int(picture["id"]) == id_formatted:
                return picture, 200
        
        return {"message" : "The picture was not found"}, 404

    except ValueError:
        return {"error message" : "The ID is in the wrong format"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json

    for picture in data:
        if picture["id"] == int(new_picture["id"]):
            return {"Message": f"picture with id {picture['id']} already present"}, 302
    
    data.append(new_picture)
    return new_picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_picture = request.json

    for i, picture in enumerate(data):
        if picture["id"] == update_picture["id"]:
            data[i] = update_picture
            return update_picture, 201
    
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == int(id):
            data.remove(picture)
            return picture, 204

    return {"message": "picture not found"}, 404
