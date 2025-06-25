import marimo

__generated_with = "0.13.11-dev14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    header = mo.md(
        """
        <div style="
            text-align: center;
            padding: 2em 1em;
            margin-bottom: 2em;
        ">
            <p style="
                font-size: 3em; /* Larger, impactful main title */
                font-weight: 800; /* Strong but not extreme */
                color: #9D00FF; /* Primary color */
                margin-bottom: 0.2em;
                letter-spacing: -0.02em; /* Slightly tighter for modern feel */
            ">
                Olympic Weightlifting Dashboard
            </p>
            <p style="
                font-size: 1.6em; /* Clear, readable subtitle */
                font-weight: 500;
                color: #7f8c8d; /* Muted secondary color */
                letter-spacing: 0.01em;
            ">
                Training Dashboard
            </p>
        </div>
        """
    )
    header
    return






@app.cell
def _(mo):
    
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
            ">👤 Welcome to the Olympic Weightlifting Dashboard! 👋 </span>

        </div>
        """
    )
    
    google_sheet_help = mo.md(
        """
        <div style="
            background: #fcfcfd;
            border-left: 4px solid #ffc803;
            border-radius: 0.8rem;
            padding: 1.2rem 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 12px rgba(157, 0, 255, 0.08);
            font-size: 1.08em;
        ">
            <span style="font-size: 1.25em; font-weight: 700; color:#ffc803;">
                📋 How to Start Tracking Your Lifts
            </span>
            <ol style="margin-top: 1em; color: #333;">
                <li>
                    <b>Copy the Template:</b>
                    <br>
                    <a href="https://docs.google.com/spreadsheets/d/1sOvuFj0_LtxaDD6gCrLZJSfJ0HYku9xLoonkTIPCFIc/edit?gid=1543506157#gid=1543506157" target="_blank" style="color: #9D00FF; text-decoration: underline;">
                        Open this Google Sheets template
                    </a> and go to <b>File → Make a copy</b> to save it to your own Google Drive.
                </li>
                <li>
                    <b>Enter Your Data:</b>
                    <br>
                    Fill in your training data (date, lift_name, weight_kg, bodyweight_kg, reps, etc.).
                </li>
                <li>
                    <b>Publish as CSV:</b>
                    <br>
                    In your copy, go to <b>File → Share → Publish to web</b>.<br>
                    Choose the sheet, select <b>Comma-separated values (.csv)</b>, click <b>Publish</b>, and copy the generated link.
                </li>
                <li>
                    <b>Paste the URL:</b>
                    <br>
                    Paste your published CSV URL below. The dashboard will load and visualize your data automatically!
                </li>
            </ol>
            <span style="color: #7f8c8d; font-size: 0.98em;">
                <b>Tip:</b> Update your sheet anytime—just refresh the dashboard to see your latest results.
            </span>
        </div>
        """
    )
    
    
    sample_data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSzIvdyxe1N-FPcuOryGoWTHUSaxBUqn9iGW2M4Q5gxPdNaGpSvfWUcR_E5ZBftdUyQh3kqFR4VifL1/pub?output=csv"
    user_url =mo.ui.text(
        value = sample_data_url,
        full_width=True,
    )

    # 2. Then, apply the styling to a *displayable variable*
    #    This is what you'll put into your mo.md or other display functions
    styled_user_url = user_url.style({
        "border": "1px solid #9D00FF",
        "border-radius": "5px",
        "padding": "0.5em 1em",
        "font-size": "1em",
        "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.05)",
        "color": "#333",
        "background-color": "#ffffff",
        "transition": "all 0.2s ease-in-out",
    })

    url_message = mo.md(
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
            ">🌐 Paste your own URL: </span>

        </div>
        """
    )
    
    # Stack the banner and dropdown neatly
    mo.vstack([banner, google_sheet_help, url_message, styled_user_url])
    return user_url

@app.cell
def _(mo):
    sinclair_gender = mo.ui.dropdown(
        options=["Female", "Male"], label="Sinclair Gender"
    )
    return (sinclair_gender,)


@app.cell
def _(mo, sinclair_gender):
    
    sinclair_message = mo.md(
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
            ">Choose Your Sinclair Coefficients: </span>

        </div>
        """
    )
    
    sinclair_info = mo.md(
        """
        <div style="
            background: #fcfcfd;
            border-left: 4px solid #ffc803;
            border-radius: 0.8rem;
            padding: 1.2rem 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 12px rgba(157, 0, 255, 0.08);
            font-size: 1.08em;
            color: #222;
        ">
            <span style="font-size: 1.18em; font-weight: 700; color: #ffc803;">
                🏅 What are Sinclair Points?
            </span>
            <br>
            Sinclair Points are a way to compare Olympic weightlifting performances across different bodyweights. 
            They use a mathematical formula to "normalize" your total, so lifters of different sizes can be compared fairly.
            <br><br>
            <b>Where can I find the official Sinclair coefficients?</b><br>
            You can find the latest official Sinclair coefficients on the 
            <a href="https://iwf.sport/weightlifting_/sinclair-coefficient/" target="_blank" style="color:#9D00FF; text-decoration: underline;">
                IWF Sinclair Coefficient page
            </a>
            under the "Documents" section.
            Use these values for the most accurate calculations.
        </div>
        """
    )
    
    if sinclair_gender.value == "Male":
        a_coeff = mo.ui.number(0.722762521, label="Male 'A':", step=1e-9)
        b_coeff = mo.ui.number(193.609, label="Male 'B':", step=1e-3)
        sinclair_coeff = mo.vstack([sinclair_message, sinclair_info, mo.hstack([sinclair_gender, a_coeff, b_coeff])])
    else:
        a_coeff = mo.ui.number(0.787004341, label="Female 'A':", step=1e-9)
        b_coeff = mo.ui.number(153.757, label="Female 'B':", step=1e-3)
        sinclair_coeff =  mo.vstack([sinclair_message, sinclair_info, mo.hstack([sinclair_gender, a_coeff, b_coeff])])

    sinclair_coeff
    return a_coeff, b_coeff


@app.cell
def __(mo, user_url, a_coeff, b_coeff):
    """
    This cell loads weightlifting data from a URL, cleans it, calculates
    various performance metrics, and displays the results.
    """
    # 1. IMPORTS & SETUP
    import pandas as pd
    import numpy as np
    from io import StringIO
    import warnings
    import logging

    logging.basicConfig(level=logging.INFO)
    
    # Define a variable to hold the final output
    final_output = None

    # 2. DATA LOADING
    def load_data(url: str) -> tuple[pd.DataFrame | None, str | None]:
        """
        Loads data from a URL, handling both standard and Pyodide environments.
        Returns a tuple of (DataFrame, error_message).
        """
        if not url:
            return None, "Please provide a data URL."
        try:
            from pyodide.http import open_url
            csv_text = open_url(url).read()
            df = pd.read_csv(StringIO(csv_text), parse_dates=["date"])
        except ImportError:
            try:
                df = pd.read_csv(url, parse_dates=["date"])
            except Exception as e:
                logging.error(f"Pandas read_csv error: {e}")
                return None, f"**Error loading data:** Could not read the file. (Details: {e})"
        except Exception as e:
            logging.error(f"Pyodide open_url error: {e}")
            return None, f"**Error loading data in browser:** Could not fetch data. (Details: {e})"
        
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        return df, None

    # 3. CORE DATA PROCESSING & CALCULATION FUNCTIONS
    def clean_and_prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
        user_data = df.copy()
        user_data.columns = user_data.columns.str.strip().str.lower()

        for col in user_data.select_dtypes(include=['object']).columns:
            user_data[col] = user_data[col].str.lower()

        required_cols = {"date", "lift_name", "weight_kg", "bodyweight_kg", "reps"}
        if not required_cols.issubset(user_data.columns):
            missing = required_cols - set(user_data.columns)
            return None, f"**Missing Columns:** Your data is missing: `{missing}`."

        user_data["date"] = pd.to_datetime(user_data["date"], errors="coerce").dt.date
        user_data["weight_kg"] = pd.to_numeric(user_data["weight_kg"], errors="coerce").replace(0, np.nan)
        user_data["bodyweight_kg"] = pd.to_numeric(user_data["bodyweight_kg"], errors="coerce").replace(0, np.nan)
        user_data["reps"] = pd.to_numeric(user_data["reps"], errors="coerce").fillna(1).astype(int)
        
        user_data = user_data.sort_values(by="date").reset_index(drop=True)
        return user_data, None

    def calculate_sinclair(df: pd.DataFrame, coeff_a: float, coeff_b: float) -> pd.DataFrame:
        df['sinclair_points'] = np.nan
        mask = (df["lift_name"] == "total") & df["weight_kg"].notna() & df["bodyweight_kg"].notna() & (df["bodyweight_kg"] > 0)
        bodyweight = df.loc[mask, "bodyweight_kg"]
        total_weight = df.loc[mask, "weight_kg"]
        sinclair_coeff = np.ones_like(bodyweight, dtype=float)
        bw_ratio_mask = bodyweight <= coeff_b
        ratio = bodyweight[bw_ratio_mask] / coeff_b
        ratio = ratio[ratio > 0]
        sinclair_coeff[bw_ratio_mask] = 10 ** (coeff_a * (np.log10(ratio)) ** 2)
        df.loc[mask, "sinclair_points"] = (total_weight * sinclair_coeff).round(2)
        return df
    
    def add_snatch_cj_spread(df: pd.DataFrame) -> pd.DataFrame:
        try:
            pivot_df = df[df["reps"] == 1].pivot_table(index="date", columns="lift_name", values="weight_kg")
            if {"snatch", "clean & jerk"}.issubset(pivot_df.columns):
                interpolated_df = pivot_df[["snatch", "clean & jerk"]].interpolate(method="linear", limit_direction="both")
                interpolated_df["spread_pct"] = (
                    (interpolated_df["clean & jerk"] - interpolated_df["snatch"]) / interpolated_df["snatch"]
                ).replace([np.inf, -np.inf], np.nan) * 100
                df = pd.merge(df, interpolated_df["spread_pct"].round(2).reset_index(), on="date", how="left")
        except Exception as e:
            warnings.warn(f"Could not calculate C&J spread: {e}")
        return df

    def add_cumulative_personal_bests(df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values(by=["lift_name", "date"])
        df["personal_best_kg"] = df.groupby("lift_name")["weight_kg"].transform(lambda s: s.cummax())
        return df

    def add_lift_bodyweight_ratio(df: pd.DataFrame) -> pd.DataFrame:
        df["lift_bodyweight_ratio"] = np.nan
        mask = (df["reps"] == 1) & df["weight_kg"].notna() & df["bodyweight_kg"].notna()
        df.loc[mask, "lift_bodyweight_ratio"] = (100 * df.loc[mask, "weight_kg"] / df.loc[mask, "bodyweight_kg"]).round(2)
        return df
    
    data_message = mo.md(
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
        ">Processed Weightlifting Data. It looks like we have some great data for you! </span>
    </div>
    """
    )

    # 4. EXECUTION PIPELINE
    data, error = load_data(user_url.value)

    if error:
        final_output = mo.md(error)
    else:
        user_data_df, clean_error = clean_and_prepare_data(data)
        if clean_error:
            final_output = mo.md(clean_error)
        elif user_data_df is None or user_data_df.empty:
            final_output = mo.md("**Processing Stopped:** No valid data after cleaning.")
        else:
            # All checks passed, proceed with processing
            user_data_df = (
                user_data_df
                .pipe(calculate_sinclair, a_coeff.value, b_coeff.value)
                .pipe(add_snatch_cj_spread)
                .pipe(add_cumulative_personal_bests)
                .pipe(add_lift_bodyweight_ratio)
            )
            
            user_data_df = user_data_df.sort_values(by=["date", "lift_name"]).reset_index(drop=True)
            # 5. DISPLAY OUTPUT
            final_output = mo.vstack([
                data_message,
                mo.ui.table(user_data_df, pagination=True, page_size=10)
            ])

    # The last expression in a marimo cell is its output.
    # By assigning either an error or the table to final_output,
    # we ensure the cell always has a valid output without early returns.
    final_output
    
    return user_data_df




@app.cell
def _(mo, user_data_df, pd):
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    # Custom color palette: blue, yellow, black
    lift_colors = [
        "#9D00FF",  # Vibrant Purple 
        "#fa7d00",  # Bright Orange 
        "#222222",  # Very Dark Grey 
        "#0072B2",  # Dark Blue 
        "#009E73",  # Teal/Green 
        "#FC46AA",  # Rose/Pinkish-Purple 
        "#FFF017",  # Greenish Yellow 
        "#1CAAFC",  # Sky Blue 
        "#B4773E",  # Mid Brown 
        "#A3A3A3"   # Light Grey
    ]
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
        lifts_df = df[df["lift_name"].isin(["snatch", "clean & jerk"])]
        fig_lifts = px.line(
            lifts_df,
            x="date",
            y="weight_kg",
            #text="weight_kg",
            color="lift_name",
            title="Weight Lifted Over Time (snatch & Clean and Jerk)",
            labels={"weight_kg": "Weight (kg)", "lift_name": "Lift"},
            markers=True,
            template="bws",
            color_discrete_sequence=lift_colors,
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
        spread_df = df[df["lift_name"] == "clean & jerk"].dropna(subset=["spread_pct"])
        return px.line(
            spread_df,
            x="date",
            y="spread_pct",
            title="clean & jerk - snatch Spread (% of snatch) Over Time",
            labels={"spread_pct": "Spread (% of snatch)"},
            markers=True,
            template="bws",
            color_discrete_sequence=lift_colors,
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
            color_discrete_sequence=lift_colors,
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
            color_discrete_sequence=lift_colors,
        )


        # Unpack the two charts from create_temporal_weight_chart
    fig_lifts, fig_total = create_temporal_weight_chart(user_data_df)
    chart_map = {
        "Temporal Evolution (Bodyweight)": create_bodyweight_chart(user_data_df),
        "Temporal Evolution (Lift kg: snatch & C&J)": fig_lifts,
        "Temporal Evolution (Lift kg: Total)": fig_total,
        "Temporal Evolution (Sinclair)": create_temporal_sinclair_chart(user_data_df),
        "C&J - snatch Spread": create_snatch_cj_spread_chart(user_data_df),
        "Lift / Bodyweight Ratio": create_lift_bodyweight_ratio_chart(user_data_df),
    }
    
    chart_message = mo.md(
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
        ">All Your PR and Stats are here! </span>
    </div>
    """
    )
    
    mo.vstack([
        chart_message,
        # *[mo.md(f"### {title}") for title in chart_map.keys()],
        *[chart for chart in chart_map.values()]
    ])