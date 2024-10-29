"""
// File: gantt_chart.py
Create a Gantt chart. It uses the initial tasks, updated tasks, interuptions and milestones data to create the chart.
"""

from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils.data_loading import load_data, modify_df_from_interuptions


class GanttChart:
    def __init__(self):
        self.df_initial = load_data("data/initial_tasks.json").iloc[::-1]
        self.df_updated = load_data("data/updated_tasks.json").iloc[::-1]
        self.df_interuptions = load_data("data/interuptions.json").iloc[::-1]
        self.df_milestones = load_data("data/milestones.json").iloc[::-1]

    def _create_base_gantt_chart(
        self,
        df,
        include_updates=True,
        include_milestones=True,
        include_interruptions=True,
    ):
        fig = px.timeline(
            df,
            x_start="Begin",
            x_end="End",
            y="Task",
            color="Task Group",
            labels={"Task": "Task Name", "Task Group": "Task Group"},
        )

        if include_updates:
            df_updated = self.df_updated.copy()
            if include_interruptions:
                df_updated = modify_df_from_interuptions(
                    df_updated, self.df_interuptions
                )
            for idx, row in df_updated.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=[row["Begin"], row["End"]],
                        y=[row["Task"], row["Task"]],
                        mode="lines",
                        line=dict(color="rgba(255, 0, 0, 0.5)", width=5),
                        name="Updated Tasks",
                        showlegend=idx == 0,
                    )
                )

        if include_interruptions:
            for idx, row in self.df_interuptions.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=[row["Begin"], row["End"]],
                        y=[row["Task"], row["Task"]],
                        mode="lines",
                        line=dict(color="rgba(0, 0, 0, 0.5)", width=5),
                        name="Interruption",
                        showlegend=idx == 0,
                    )
                )

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

        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))

        if include_updates:
            tasks = df["Task"]._append(self.df_updated["Task"])
            num_tasks = len(tasks.unique())
        else:
            num_tasks = len(df["Task"].unique())
        if include_interruptions:
            num_tasks += len(self.df_interuptions["Task"].unique())
        if include_milestones:
            num_tasks += len(self.df_milestones["Task"].unique())
        task_height = 30
        fig_height = num_tasks * task_height

        fig.update_layout(height=fig_height)

        return fig

    def create_baseline_gantt_chart(
        self, include_interruptions=True, include_milestones=True
    ):
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
        self, include_interruptions=True, include_milestones=True
    ):
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
        self, include_interruptions=True, include_milestones=True
    ):
        df = self.df_updated.copy()
        if include_interruptions:
            df = modify_df_from_interuptions(df, self.df_interuptions)
        return self._create_base_gantt_chart(
            df,
            include_updates=False,
            include_milestones=include_milestones,
            include_interruptions=include_interruptions,
        )
