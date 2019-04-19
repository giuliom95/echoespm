from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask import render_template
from flask import url_for

from db import db

app = Flask(__name__)
dbconn = db()

import re


@app.route('/content/<project>/', methods=['GET'])
def project_overview(project):
    data = dbconn.getProjectOverview(project)

    # Tableify data
    table = []
    for ct in data:
        row = [{'class': 'content_type', 'text': ct}]
        table.append({'class': 'header_row', 'content': row})
        contents = data[ct]
        if len(contents) == 0:
            continue
        row += [
            {'class': 'resource_type', 'text': rt} 
            for rt in list(contents.values())[0].keys()
        ]
        for c in contents:
            row = [{'class': 'content_name', 'text': c}]
            for rt in contents[c]:
                ver, status = contents[c][rt]
                if ver == None:
                    ver = '---'
                    status = 'no_version'
                else:
                    ver = f'v{ver:0>3}'
                row.append({'class': f'version {status}', 'text': ver})
            table.append({'class': 'normal_row', 'content': row})
    
    css_path = url_for('static', filename='style.css')
    return render_template('project_overview.jinja2', table=table, css=css_path)
    

