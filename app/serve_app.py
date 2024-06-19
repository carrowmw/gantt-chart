import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.model.gantt_chart import GanttChart


def serve_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    gantt_chart = GanttChart()

    left_config_column = dbc.Col(
        children=[
            dcc.Dropdown(
                id="chart-dropdown",
                options=[
                    {"label": "Gantt Chart with Slippage", "value": "slippage"},
                    {"label": "Updated Gantt Chart", "value": "updated"},
                    {"label": "Baseline Gantt Chart", "value": "baseline"},
                ],
                value="slippage",
            ),
        ],
        width=6,
        align="center",
        class_name="column-element dash-dropdown",
    )

    right_config_column = dbc.Col(
        children=[
            dcc.Checklist(
                id="interruptions-checklist",
                options=[
                    {
                        "label": "Include Interruptions",
                        "value": "include_interruptions",
                    },
                ],
                value=["include_interruptions", "include_milestones"],
            ),
            dcc.Checklist(
                id="milestones-checklist",
                options=[
                    {"label": "Include Milestones", "value": "include_milestones"},
                ],
                value=["include_milestones"],
            ),
        ],
        width=6,
        align="center",
        class_name="column-element dash-checklist",
    )

    top_row = dbc.Row(
        children=[
            left_config_column,
            right_config_column,
        ],
        class_name="row-element ",
        style={"width": "100%"},
    )

    bottom_row = dbc.Row(
        children=[dcc.Graph(id="gantt-chart")], class_name="row-element"
    )

    app.layout = html.Div(children=[top_row, bottom_row])

    @app.callback(
        Output("gantt-chart", "figure"),
        Input("chart-dropdown", "value"),
        Input("interruptions-checklist", "value"),
        Input("milestones-checklist", "value"),
    )
    def update_chart(selected_chart, interruptions_checklist, milestones_checklist):
        include_interruptions = "include_interruptions" in interruptions_checklist
        include_milestones = "include_milestones" in milestones_checklist

        if selected_chart == "slippage":
            fig = gantt_chart.create_gantt_chart_with_slippage(
                include_interruptions, include_milestones
            )
        elif selected_chart == "updated":
            fig = gantt_chart.create_updated_gantt_chart(
                include_interruptions, include_milestones
            )
        elif selected_chart == "baseline":
            fig = gantt_chart.create_baseline_gantt_chart(
                include_interruptions, include_milestones
            )
        else:
            fig = {}

        return fig

    return app
