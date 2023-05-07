from anomaly_detection_logic import *

from flask import Flask
from flask_restful import Resource, Api, request

import numpy as np
import pandas as pd
from datetime import datetime

table = pd.read_csv("dataset_transacc_tdc_tdd_20230309.csv")
app = Flask(__name__)
api = Api(app)

table = get_table_ready(table)

class Anomaly(Resource):

    def get(self):
        client_id = None
        year = None
        week = None

        try:
            client_id = int(request.args.get("client_id"))
            year = int(request.args.get("year"))
            week = int(request.args.get("week"))
        except:
            return "Ha habido un error. Los parametros proporcionados son inválidos.", 400

        output = anomaly_triggered_week_n(week, year, client_id, table)

        result = ""

        if output is None:
            return "Ha habido un error. La semana no fue encontrada", 400, 
        
        if output:
            result = "¡Hey! Parece ser que la semana pasada gastaste más de lo normal. ¿Está todo bien?"
        else:
            result = "¡Hey! Tus gastos semanales estuvieron dentro de los rangos normales. ¡Sigue así!"

        return result, 200  # return data and 200 OK code


api.add_resource(Anomaly, '/anomaly')

if __name__ == '__main__':
    app.run()  # run our Flask app