from flask import (make_response, jsonify, current_app as app,
                    request)
from functools import wraps

# Decorator to allow access only with the use of APP Key.
def app_key_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    print(f"Args: {args}\nKwargs: {kwargs}")
    if request.args.get('app_key') != app.config['APP_KEY']:
      response = { "message": "Invalid Credentials !" }
      return make_response(jsonify(response), 404)
    return f(*args, **kwargs)
  return wrapper