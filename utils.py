import yaml
import pandas as pd 
import plotly.express as px
import utils as ut
import mews_api as ma
import db_utils as db

CONFIG_FNAME = 'config.yaml'

def load_config():
    # Load configuration from YAML file
    config_dict = {}
    with open(CONFIG_FNAME, 'r') as config_file:
        config = yaml.safe_load(config_file)
        config_dict['url'] = config['mews']['url']
        config_dict['client_token'] = config['mews']['client_token']
        config_dict['access_token'] = config['mews']['access_token']
        config_dict['record_limit'] = config['mews']['record_limit']
        config_dict['client'] = config['mews']['client']
        config_dict['db_name'] = config['database']['db_name']
        config_dict['host'] = config['app']['host']
        config_dict['port'] = config['app']['port']
        config_dict['debug'] = config['app']['debug']

    return config_dict

def process_mews_data(data):
    """
    Process data from Mews.
    """
    formatted_data = []
    for d in data['Reservations']:
        formatted_data.append({
            'ID': d['Id'], 
            # 'ENTERPRISEID': d['EnterpriseId'], 
            'STATE': d['State'], 
            'ORIGIN': d['Origin'], 
            'CREATEDUTC': d['CreatedUtc'],
            'BUSINESSSEGMENTID': d['BusinessSegmentId'],
            'PURPOSE': d['Purpose']
        })

    return formatted_data

def get_line_chart_data(df):
    df_copy = df.copy()
    df_copy['Month'] = df_copy['CREATEDUTC'].str[:7]
    
    # Aggregate count of ID by CREATEDUTC
    line_df = df_copy.groupby(df_copy['Month'])['ID'].count().reset_index().to_dict(orient='records')
    
    return line_df

def create_line_chart(df):
    # Convert CREATEDUTC to datetime
    df['CREATEDUTC'] = pd.to_datetime(df['CREATEDUTC'])
    
    # Aggregate count of ID by CREATEDUTC
    line_df = df.groupby(df['CREATEDUTC'].dt.date)['ID'].count().reset_index()
    
    # Create a line chart using Plotly Express with a modern template
    line_fig = px.line(
        line_df, x='CREATEDUTC', y='ID',
        title='Daily Reservation Volumes',
        template='plotly_white', # You can also try 'plotly_dark', 'ggplot2', 'seaborn', etc.
        markers=True
    )

    # Customize the layout
    line_fig.update_layout({
        'xaxis_title': 'Date',
        'yaxis_title': 'Volume',
        'plot_bgcolor': 'rgba(173, 216, 230, 0.2)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'title': {
            'x': 0.5,
            'xanchor': 'center'
        },
        'font': {
            'family': "Helvetica, Arial, sans-serif",
            'size': 14,
            'color': '#7f7f7f'
        }
    })

    return line_fig

def create_stacked_bar_chart(df, category):
    # Convert CREATEDUTC to datetime
    df['CREATEDUTC'] = pd.to_datetime(df['CREATEDUTC'])
    
    # Aggregate count by CREATEDUTC and the given category
    bar_df = df.groupby([df['CREATEDUTC'].dt.date, category]).size().reset_index(name='counts')
    
    # Create a stacked bar chart using Plotly Express with a modern template
    stacked_bar_fig = px.bar(
        bar_df, x='CREATEDUTC', y='counts', color=category,
        title=f'Daily Volumes by {category}',
        template='plotly_white',
        category_orders={category: sorted(bar_df[category].unique())} # Ensures consistent color mapping
    )

    # Customize the layout
    stacked_bar_fig.update_layout({
        'xaxis_title': 'Date',
        'yaxis_title': 'Volume',
        'plot_bgcolor': 'rgba(173, 216, 230, 0.2)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'title': {
            'x': 0.5,
            'xanchor': 'center'
        },
        'font': {
            'family': "Helvetica, Arial, sans-serif",
            'size': 14,
            'color': '#7f7f7f'
        },
        'legend': {
            'title_text': '',
            'bgcolor': 'rgba(0,0,0,0)',
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -1.0,
            'xanchor': 'center',
            'x': 0.5
        }
    })

    return stacked_bar_fig


def update_data():
    raw_data = ma.get_api_data()
    formatted_data = ut.process_mews_data(raw_data)
    db.insert_into_reservations_table(formatted_data)