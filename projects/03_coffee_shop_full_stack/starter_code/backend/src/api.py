import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def drinks_get():
    try:
        drinkList = Drink.query.all()
        shortList = []
        for drink in drinkList:
            # there seems to be a problem with the short function
            shortList.append(drink.short())

        return ({
            'success': True,
            'drinks': shortList
        })
    except Exception as e:
        print(f'Exception in adding new drink: {e}')
        abort(500)


@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def drinks_details_get(payload):
    try:
        drinkList = Drink.query.all()
        longList = []
        for drink in drinkList:
            longList.append(drink.long())

        return ({
            'success': True,
            'drinks': longList
        })

    except Exception as e:
        abort(500)


@app.route('/drinks', methods=["POST"])
@requires_auth(permission='post:drinks')
def drinks_post(payload):
    req_in = request.json

    if not all([x in req_in for x in ['title', 'recipe']]):
        abort(422)

    title = req_in['title']
    recipe = json.dumps(req_in['recipe'])
    try:
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
    except Exception as e:
        print(f'Exception in adding new drink: {e}')
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def drinks_update(payload, id):
    drink = Drink.query.get_or_404(id)
    req_in = request.json

    if('recipe' in req_in):
        recipe = json.dumps(req_in['recipe'])
        drink.recipe = recipe
    if('title' in req_in):
        title = req_in['title']
        drink.title = title
    try:
        drink.update()
    except Exception as e:
        print(f'Exception in editing a drink: {e}')

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def drinks_delete(payload, id):
    drink = Drink.query.get_or_404(id)
    try:
        drink.delete()
    except Exception as e:
        print(f'Exception in deleting a drink: {e}')
        abort(422)

    return jsonify({
        "success": True,
        "delete": id
    })


@app.errorhandler(AuthError)
def auth_error(excpt):
    response = jsonify(excpt.error)
    response.status_code = excpt.status_code
    return response


@app.errorhandler(400)
def bad_request(error):
    '''Server cannot process request due to malformed request'''
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    '''Authentication not provided'''
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    '''Server is refusing action'''
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(404)
def not_found(error):
    '''not found on the server'''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    '''Catch all server error'''
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
