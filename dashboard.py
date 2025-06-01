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
        """Load an uploaded CSV file into a Pandas DataFrame.

        Parameters
        ----------
        file_data : marimo.ui.FileUIElement
            The file UI element from Marimo, containing the uploaded CSV data.
            It's expected that `file_data.value[0].contents` yields the
            byte string of the CSV content.

        Returns
        -------
        pd.DataFrame
            A Pandas DataFrame created from the content of the uploaded CSV file.
        """
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
        """Calculate Sinclair points for a weightlifting total.

        The Sinclair coefficient is calculated based on bodyweight relative
        to a coefficient 'B'. If bodyweight is greater than 'B', the
        Sinclair coefficient is 1.0.

        Parameters
        ----------
        total_weight_lifted : float
            The total weight lifted by the athlete in kilograms.
        bodyweight : float
            The athlete's bodyweight in kilograms.
        coeff_a : float
            The 'A' coefficient for Sinclair calculation, specific to gender.
        coeff_b : float
            The 'B' coefficient (bodyweight cap) for Sinclair calculation.

        Returns
        -------
        float or None
            The calculated Sinclair points, rounded to two decimal places.
            Returns None if `total_weight_lifted` or `bodyweight` is NaN,
            or if `bodyweight` is non-positive, or if the ratio for log is non-positive.
        """
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
        """Add Clean & Jerk vs. Snatch spread percentage column.

        Calculates the spread between Clean & Jerk and Snatch as a percentage
        of Snatch weight. This is added as a 'spread_pct' column.
        using linear interpolation for missing values on the same date.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame with 'date', 'lift_name', and 'weight_kg' columns.
            'date' will be converted to datetime objects.

        Returns
        -------
        pd.DataFrame
            DataFrame with an added 'spread_pct' column, rounded to the nearest integer.
        """
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date")
        if "spread_pct" in df.columns:
            df = df.drop(columns=["spread_pct"])

        # Pivot the table to have Snatch and Clean & Jerk weights side by side
        pivot_df = df.pivot_table(index="date", columns="lift_name", values="weight_kg")

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
        """Add cumulative personal best for each lift.

        Calculates and adds a 'personal_best_kg' column, representing the
        highest weight lifted for each 'lift_name' up to each recorded date.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame with 'date', 'lift_name', and 'weight_kg' columns.

        Returns
        -------
        pd.DataFrame
            DataFrame with an added 'personal_best_kg' column.
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
        """Add lift-to-bodyweight ratio column.

        Calculates the ratio of 'weight_kg' to 'bodyweight_kg', expressed as a
        percentage, and adds it as 'lift_bodyweight_ratio'.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame with 'weight_kg' and 'bodyweight_kg' columns.

        Returns
        -------
        pd.DataFrame
            DataFrame with an added 'lift_bodyweight_ratio' column, rounded to the nearest integer.
        """
        df["lift_bodyweight_ratio"] = round(100 * df["weight_kg"] / df["bodyweight_kg"])
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
        """Create a line chart of weight lifted over time.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data to plot. Expected columns are
            'date', 'weight_kg', and 'lift_name'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing weight lifted over time,
            colored by lift name.
        """
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
        """Create a line chart of Clean & Jerk vs. Snatch spread over time.

        The spread is shown as a percentage of Snatch weight.
        This chart filters for 'Clean & Jerk' lift names as 'spread_pct'
        is primarily associated with it.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data. Expected columns: 'date', 'lift_name', 'spread_pct'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing the C&J - Snatch spread percentage.
        """
        spread_df = df[df["lift_name"] == "Clean & Jerk"].dropna(subset=["spread_pct"])
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

    def create_self_evaluated_shape_chart(df: pd.DataFrame) -> go.Figure:
        """Create a line chart of self-evaluated physical shape over time.

        If multiple shape evaluations exist for the same date, their mean
        is plotted. The Y-axis is fixed from 1 to 5.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data. Expected columns: 'date', 'self_evaluated_shape'.

        Returns
        -------
        go.Figure
            A Plotly graph object figure showing self-evaluated shape over time.
        """
        shape_data = df.groupby("date")["self_evaluated_shape"].mean().reset_index()
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
        create_self_evaluated_shape_chart,
        create_snatch_cj_spread_chart,
        create_temporal_sinclair_chart,
        create_temporal_weight_chart,
    )

@app.cell
def _(mo):
    mo.md(
        r"""
    ## 3. Choose a chart to display
    The chart will update automatically based on your selection.
    """
    )
    return

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
    chart_dict = {
        "Temporal Evolution (Bodyweight)": create_bodyweight_chart(data_df),
        "Temporal Evolution (Lift kg)": create_temporal_weight_chart(data_df),
        "Temporal Evolution (Sinclair)": create_temporal_sinclair_chart(data_df),
        "C&J - Snatch Spread": create_snatch_cj_spread_chart(data_df),
        "Lift / Bodyweight Ratio": create_lift_bodyweight_ratio_chart(data_df),
        "Self-Evaluated Shape": create_self_evaluated_shape_chart(data_df),
    }
    chart_selector = mo.ui.dropdown(
        options=chart_dict,
        label="choose a chart",
        searchable=True,
    )
    chart_selector
    return chart_selector


@app.cell
def _(
    chart_selector
):
    chart_selector.value
    return

if __name__ == "__main__":
    app.run()
