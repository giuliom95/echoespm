from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

from db import db

app = Flask(__name__)
dbconn = db()

import re


@app.route('/content/', methods=['GET'])
def handle_content_type_list():
    data = dbconn.get_content_types_list()
    return jsonify(data)


@app.route('/content/<content_type>', methods=['GET', 'POST'])
def handle_content_type(content_type):
    if request.method == 'GET':
        try:
            data = dbconn.get_content_type(content_type)
            return jsonify(data)
        except KeyError:
            abort(404)
    elif request.method == 'POST':
        try:
            dbconn.add_content_type(content_type)
        except ValueError:
            abort(409)
        return '', 204


@app.route('/content/<content_type>/', methods=['GET'])
def handle_contents_list(content_type):
    try:
        data = dbconn.get_contents_list(content_type)
        return jsonify(data)
    except KeyError:
        abort(404)


@app.route('/content/<content_type>/<content_name>', methods=['GET', 'POST'])
def handle_content(content_type, content_name):
    if request.method == 'GET':
        try:
            data = dbconn.get_content(content_type, content_name)
            return jsonify(data)
        except KeyError:
            abort(404)
    elif request.method == 'POST':
        try:
            dbconn.add_content(content_type, content_name)
        except KeyError:
            abort(400)
        except ValueError:
            abort(409)
        return '', 204


@app.route('/content/<content_type>/<content_name>/', methods=['GET'])
def handle_resources_list(content_type, content_name):
    try:
        data = dbconn.get_resources_list(content_type, content_name)
        return jsonify(data)
    except KeyError:
        abort(404)


@app.route('/content/<content_type>/<content_name>/<resource_name>', methods=['GET', 'POST'])
def handle_resource(content_type, content_name, resource_name):
    if request.method == 'GET':
        try:
            data = dbconn.get_resource(content_type, content_name, resource_name)
            return jsonify(data)
        except KeyError:
            abort(404)
    elif request.method == 'POST':
        try:
            dbconn.add_resource(content_type, content_name, resource_name)
        except KeyError:
            abort(400)
        except ValueError:
            abort(409)
        return '', 204


@app.route('/content/<content_type>/<content_name>/<resource_name>/', methods=['GET'])
def handle_versions_list(content_type, content_name, resource_name):
    try:
        data = dbconn.get_versions_list(content_type, content_name, resource_name)
        return jsonify(data)
    except KeyError:
        abort(404)


@app.route('/content/<content_type>/<content_name>/<resource_name>/<version>', methods=['GET', 'POST'])
def handle_version(content_type, content_name, resource_name, version):
    # Check if version follows the vXXX pattern
    if re.match('^v[0-9]{3}$', version) == None:
        abort(400)
    v_num = int(version[1:])
    if request.method == 'GET':
        try:
            return_deps = request.args.get('dependencies', default=0, type=int) == 1
            data = dbconn.get_version(content_type, content_name, resource_name, v_num, return_deps=return_deps)
            return jsonify(data)
        except KeyError:
            abort(404)
    elif request.method == 'POST':
        try:
            deps = []
            if 'dependencies' in request.form:
                for d in request.form.getlist('dependencies'):
                    if re.match('^([^/]+/){3}[^/]+$', d) == None:
                        abort(400)
                    splitted_d = d.split('/')
                    if re.match('^v[0-9]{3}$', splitted_d[3]) == None:
                        abort(400)
                    splitted_d[3] = int(splitted_d[3][1:])
                    deps.append(tuple(splitted_d))
            dbconn.add_version(content_type, content_name, resource_name, v_num, deps)
        except KeyError:
            abort(400)
        except ValueError:
            abort(409)
        return '', 204
