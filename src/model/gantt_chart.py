"""
// File: gantt_chart.py
Create a Gantt chart with overlay of current tasks. It uses the initial tasks, updated tasks, interuptions and milestones data to create the chart.
"""
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from src.utils.data_loading import load_data, modify_df_from_interuptions

class GanttChart():
    """
    Class to create a Gantt chart with overlay of current tasks. It uses the initial tasks, updated tasks, interuptions and milestones data to create the chart.

    Parameters:
    None

    Returns:
    None
    """
    def __init__(self):
        self.df_initial = load_data("data/initial_tasks.json")
        self.df_updated = load_data("data/updated_tasks.json")
        self.df_interuptions = load_data("data/interuptions.json")
        self.df_milestones = load_data("data/milestones.json")
        self.df_initial = modify_df_from_interuptions(self.df_initial, self.df_interuptions)
        self.df_current = modify_df_from_interuptions(self.df_updated, self.df_interuptions)
        self.df_milestones = modify_df_from_interuptions(self.df_milestones, self.df_interuptions)
        print(self.df_current.head())
        print(self.df_interuptions.head())
        print(self.df_initial.head())


    def create_gantt_chart_with_slippage(self):
        """
        Create a Gantt chart with overlay of current tasks

        Parameters:
        df_initial: pd.DataFrame
        df_current: pd.DataFrame

        Returns:
        gantt_chart: plotly.graph_objs._figure.Figure
        """

        # Create the initial Gantt chart
        fig = px.timeline(
            self.df_initial,
            x_start="Begin",
            x_end="End",
            y="Task",
            color="Task Group",
            labels={"Task": "Task Name", "Task Group": "Task Group"},
        )

        # Add the current tasks as separate traces with the same legend name
        for _, row in self.df_current.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[row['Begin'], row['End']],
                    y=[row['Task'], row['Task']],
                    mode='lines',
                    line=dict(color='rgba(255, 0, 0, 0.5)', width=10),
                    name='Updated Task',
                    showlegend=_ == 0  # Only show legend for the first task
                )
            )

        # Add the milestones as a single trace
        fig.add_trace(
            go.Scatter(
                x=self.df_milestones['Begin'],
                y=self.df_milestones['Task'],
                mode='markers',
                marker=dict(color='rgba(0, 0, 0, 1)', size=10),
                name='Milestone'
            )
        )

        # Add the interuptions as separate traces with different legend names
        for _, row in self.df_interuptions.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[row['Begin'], row['End']],
                    y=[row['Task'], row['Task']],
                    mode='lines',
                    line=dict(color='rgba(0, 0, 255, 0.5)', width=10),
                    name=row['Task']
                )
            )


        # Add a vertical line for today's date
        today_date = datetime.now().strftime('%Y-%m-%d')
        fig.add_shape(
            dict(
                type="line",
                x0=today_date,
                y0=0,
                x1=today_date,
                y1=1,
                xref="x",
                yref="paper",
                line=dict(color="RoyalBlue", width=2, dash="dot"),
            )
        )


        # Update layout for better readability
        fig.update_layout(
            title="Gantt Chart with Initial and Current Tasks",
            xaxis_title="Time",
            yaxis_title="Task",
            showlegend=True,
        )

        return fig

    def create_current_gantt_chart(self):
        """
        Create a Gantt chart with overlay of current tasks

        Parameters:
        df_current: pd.DataFrame

        Returns:
        gantt_chart: plotly.graph_objs._figure.Figure
        """

        # Create the initial Gantt chart
        fig = px.timeline(
            self.df_current,
            x_start="Begin",
            x_end="End",
            y="Task",
            color="Task Group",
            labels={"Task": "Task Name", "Task Group": "Task Group"},
        )

        # Add the milestones as a single trace
        fig.add_trace(
            go.Scatter(
                x=self.df_milestones['Begin'],
                y=self.df_milestones['Task'],
                mode='markers',
                marker=dict(color='rgba(0, 0, 0, 1)', size=10),
                name='Milestone'
            )
        )

        # Add the interuptions as separate traces with different legend names
        for _, row in self.df_interuptions.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[row['Begin'], row['End']],
                    y=[row['Task'], row['Task']],
                    mode='lines',
                    line=dict(color='rgba(0, 0, 255, 0.5)', width=10),
                    name=row['Task']
                )
            )

        # Add a vertical line for today's date
        today_date = datetime.now().strftime('%Y-%m-%d')
        fig.add_shape(
            dict(
                type="line",
                x0=today_date,
                y0=0,
                x1=today_date,
                y1=1,
                xref="x",
                yref="paper",
                line=dict(color="RoyalBlue", width=2, dash="dot"),
            )
        )

        # Update layout for better readability
        fig.update_layout(
            title="Gantt Chart with Current Tasks",
            xaxis_title="Time",
            yaxis_title="Task",
            showlegend=True,
        )

        return fig