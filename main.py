from datetime import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from apscheduler.schedulers.background import BackgroundScheduler

from get_neos import GetNeos

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neo.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Neos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    nasa_jpl_url = db.Column(db.String(255))
    is_potentially_hazardous_asteroid = db.Column(db.String(25))
    date = db.Column(db.DateTime())

    def __repr__(self):
        return '<Neo %s>' % self.name


class NeoSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "nasa_jpl_url", "is_potentially_hazardous_asteroid", "date")


neo_schema = NeoSchema()
neos_schema = NeoSchema(many=True)


def my_scheduled_job():
    neo_data = GetNeos()
    neo_json = neo_data.getneo()
    neos = Neos.query.filter_by(name=neo_json['title']).first()
    if not neos:
        date_dt3 = datetime.strptime(neo_json['date'], '%Y-%m-%d')
        new_post = Neos(
            name=neo_json['title'],
            nasa_jpl_url=neo_json['url'],
            date=date_dt3
        )

        db.session.add(new_post)
        db.session.commit()


sched = BackgroundScheduler(daemon=True)
sched.add_job(my_scheduled_job, 'interval', seconds=5)
sched.start()


class NeoListResource(Resource):
    def get(self):
        neos = Neos.query.all()
        return neos_schema.dump(neos)


api.add_resource(NeoListResource, '/neos/week')


if __name__ == '__main__':
    app.run(debug=True)