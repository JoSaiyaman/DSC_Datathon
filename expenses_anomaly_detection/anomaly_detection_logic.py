import numpy as np
import pandas as pd
from datetime import datetime

def string_to_date(field):
    def to_date(row):
        date_str = row[field]
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return date
        except:
            return None
    return to_date
def anomaly_triggered_week_n(week, year, user_id, previous_data):
    """
    previous_data must contain "fecha_objeto" column
    user_id: int
    """
    transactions_user_id = previous_data[previous_data["id_cliente"] == user_id]
    sorted_transactions = transactions_user_id.sort_values(by="fecha_objeto", inplace=False)
    
    sorted_transactions["semana"] = sorted_transactions.apply(lambda x: x["fecha_objeto"].isocalendar()[1], axis=1)
    sorted_transactions["anio"] = sorted_transactions.apply(lambda x: x["fecha_objeto"].year, axis=1)
    
    result = {}
    for index, row in sorted_transactions.iterrows():
        current_year = int(row["anio"])
        current_week = int(row["semana"])
        
        if (current_week, current_year) not in result:
            result[(current_week, current_year)] = row["monto_transaccion"]
        else:
            result[(current_week, current_year)] = result[(current_week, current_year)] + row["monto_transaccion"]

    if (week, year) not in result:
        return None
            
    week_sums = []
    for key in result.keys():
        accum_year = key[1]
        accum_week = key[0]
        
        if accum_year < year:
            week_sums.append(result[(accum_week, accum_year)])
        
        if accum_year == year and accum_week < week:
            week_sums.append(result[(accum_week, accum_year)])
            
            
    spent_this_week = result[(week, year)]
    
    std = np.std(week_sums)
    average = sum(week_sums)/len(week_sums)
    z_score = (spent_this_week - average)/std
    return z_score >= 2

def get_table_ready(table):
    table["fecha_objeto"] = table.apply(string_to_date("fecha_transaccion"), axis=1)
    return table