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
    # Olympic Weightlifting Statistics Dashboard
    ## 1. Configure Sinclair Coefficients
    """
    )
    return


@app.cell
def _(mo):
    sinclair_gender = mo.ui.dropdown(
        options=["Female", "Male"], label="Sinclair Gender"
    )
    return (sinclair_gender,)


@app.cell
def _(mo, sinclair_gender):
    if sinclair_gender.value == "Male":
        a_coeff = mo.ui.number(0.722762521, label="Male 'A':", step=1e-9)
        b_coeff = mo.ui.number(193.609, label="Male 'B':", step=1e-3)
        sinclair_coeff = mo.hstack([sinclair_gender, a_coeff, b_coeff])
    else:
        a_coeff = mo.ui.number(0.787004341, label="Female 'A':", step=1e-9)
        b_coeff = mo.ui.number(153.757, label="Female 'B':", step=1e-3)
        sinclair_coeff = mo.hstack([sinclair_gender, a_coeff, b_coeff])

    sinclair_coeff
    return a_coeff, b_coeff


@app.cell
def _(mo):
    mo.md(r"""## 2. Provide your data""")
    return


@app.cell
def _(mo):
    csv_file = mo.ui.file(
        filetypes=[".csv"], kind="button", label="Upload Local CSV File"
    )

    # Display the file uploader in the Marimo notebook
    csv_file
    return (csv_file,)


@app.cell
def _(a_coeff, b_coeff, csv_file):
    import io
    import math
    import pandas as pd


    # Function to load the uploaded file into a Pandas DataFrame
    def load_csv_to_dataframe(file_data):
        content_bytes = file_data.value[0].contents
        content_string = io.StringIO(content_bytes.decode("utf-8"))
        df = pd.read_csv(content_string)
        return df


    def calculate_sinclair_points(
        total_weight_lifted: float,
        bodyweight: float,
        coeff_a: float,
        coeff_b: float,
    ) -> float | None:
        if pd.isna(total_weight_lifted) or pd.isna(bodyweight) or bodyweight <= 0:
            return None
        if bodyweight <= coeff_b:
            ratio = bodyweight / coeff_b
            if ratio <= 0:
                return None
            sinclair_coefficient = 10 ** (coeff_a * (math.log10(ratio)) ** 2)
        else:
            sinclair_coefficient = 1.0
        return round(total_weight_lifted * sinclair_coefficient, 2)


    def add_snatch_cj_spread_pct(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a 'snatch_cj_spread_pct' column to the DataFrame, representing the spread
        between Clean & Jerk and Snatch as a percentage of Snatch over time,
        using linear interpolation for missing values on the same date.

        Args:
            df: Pandas DataFrame with columns 'date' (object), 'lift_name' (object), 'weight_kg' (float64).
                It's assumed the DataFrame is not necessarily sorted by 'date'.

        Returns:
            Pandas DataFrame with an added 'snatch_cj_spread_pct' column.
        """
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date")
        if "spread_pct" in df.columns:
            df = df.drop(columns=["spread_pct"])

        # Pivot the table to have Snatch and Clean & Jerk weights side by side
        pivot_df = df.pivot_table(
            index="date", columns="lift_name", values="weight_kg"
        )

        # Interpolate missing values
        interpolated_df = pivot_df.interpolate(method="linear")

        # Calculate the spread as a percentage of Snatch
        interpolated_df["spread_pct"] = round(
            (
                (interpolated_df["Clean & Jerk"] - interpolated_df["Snatch"])
                / interpolated_df["Snatch"]
            )
            * 100
        )

        # Merge the spread back into the original DataFrame
        merged_df = pd.merge(
            df, interpolated_df["spread_pct"].reset_index(), on="date", how="left"
        )

        return merged_df


    def add_cumulative_personal_best(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a 'personal_best_kg' column showing the personal best weight lifted
        for each 'lift_name' up to that date.

        Args:
            df: Pandas DataFrame with 'date' (object), 'lift_name' (object), and 'weight_kg' (float64) columns.
                It's assumed the DataFrame is sorted by 'date'.

        Returns:
            Pandas DataFrame with an added 'personal_best_kg' column.
        """
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by=["lift_name", "date"])

        def calculate_pb(series):
            return series.cummax()

        df["personal_best_kg"] = df.groupby("lift_name")["weight_kg"].transform(
            calculate_pb
        )

        return df


    def add_lift_bodyweight_ratio(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a 'lift_bodyweight_ratio' column to the DataFrame, calculated as weight_kg / bodyweight_kg.

        Args:
            df: Pandas DataFrame with 'weight_kg' (float64) and 'bodyweight_kg' (float64) columns.

        Returns:
            Pandas DataFrame with an added 'lift_bodyweight_ratio' column.
        """
        df["lift_bodyweight_ratio"] = round(
            100 * df["weight_kg"] / df["bodyweight_kg"]
        )
        return df


    # Load the DataFrame whenever a file is uploaded
    data_df = load_csv_to_dataframe(csv_file)
    data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
    data_df["sinclair_points"] = data_df.apply(
        lambda row: (
            calculate_sinclair_points(
                row["weight_kg"],
                row["bodyweight_kg"],
                a_coeff.value,
                b_coeff.value,
            )
            if row["lift_name"] in ["Snatch", "Clean & Jerk"]
            else None
        ),
        axis=1,
    )
    data_df = add_snatch_cj_spread_pct(data_df)
    data_df = add_cumulative_personal_best(data_df)
    data_df = add_lift_bodyweight_ratio(data_df)
    data_df = data_df.reset_index(drop=True)

    if "Unnamed: 0" in data_df.columns:
        data_df = data_df.drop(columns=["Unnamed: 0"])
    return data_df, pd


@app.cell
def _():
    EXPECTED_COLUMNS = {
        "date": "object",
        "lift_name": "object",
        "weight_kg": "float64",
        "bodyweight_kg": "float64",
        "self_evaluated_shape": "int64",
    }

    REQUIRED_COLUMNS = ["date", "lift_name", "weight_kg", "bodyweight_kg"]
    return


@app.cell
def _(data_df):
    data_df.head(10)
    return


@app.cell
def _(pd):
    import plotly.express as px
    import plotly.graph_objects as go


    def create_temporal_weight_chart(df: pd.DataFrame) -> go.Figure:
        """Generates a line chart of weight lifted over time."""
        return px.line(
            df,
            x="date",
            y="weight_kg",
            color="lift_name",
            title="Weight Lifted Over Time (kg)",
            labels={"weight_kg": "Weight (kg)", "lift_name": "Lift"},
            markers=True,
            template="plotly_white",
        )


    def create_temporal_sinclair_chart(df: pd.DataFrame) -> go.Figure:
        """Generates a line chart of Sinclair points over time."""
        return px.line(
            df,
            x="date",
            y="sinclair_points",
            color="lift_name",
            title="Sinclair Points Over Time",
            labels={"sinclair_points": "Sinclair Points", "lift_name": "Lift"},
            markers=True,
            template="plotly_white",
        )


    def create_snatch_cj_spread_chart(df: pd.DataFrame) -> go.Figure:
        """Generates a line chart of Clean & Jerk - Snatch spread over time."""
        # Filter for Clean & Jerk rows, as 'spread_pct' is relevant here
        spread_df = df[df["lift_name"] == "Clean & Jerk"].dropna(
            subset=["spread_pct"]
        )
        return px.line(
            spread_df,
            x="date",
            y="spread_pct",
            title="Clean & Jerk - Snatch Spread (% of Snatch) Over Time",
            labels={"spread_pct": "Spread (% of Snatch)"},
            markers=True,
            template="plotly_white",
        )


    def create_lift_bodyweight_ratio_chart(df: pd.DataFrame) -> go.Figure:
        """Generates a line chart of Lift / Bodyweight Ratio over time."""
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


    def create_self_evaluated_shape_chart(df: pd.DataFrame) -> go.Figure:
        """Generates a line chart of self-evaluated shape over time."""
        # Group by date and take the mean of self_evaluated_shape if multiple entries per day
        # Or you might want to show all points for self_evaluated_shape if it's per session
        # For now, let's assume one shape per date or take the average for simplicity
        shape_data = (
            df.groupby("date")["self_evaluated_shape"].mean().reset_index()
        )
        return px.line(
            shape_data,
            x="date",
            y="self_evaluated_shape",
            title="Self-Evaluated Shape Over Time (1-5)",
            labels={"self_evaluated_shape": "Shape Rating"},
            markers=True,
            template="plotly_white",
            range_y=[1, 5],  # Ensure y-axis is fixed for shape rating
        )


    def create_bodyweight_chart(df: pd.DataFrame) -> go.Figure:
        """Generates a line chart of Bodyweight over time."""
        dum = df.copy()
        dum = (
            dum[["date", "bodyweight_kg"]].drop_duplicates().sort_values(by="date")
        )
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
        create_self_evaluated_shape_chart,
        create_snatch_cj_spread_chart,
        create_temporal_sinclair_chart,
        create_temporal_weight_chart,
    )


@app.cell
def _(
    create_bodyweight_chart,
    create_lift_bodyweight_ratio_chart,
    create_self_evaluated_shape_chart,
    create_snatch_cj_spread_chart,
    create_temporal_sinclair_chart,
    create_temporal_weight_chart,
    data_df,
    mo,
):
    tabs_content = {
        "Temporal Evolution (Bodyweight)": create_bodyweight_chart(data_df),
        "Temporal Evolution (Lift kg)": create_temporal_weight_chart(data_df),
        "Temporal Evolution (Sinclair)": create_temporal_sinclair_chart(data_df),
        "C&J - Snatch Spread": create_snatch_cj_spread_chart(data_df),
        "Lift / Bodyweight Ratio": create_lift_bodyweight_ratio_chart(data_df),
        "Self-Evaluated Shape": create_self_evaluated_shape_chart(data_df),
    }
    mo.ui.tabs(tabs_content)
    return


if __name__ == "__main__":
    app.run()
