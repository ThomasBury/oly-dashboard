import marimo

__generated_with = "0.13.11-dev14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    # Set logo path and size (adjust as needed)
    logo_path = "bws_log_tr_bkg.png"  # Ensure this file is in the same directory or adjust the path
    logo_width = "120px"  # Change this value to customize logo size

    header = mo.md(
        f"""
        <div style="
            text-align: center;
            padding: 2em 1em 1em 1em;
            margin-bottom: 2em;
        ">
            <img src='{logo_path}' alt="BWS Logo" style="
                width: {logo_width};
                max-width: 30vw;
                height: auto;
                display: block;
                margin: 0 auto 1em auto;
            "/>
            <p style="
                font-size: 3em;
                font-weight: 800;
                color: #fa7d00;
                margin-bottom: 0.2em;
                letter-spacing: -0.02em;
            ">
                Brussels Weightlifting School
            </p>
            <p style="
                font-size: 1.6em;
                font-weight: 500;
                color: #7f8c8d;
                letter-spacing: 0.01em;
            ">
                Competition Dashboard
            </p>
        </div>
        """
    )
    header
    return



@app.cell
def _(mo):
    import pandas as pd
    # from pyodide.http import open_url  # Only available in Pyodide environments
    from io import StringIO
    
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTy21622d_G-6bZw8-ugzG9RMbLvy_0h_eyhcVtcOYLcssPygig8pPnwAimXVcvntOD8X_JdCOWdd2/pub?output=csv"
    try:
        # For WASM (Marimo export, in browser)
        from pyodide.http import open_url

        csv_text = open_url(url).read()
        data = pd.read_csv(StringIO(csv_text))
    except ImportError:
        # For local Python execution (Jupyter, VSCode, etc.)
        data = pd.read_csv(url, parse_dates=["date"])
    
    members = data["member"].unique().tolist()
    return (data, members, pd,)


@app.cell
def _(mo, members):
    # 1. Create the mo.ui.dropdown object FIRST
    member_selector = mo.ui.dropdown(
        options=members,
        label="",       # No label—cleaner look
        searchable=True,
        value="Anna" if "Anna" in members else members[0],  # Default to the first member
    )
    
    # 2. Then, apply the styling to a *displayable variable*
    #    This is what you'll put into your mo.md or other display functions
    styled_member_dropdown = member_selector.style({
        "border": "1px solid #9D00FF",
        "border-radius": "5px",
        "padding": "0.5em 1em",
        "font-size": "1em",
        "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.05)",
        "color": "#333",
        "background-color": "#ffffff",
        "transition": "all 0.2s ease-in-out",
    })

    
    user_message = mo.md(
        """
        ### Select a Member:

        """
    )

    # Create a styled container using custom HTML + CSS
    banner = mo.md(
        """
        <div style="
            background: #fcfcfd;
            border-left: 4px solid #9D00FF;
            border-radius: 0.8rem;
            padding: 1.2rem 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 12px rgba(157, 0, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <span style="
                font-size: 1.3rem;
                font-weight: 700;
                background: linear-gradient(90deg, #9D00FF, #7D5FFF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">👤 Hey, you! What's your name? 👋 </span>
            <span style="color: #555; font-size: 1rem;">
                Choose your name from the list below to get started.
            </span>
        </div>
        """
    )

    # Stack the banner and dropdown neatly
    mo.vstack([banner, user_message, styled_member_dropdown])

    return (member_selector,)


@app.cell
def _(mo, pd, data, member_selector):
    import numpy as np
    member_name = member_selector.value

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
        member_data["weight_kg"] = member_data["weight_kg"].replace(0, np.nan)
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
    # Custom color palette: blue, yellow, black
    club_colors = ["#9D00FF", "#fa7d00", "#222222"]
    pio.templates["bws"] = go.layout.Template(
        layout=go.Layout(
            font=dict(family="Arial", size=16, color="#222"),
            plot_bgcolor="#f5f7fa",
            paper_bgcolor="#f5f7fa",
            title=dict(font=dict(color="#9D00FF")),
            legend=dict(bgcolor="#fff", bordercolor="#9D00FF", borderwidth=1),
        )
    )
    pio.renderers.default = "iframe"

    def create_temporal_weight_chart(df: pd.DataFrame) -> go.Figure:
        import plotly.express as px
        import plotly.graph_objects as go
        lifts_df = df[df["lift_name"].isin(["snatch", "clean_and_jerk"])]
        fig_lifts = px.line(
            lifts_df,
            x="date",
            y="weight_kg",
            #text="weight_kg",
            color="lift_name",
            title="Weight Lifted Over Time (Snatch & Clean and Jerk)",
            labels={"weight_kg": "Weight (kg)", "lift_name": "Lift"},
            markers=True,
            template="bws",
            color_discrete_sequence=club_colors,
        )
        fig_lifts.update_traces(textposition="top center", textfont_size=14)
        if not lifts_df.empty and 'lift_name' in lifts_df.columns and 'personal_best_kg' in lifts_df.columns:
            for lift_name in lifts_df["lift_name"].unique():
                lift_color = None
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
        total_df = df[df["lift_name"] == "total"]
        fig_total = px.line(
            total_df,
            x="date",
            y="weight_kg",
            # text="weight_kg",
            title="Total Weight Lifted Over Time",
            labels={"weight_kg": "Total (kg)"},
            markers=True,
            template="bws",
            color_discrete_sequence=["#9D00FF"],
        )
        fig_total.update_traces(textposition="top center", textfont_size=14)
        if not total_df.empty and 'personal_best_kg' in total_df.columns:
            fig_total.add_trace(go.Scatter(
                x=total_df["date"],
                y=total_df["personal_best_kg"],
                mode='lines',
                line=dict(color="#9D00FF", dash='dash', shape='hv', width=1.25),
                name='Total PB',
                legendgroup='total',
                showlegend=True
            ))
        return fig_lifts, fig_total

    def create_temporal_sinclair_chart(df: pd.DataFrame) -> go.Figure:
        import plotly.express as px
        import plotly.graph_objects as go
        total_df = df[df["lift_name"] == "total"].sort_values(by="date")
        fig = px.line(
            total_df,
            x="date",
            y="sinclair_points",
            # text="sinclair_points",
            title="Sinclair Points Over Time (Total)",
            labels={"sinclair_points": "Sinclair Points"},
            markers=True,
            template="bws",
            color_discrete_sequence=["#9D00FF"],
        )
        fig.update_traces(textposition="top center", textfont_size=14)
        if not total_df.empty:
            sinclair_pb = total_df["sinclair_points"].cummax()
            fig.add_trace(go.Scatter(
                x=total_df["date"],
                y=sinclair_pb,
                mode='lines',
                line=dict(color='#9D00FF', dash='dash', shape='hv', width=1.25),
                name='Sinclair PB',
                legendgroup='sinclair',
                showlegend=True
            ))
        return fig

    def create_snatch_cj_spread_chart(df: pd.DataFrame) -> go.Figure:
        spread_df = df[df["lift_name"] == "clean_and_jerk"].dropna(subset=["spread_pct"])
        return px.line(
            spread_df,
            x="date",
            y="spread_pct",
            title="Clean & Jerk - Snatch Spread (% of snatch) Over Time",
            labels={"spread_pct": "Spread (% of snatch)"},
            markers=True,
            template="bws",
            color_discrete_sequence=["#fa7d00"],
        )

    def create_lift_bodyweight_ratio_chart(df: pd.DataFrame) -> go.Figure:
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
            template="bws",
            color_discrete_sequence=club_colors,
        )

    def create_bodyweight_chart(df: pd.DataFrame) -> go.Figure:
        dum = df.copy()
        dum = dum[["date", "bodyweight_kg"]].drop_duplicates().sort_values(by="date")
        return px.line(
            dum,
            x="date",
            y="bodyweight_kg",
            title="Bodyweight Over Time",
            markers=True,
            template="bws",
            color_discrete_sequence=club_colors,
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
