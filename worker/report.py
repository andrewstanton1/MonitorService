from flask import Flask, request, jsonify
from sqlalchemy import  create_engine, MetaData, Table
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
ma = Marshmallow(app)
basedir = os.path.abspath(os.path.dirname(__file__))

def loadSession():
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'crud.sqlite'))
    metadata = MetaData()
    with engine.connect() as connection:
        report = Table('report', metadata, autoload=True, autoload_with=engine)
        result = [row for row in connection.execute("SELECT message, timestamp FROM report")]
    return result

class ReportSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('message', 'timestamp')


report_schema = ReportSchema()
report_schema = ReportSchema(many=True)

@app.route("/report", methods=["GET"])
def get_report():
    try:
        rows = loadSession()
    except:
        return "No data", '400'

    result = report_schema.dump(rows)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5002)