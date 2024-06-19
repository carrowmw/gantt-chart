"""
// File: gantt_chart.py
Create a Gantt chart. It uses the initial tasks, updated tasks, interuptions and milestones data to create the chart.
"""

from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from src.utils.data_loading import load_data, modify_df_from_interuptions


class GanttChart:
    """
    Class to create a Gantt chart with overlay of project progress. It uses the initial tasks, updated tasks, interruptions and milestones data to create the chart.

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

    def _create_base_gantt_chart(
        self,
        df,
        include_updates=True,
        include_milestones=True,
        include_interruptions=True,
    ):
        """
        Private method to create the base Gantt chart.

        Parameters:
        df: pd.DataFrame
        include_milestones: bool
        include_interruptions: bool

        Returns:
        fig: plotly.graph_objs._figure.Figure
        """
        # Create the initial Gantt chart
        fig = px.timeline(
            df,
            x_start="Begin",
            x_end="End",
            y="Task",
            color="Task Group",
            labels={"Task": "Task Name", "Task Group": "Task Group"},
        )

        if include_updates:
            # Add the updated tasks as separate traces with the same legend name
            for idx, row in self.df_updated.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=[row["Begin"], row["End"]],
                        y=[row["Task"], row["Task"]],
                        mode="lines",
                        line=dict(color="rgba(255, 0, 0, 0.5)", width=5),
                        name="Updatee Task",
                        showlegend=idx == 0,  # Only show legend for the first task
                    )
                )

        if include_interruptions:
            # Add the interruptions as separate traces with the same legend name
            for idx, row in self.df_interuptions.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=[row["Begin"], row["End"]],
                        y=[row["Task"], row["Task"]],
                        mode="lines",
                        line=dict(color="rgba(0, 0, 0, 0.5)", width=5),
                        name="Interruption",
                        showlegend=idx == 0,  # Only show legend for the first task
                    )
                )

        # Add the milestones as a single trace if included
        if include_milestones:
            fig.add_trace(
                go.Scatter(
                    x=self.df_milestones["Begin"],
                    y=self.df_milestones["Task"],
                    mode="markers",
                    marker=dict(color="rgba(0, 0, 0, 1)", size=10),
                    name="Milestone",
                )
            )

        # Add a vertical line for today's date
        today_date = datetime.now().strftime("%Y-%m-%d")
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

        # Add range slider
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))

        # Calculate the height dynamically based on the number of tasks
        num_tasks = len(df["Task"].unique())
        task_height = 50  # Height per task in pixels
        fig_height = num_tasks * task_height

        # Update the layout to set the height
        fig.update_layout(height=fig_height)

        return fig

    def create_baseline_gantt_chart(
        self, include_interruptions=False, include_milestones=True
    ):
        """
        Create a Gantt chart with overlay of initial tasks and optionally include interruptions.

        Parameters:
        include_interruptions: bool

        Returns:
        gantt_chart: plotly.graph_objs._figure.Figure
        """
        df = self.df_initial.copy()
        if include_interruptions:
            df = modify_df_from_interuptions(df, self.df_interuptions)
        return self._create_base_gantt_chart(
            df,
            include_updates=False,
            include_milestones=include_milestones,
            include_interruptions=include_interruptions,
        )

    def create_gantt_chart_with_slippage(
        self, include_interruptions=False, include_milestones=True
    ):
        """
        Create a Gantt chart with overlay of project progress tasks and optionally include interruptions.

        Parameters:
        include_interruptions: bool

        Returns:
        gantt_chart: plotly.graph_objs._figure.Figure
        """
        df = self.df_initial.copy()
        if include_interruptions:
            df = modify_df_from_interuptions(df, self.df_interuptions)
        return self._create_base_gantt_chart(
            df,
            include_updates=True,
            include_milestones=include_milestones,
            include_interruptions=include_interruptions,
        )

    def create_updated_gantt_chart(
        self, include_interruptions=False, include_milestones=True
    ):
        """
        Create a Gantt chart with overlay of updated tasks and optionally include interruptions.

        Parameters:
        include_interruptions: bool

        Returns:
        gantt_chart: plotly.graph_objs._figure.Figure
        """
        df = self.df_updated.copy()
        if include_interruptions:
            df = modify_df_from_interuptions(df, self.df_interuptions)
        return self._create_base_gantt_chart(
            df,
            include_updates=False,
            include_milestones=include_milestones,
            include_interruptions=include_interruptions,
        )
