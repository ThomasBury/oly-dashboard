import marimo

__generated_with = "0.13.11-dev14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Brussels Weightlifting School
    ## Competion Dashboard
    """
    )
    return


@app.cell
def _():
    import pandas as pd
    data = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTy21622d_G-6bZw8-ugzG9RMbLvy_0h_eyhcVtcOYLcssPygig8pPnwAimXVcvntOD8X_JdCOWdd2/pub?output=csv"
    )
    members = data["member"].unique().tolist()
    return (data, members, pd,)

# @app.cell
# def _(mo):
#     csv_file = mo.ui.file(
#         filetypes=[".csv"], kind="button", label="Upload Local CSV File"
#     )

#     # Display the file uploader in the Marimo notebook
#     csv_file
#     return (csv_file,)

# @app.cell
# def _(csv_file):
#     import io
#     import pandas as pd

#     # Function to load the uploaded file into a Pandas DataFrame
#     def load_csv_to_dataframe(file_data):
#         """Load an uploaded CSV file into a Pandas DataFrame.

#         Parameters
#         ----------
#         file_data : marimo.ui.FileUIElement
#             The file UI element from Marimo, containing the uploaded CSV data.
#             It's expected that `file_data.value[0].contents` yields the
#             byte string of the CSV content.

#         Returns
#         -------
#         pd.DataFrame
#             A Pandas DataFrame created from the content of the uploaded CSV file.
#         """
#         content_bytes = file_data.value[0].contents
#         content_string = io.StringIO(content_bytes.decode("utf-8"))
#         df = pd.read_csv(content_string)
#         return df
#     data = load_csv_to_dataframe(csv_file)
#     members = data["member"].unique().tolist()
#     return (data, members, pd,)


@app.cell
def _(mo, members):
    member = mo.ui.dropdown(
        options=members, label="Identify yourself", searchable=True
    )
    mo.vstack([
        mo.md("**Hey, you! What's your name?** 👋"),
        member
    ])
    return (member,)
    
    
@app.cell
def _(mo, pd, data, member):
    member_name = member.value

    def get_member_data(data, member):
        member_data = data[data["member"] == member].copy()
        member_data["date"] = pd.to_datetime(member_data["date"]).dt.date
        member_data = member_data.sort_values(by="date")
        member_data = member_data.reset_index(drop=True)
        member_data = member_data.drop(columns=["member"])
        member_data = member_data.melt(
            id_vars=[col for col in member_data.columns if col not in ["snatch", "clean_and_jerk", "total"]],
            value_vars=["snatch", "clean_and_jerk", "total"],
            var_name="lift_name",
            value_name="weight_kg"
        )
        member_data["weight_kg"] = member_data["weight_kg"].astype(float).fillna(0)
        member_data["sinclair_points"] = round(member_data["weight_kg"] * member_data["sinclair_coef_2021"])
        member_data = member_data.sort_values(by=["date", "sinclair_points"]).reset_index(drop=True)
        return member_data

    member_data_df = get_member_data(data, member_name)

    mo.vstack([
        mo.md(f"Welcome, **{member_name}**!"),
        member_data_df  # This will display the DataFrame as a table
    ])
    return (member_data_df, member_name, pd)

@app.cell
def _(member_data_df, pd):
    def add_snatch_cj_spread_pct(df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values(by="date")
        if "spread_pct" in df.columns:
            df = df.drop(columns=["spread_pct"])
        pivot_df = df.pivot_table(index="date", columns="lift_name", values="weight_kg")
        interpolated_df = pivot_df.interpolate(method="linear")
        interpolated_df["spread_pct"] = round(
            (
                (interpolated_df["clean_and_jerk"] - interpolated_df["snatch"])
                / interpolated_df["snatch"]
            )
            * 100
        )
        merged_df = pd.merge(
            df, interpolated_df["spread_pct"].reset_index(), on="date", how="left"
        )
        return merged_df
    def add_cumulative_personal_best(df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values(by=["lift_name", "date"])
        def calculate_pb(series):
            return series.cummax()
        df["personal_best_kg"] = df.groupby("lift_name")["weight_kg"].transform(
            calculate_pb
        )
        return df
    def add_lift_bodyweight_ratio(df: pd.DataFrame) -> pd.DataFrame:
        df["lift_bodyweight_ratio"] = round(100 * df["weight_kg"] / df["bodyweight_kg"])
        return df
    member_data_df["date"] = pd.to_datetime(member_data_df["date"]).dt.date
    data_df = add_snatch_cj_spread_pct(member_data_df)
    data_df = add_cumulative_personal_best(data_df)
    data_df = add_lift_bodyweight_ratio(data_df)
    data_df = data_df.reset_index(drop=True)
    if "Unnamed: 0" in data_df.columns:
        data_df = data_df.drop(columns=["Unnamed: 0"])
        
        
    
    return data_df, pd


@app.cell
def _(pd):
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    pio.renderers.default = "iframe"

    def create_temporal_weight_chart(df: pd.DataFrame) -> go.Figure:
        """Create two line charts: one for snatch & clean_and_jerk, one for total."""
        import plotly.express as px
        import plotly.graph_objects as go
        # Chart 1: snatch and clean_and_jerk
        lifts_df = df[df["lift_name"].isin(["snatch", "clean_and_jerk"])]
        fig_lifts = px.line(
            lifts_df,
            x="date",
            y="weight_kg",
            text="weight_kg",
            color="lift_name",
            title="Weight Lifted Over Time (Snatch & Clean and Jerk)",
            labels={"weight_kg": "Weight (kg)", "lift_name": "Lift"},
            markers=True,
            template="plotly_white",
        )
        fig_lifts.update_traces(textposition="top center", textfont_size=14)
        # Add personal best stepwise dashed lines for each lift
        if not lifts_df.empty and 'lift_name' in lifts_df.columns and 'personal_best_kg' in lifts_df.columns:
            for lift_name in lifts_df["lift_name"].unique():
                lift_color = None
                # Find the color for this lift from the traces
                for trace in fig_lifts.data:
                    if trace.name == lift_name:
                        lift_color = trace.line.color
                        break
                lift_pb_df = lifts_df[lifts_df["lift_name"] == lift_name].sort_values(by="date")
                if not lift_pb_df.empty:
                    fig_lifts.add_trace(go.Scatter(
                        x=lift_pb_df["date"],
                        y=lift_pb_df["personal_best_kg"],
                        mode='lines',
                        line=dict(color=lift_color, dash='dash', shape='hv', width=1.25),
                        name=f'{lift_name} PB',
                        legendgroup=lift_name,
                        showlegend=True
                    ))
        # Chart 2: total
        total_df = df[df["lift_name"] == "total"]
        fig_total = px.line(
            total_df,
            x="date",
            y="weight_kg",
            text="weight_kg",
            title="Total Weight Lifted Over Time",
            labels={"weight_kg": "Total (kg)"},
            markers=True,
            template="plotly_white",
        )
        fig_total.update_traces(textposition="top center", textfont_size=14)
        # Add personal best stepwise dashed line for total
        if not total_df.empty and 'personal_best_kg' in total_df.columns:
            fig_total.add_trace(go.Scatter(
                x=total_df["date"],
                y=total_df["personal_best_kg"],
                mode='lines',
                line=dict(color='black', dash='dash', shape='hv', width=1.25),
                name='Total PB',
                legendgroup='total',
                showlegend=True
            ))
        return fig_lifts, fig_total

    def create_temporal_sinclair_chart(df: pd.DataFrame) -> go.Figure:
        """Create a line chart of Sinclair points over time.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data to plot. Expected columns are
            'date', 'sinclair_points', and 'lift_name'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing Sinclair points over time,
            colored by lift name.
        """
        import plotly.express as px
        import plotly.graph_objects as go
        # Only use total
        total_df = df[df["lift_name"] == "total"].sort_values(by="date")
        fig = px.line(
            total_df,
            x="date",
            y="sinclair_points",
            text="sinclair_points",
            title="Sinclair Points Over Time (Total)",
            labels={"sinclair_points": "Sinclair Points"},
            markers=True,
            template="plotly_white",
        )
        fig.update_traces(textposition="top center", textfont_size=14)
        # Add stepwise dashed line for Sinclair PB (rolling max)
        if not total_df.empty:
            sinclair_pb = total_df["sinclair_points"].cummax()
            fig.add_trace(go.Scatter(
                x=total_df["date"],
                y=sinclair_pb,
                mode='lines',
                line=dict(color='black', dash='dash', shape='hv', width=1.25),
                name='Sinclair PB',
                legendgroup='sinclair',
                showlegend=True
            ))
        return fig

    def create_snatch_cj_spread_chart(df: pd.DataFrame) -> go.Figure:
        """Create a line chart of clean_and_jerk vs. snatch spread over time.

        The spread is shown as a percentage of snatch weight.
        This chart filters for 'clean_and_jerk' lift names as 'spread_pct'
        is primarily associated with it.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data. Expected columns: 'date', 'lift_name', 'spread_pct'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing the C&J - snatch spread percentage.
        """
        spread_df = df[df["lift_name"] == "clean_and_jerk"].dropna(subset=["spread_pct"])
        return px.line(
            spread_df,
            x="date",
            y="spread_pct",
            title="Clean & Jerk - Snatch Spread (% of snatch) Over Time",
            labels={"spread_pct": "Spread (% of snatch)"},
            markers=True,
            template="plotly_white",
        )

    def create_lift_bodyweight_ratio_chart(df: pd.DataFrame) -> go.Figure:
        """Create a line chart of lift to bodyweight ratio over time.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data. Expected columns: 'date',
            'lift_bodyweight_ratio', 'lift_name'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing the lift/bodyweight ratio, colored by lift name.
        """
        return px.line(
            df,
            x="date",
            y="lift_bodyweight_ratio",
            color="lift_name",
            title="Lift / Bodyweight Ratio Over Time",
            labels={
                "lift_bodyweight_ratio": "Ratio (Lift / Bodyweight)",
                "lift_name": "Lift",
            },
            markers=True,
            template="plotly_white",
        )

    def create_bodyweight_chart(df: pd.DataFrame) -> go.Figure:
        """Create a line chart of bodyweight over time.

        Duplicate bodyweight entries for the same date are removed before plotting.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data. Expected columns: 'date', 'bodyweight_kg'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing bodyweight over time.
        """
        dum = df.copy()
        dum = dum[["date", "bodyweight_kg"]].drop_duplicates().sort_values(by="date")
        return px.line(
            dum,
            x="date",
            y="bodyweight_kg",
            title="Bodyweight Over Time",
            markers=True,
            template="plotly_white",
        )

    return (
        create_bodyweight_chart,
        create_lift_bodyweight_ratio_chart,
        create_snatch_cj_spread_chart,
        create_temporal_sinclair_chart,
        create_temporal_weight_chart,
    )

@app.cell
def _(mo,
    create_bodyweight_chart,
    create_lift_bodyweight_ratio_chart,
    create_snatch_cj_spread_chart,
    create_temporal_sinclair_chart,
    create_temporal_weight_chart,
    data_df
):
    # Unpack the two charts from create_temporal_weight_chart
    fig_lifts, fig_total = create_temporal_weight_chart(data_df)
    chart_map = {
        "Temporal Evolution (Bodyweight)": create_bodyweight_chart(data_df),
        "Temporal Evolution (Lift kg: Snatch & C&J)": fig_lifts,
        "Temporal Evolution (Lift kg: Total)": fig_total,
        "Temporal Evolution (Sinclair)": create_temporal_sinclair_chart(data_df),
        "C&J - snatch Spread": create_snatch_cj_spread_chart(data_df),
        "Lift / Bodyweight Ratio": create_lift_bodyweight_ratio_chart(data_df),
    }
    mo.vstack([
        mo.md("## All charts below"),
        # *[mo.md(f"### {title}") for title in chart_map.keys()],
        *[chart for chart in chart_map.values()]
    ])
    return

if __name__ == "__main__":
    app.run()
