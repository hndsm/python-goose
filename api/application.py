from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import render_template
from decorators import authenticate
from lib.goose_api import GooseAPI
import json

import goose.exceptions
import traceback

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.route("/")
def root():
    return redirect(url_for('swagger'))

@app.route("/api")
def api():
    pass # SwaggerUI helper URL

@app.route("/api/extract.json")
@authenticate.requires_auth
def extract():
    try:
        extracted_content = GooseAPI(request.args.get('url')).extract()
        return Response(json.dumps(extracted_content), mimetype='application/json')
    except goose.exceptions.SSLError as error:
        return Response(json.dumps({'success': False, 'error': 'SSL error: ' + str(error)}), mimetype='application/json', status= '495')
    except goose.exceptions.SSLDomainError as error:
        return Response(json.dumps({'success': False, 'error': 'SSL domain error: ' + str(error)}), mimetype='application/json', status= '495')
    except goose.exceptions.NotAuthorizedError as error:
        return Response(json.dumps({'success': False, 'error': str(error)}), mimetype='application/json', status= '401')
    except goose.exceptions.ConnectionError as error:
        return Response(json.dumps({'success': False, 'error': str(error)}), mimetype='application/json', status= '403')
    except goose.exceptions.NotFoundError as error:
        return Response(json.dumps({'success': False, 'error': 'Page not found'}), mimetype='application/json', status= '404')
    except goose.exceptions.TimeoutError as error:
        return Response(json.dumps({'success': False, 'error': str(error)}), mimetype='application/json', status= '408')
    except goose.exceptions.UnexpectedRedirectError as error:
        return Response(json.dumps({'success': False, 'error': str(error)}), mimetype='application/json', status= '307')
    except goose.exceptions.TooManyRedirectsError as error:
        return Response(json.dumps({'success': False, 'error': str(error)}), mimetype='application/json', status= '308')
    except goose.exceptions.DatabaseError as error:
        return Response(json.dumps({'success': False, 'error': 'Database error: ' + str(error)}), mimetype='application/json', status= '500')    
    except goose.exceptions.UnknownError as error:
        return Response(json.dumps({'success': False, 'error': 'Remote server Internal error'}), mimetype='application/json', status= '500')              
    except Exception as error:
    	print traceback.format_exc().splitlines()
        return Response(json.dumps({'success': False, 'error': 'Goose Internal server error: ' + str(error)}), mimetype='application/json', status= '500')  

    

@app.route('/swagger')
@authenticate.requires_auth
def swagger():
    return render_template('/api/documentation/show.html')

@app.route('/api/documentation/endpoints/<name>')
@authenticate.requires_auth
def documentation_endpoints(name=None):
    return render_template('/api/documentation/endpoints/%s' % name, mimetype='application/json')

@app.route('/api/documentation/<name>')
@authenticate.requires_auth
def documentation(name=None):
    return render_template('/api/documentation/%s.json' % name, mimetype='application/json')


if __name__ == "__main__":
    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)
    app.run(debug=True, use_reloader=True)
