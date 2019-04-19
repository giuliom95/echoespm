from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask import render_template

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
        row = [ct]
        table.append(row)
        contents = data[ct]
        if len(contents) == 0:
            continue
        row += list(contents.values())[0].keys()
        for c in contents:
            row = [c]
            for rt in contents[c]:
                ver, status = contents[c][rt]
                if ver == None:
                    ver = 0
                row.append(ver)
            table.append(row)
    
    return render_template('project_overview.jinja2', table=table)
    

