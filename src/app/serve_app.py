import dash
from dash import html, dcc, Input, Output
from src.model.gantt_chart import GanttChart

def create_app():
    """"
    Create the Dash app with the Gantt chart objects

    Parameters:
    None

    Returns:
    app: dash.Dash
    """

    # Create the Dash app
    app = dash.Dash(__name__)

    # Create the Gantt chart objects
    gantt_chart = GanttChart()

    # Create the layout
    app.layout = html.Div([
        html.H1("Gantt Chart with Slippage"),
        dcc.Graph(figure=gantt_chart.create_gantt_chart_with_slippage()),
        html.H1("Current Gantt Chart"),
        dcc.Graph(figure=gantt_chart.create_current_gantt_chart())
    ])

    return app.run_server(debug=True)