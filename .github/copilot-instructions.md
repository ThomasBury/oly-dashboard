# Copilot Instructions for Olympic Weightlifting Dashboard

## General Guidance

- **Use Context7** for current documentation when discussing frameworks, libraries, or APIs.

## Project Architecture

- This project is a Marimo-based interactive dashboard for Olympic weightlifting data analysis.
- The main entry point is `dashboard.py`, structured as a sequence of Marimo cells (functions decorated with `@app.cell`).
- Data flows from user input (Google Sheets CSV URL) through data cleaning, metric calculation, and visualization, all within the notebook-style script.

## Key Workflows

- **Data Input:** Users provide a published Google Sheets CSV URL. The dashboard expects columns: `date`, `lift_name`, `weight_kg`, `bodyweight_kg`, `reps`, etc.
- **Sinclair Coefficients:** Users select gender and can adjust Sinclair A/B coefficients. These are used for normalized scoring.
- **Data Processing:** Data is loaded, cleaned, and processed in a pipeline of functions (see `dashboard.py`, e.g., `clean_and_prepare_data`, `calculate_sinclair`, etc.).
- **Visualization:** Uses Plotly (via Marimo) for interactive charts. Custom color palettes and templates are defined in each cell.

## Conventions & Patterns

- **Marimo Cells:** Each logical step (input, processing, visualization) is a separate `@app.cell` function. Outputs are returned as the last expression.
- **Styling:** Custom HTML/CSS is used for banners and instructions via `mo.md`.
- **DataFrame Operations:** All data manipulations are performed with Pandas, using `.pipe()` for composability.
- **Error Handling:** User-facing errors are displayed as Markdown via `mo.md`.

## Integration Points

- **External Data:** Relies on Google Sheets published as CSV for both training and competition data.
- **Plotly:** All charts are built with Plotly Express or Graph Objects, using a custom template (`bws`).
- **No traditional build/test scripts:** The dashboard is run interactively via Marimo, not as a standalone app or web server.

## Examples

- See `dashboard.py` for patterns on:
  - Creating user input widgets: `mo.ui.text`, `mo.ui.dropdown`, `mo.ui.number`
  - Data cleaning: `clean_and_prepare_data`
  - Visualization: `create_temporal_weight_chart`, `create_lift_bodyweight_ratio_chart`

## Reference

- For data format and user instructions, see `README.md`.
- For sample data, see `test_oly_data.csv`.