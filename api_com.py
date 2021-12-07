import datetime
import os
from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from src.utils import creds as cred

# import json

# from src.utils.general import get_db_conn_sql_alchemy

# mysql://username:password@server/db
# "postgresql://postgres:Equ1p0_2@rds-dpa.cheenr0nt3eh.us-east-2.rds.amazonaws.com:5432/food"

# db_conn_str = get_db_conn_sql_alchemy('../../conf/local/credentials.yaml')

db_conn_str = f'postgresql://{os.environ["PGUSR"]}:{os.environ["PGPASS"]}@db:5432/postgres'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn_str
api = Api(app)
db = SQLAlchemy(app)


class DataCCD(db.Model):
    __table_args__ = {'schema': 'clean'}
    __tablename__ = 'variables'

    mopllaag = db.Column(db.Integer, primary_key=True)
    mink123m = db.Column(db.Integer)
    ppersaut = db.Column(db.Integer)
    pwaoreg = db.Column(db.Integer)
    pbrand = db.Column(db.Integer)
    aplezier = db.Column(db.Integer)
    afiets = db.Column(db.Integer)
    caravan = db.Column(db.Integer)
    date_ing = db.Column(db.DateTime)

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


all_data = api.model("data_CCP", {
    'mopllaag': fields.Integer,
    'mink123m': fields.Integer,
    'ppersaut': fields.Integer,
    'pwaoreg': fields.Integer,
    'pbrand': fields.Integer,
    'aplezier': fields.Integer,
    'afiets': fields.Integer,
    'caravan': fields.Integer,
    'date_ing': fields.Date
})

all_data_list = api.model('all_data_clean', {
    'all_data': fields.Nested(all_data)
})


# endpoints
@api.route('/')
class ApiInfo(Resource):
    def get(self):
        return {'Api_CCD': 'Api de Computacion para Ciencia de Datos'}


@api.route('/all_data/')
class AllData(Resource):
    @api.marshal_with(all_data_list, as_list=True)
    def get(self):
        all_d = DataCCD.query.all()
        a_d = []
        for element in all_d:
            a_d.append({
                'mopllaag': element.mopllaag,
                'mink123m': element.mink123m,
                'ppersaut': element.ppersaut,
                'pwaoreg': element.pwaoreg,
                'pbrand': element.pbrand,
                'aplezier': element.aplezier,
                'afiets': element.afiets,
                'caravan': element.caravan,
                'date_ing': element.date_ing
            })

        return {'all_data': a_d}


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", debug=True, port=8080)
