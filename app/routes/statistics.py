"""
This module contains the routes and functions for generating and displaying
statistics reports for donations and received items.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, jsonify
from app.utils.db import mongo

statistics_bp = Blueprint('statistics', __name__)

REPORTS_FOLDER = 'static/reports'
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)


def generate_statistics_report():
    """
    Generates a statistics report for donations and received items.

    Returns:
        tuple: A tuple containing the report data, the path to the report file, 
               and the path to the chart image file.
    """

    total_donations = mongo.db.donations.count_documents({})

    total_received = mongo.db.tracking.count_documents({"status": "Recebido"})

    donations_by_location = list(
        mongo.db.donations.aggregate([{
            "$group": {
                "_id": "$destination",
                "count": {
                    "$sum": 1
                }
            }
        }]))

    for donation in donations_by_location:
        donation['destination'] = donation.pop('_id')

    if donations_by_location:
        df = pd.DataFrame(donations_by_location)
        df.columns = ['destination', 'Quantidade']
    else:
        df = pd.DataFrame(columns=['destination', 'Quantidade'])

    report_data = {
        'total_donations': total_donations,
        'total_received': total_received,
        'donations_by_location': df.to_dict(orient='records')
    }
    report_path = os.path.join(REPORTS_FOLDER, 'statistics_report.json')
    with open(report_path, 'w') as f:  #pylint: disable=unspecified-encoding
        f.write(pd.json.dumps(report_data, indent=4))  #pylint: disable=no-member

    if not df.empty:
        plt.figure(figsize=(10, 6))
        plt.bar(df['destination'], df['Quantidade'], color='green')
        plt.title('Doações por Local')
        plt.xlabel('Destino')
        plt.ylabel('Quantidade')
        chart_path = os.path.join(REPORTS_FOLDER, 'donations_chart.png')
        plt.savefig(chart_path)
        plt.close()
    else:
        chart_path = None

    return report_data, report_path, chart_path

#EU015
#EU016
@statistics_bp.route('/generate_statistics', methods=['GET'])
def generate_statistics():
    """
    Route to generate the statistics report.

    Returns:
        Response: A JSON response containing a success message, the path to the report file,
                  and the path to the chart image file.
    """
    report_data, report_path, chart_path = generate_statistics_report()  #pylint: disable=unused-variable
    return jsonify({
        'message': 'Relatório gerado com sucesso',
        'report_path': report_path,
        'chart_path': chart_path
    })

#EU015
#EU016
@statistics_bp.route('/statistics', methods=['GET'])
def statistics_page():
    """
    Route to display the statistics report page.

    Returns:
        Response: A rendered HTML template displaying the statistics report and chart.
    """
    report_path = os.path.join(REPORTS_FOLDER, 'statistics_report.json')
    chart_path = os.path.join(REPORTS_FOLDER, 'donations_chart.png')

    if not os.path.exists(report_path):
        return jsonify({
            'message':
            'Relatório não encontrado. Por favor, gere o relatório primeiro.'
        }), 404

    with open(report_path, 'r') as f:  #pylint: disable=unspecified-encoding
        report_data = pd.json.loads(f.read())  #pylint: disable=no-member

    return render_template(
        'statistics.html',
        total_donations=report_data['total_donations'],
        total_received=report_data['total_received'],
        donations_by_location=report_data['donations_by_location'],
        chart_path=chart_path)
