from flask import Flask, render_template
import sqlite3
import pandas as pd
import plotly
import json
import utils as ut

app = Flask(__name__)

# Route for serving the dashboard
# http://127.0.0.1:5000/
@app.route('/mews-dasboard')
def dashboard():

    # Load config dict
    config = ut.load_config()

    # Connect to the SQLite database
    conn = sqlite3.connect(config['db_name'])
    
    # Query the database to fetch the required data
    df = pd.read_sql_query("SELECT * FROM reservations", conn)
    
    # Close the connection to the database
    conn.close()
    
    line_chart_data = ut.get_line_chart_data(df)

    # Process the data and create Plotly figures
    line_fig = ut.create_line_chart(df)
    stacked_bar_bs_fig = ut.create_stacked_bar_chart(df, 'BUSINESSSEGMENTID')
    stacked_bar_purpose_fig = ut.create_stacked_bar_chart(df, 'PURPOSE')
    
    # Convert the figures to JSON for rendering in the HTML template
    line_graph_json = json.dumps(line_fig, cls=plotly.utils.PlotlyJSONEncoder)
    stacked_bar_bs_json = json.dumps(stacked_bar_bs_fig, cls=plotly.utils.PlotlyJSONEncoder)
    stacked_bar_purpose_json = json.dumps(stacked_bar_purpose_fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template, passing the data and JSON strings
    return render_template('dashboard.html', 
                           line_chart_data=line_chart_data,
                           line_graph_json=line_graph_json,
                           stacked_bar_bs_json=stacked_bar_bs_json,
                           stacked_bar_purpose_json=stacked_bar_purpose_json)

if __name__ == '__main__':
    # Load config dict
    config = ut.load_config()
    ut.update_data()
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
