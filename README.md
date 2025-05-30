# Olympic Weightlifting Statistics Dashboard

This dashboard provides a way to visualize and analyze your Olympic weightlifting training data. It calculates Sinclair points, tracks personal bests, shows lift-to-bodyweight ratios, and more.

## How to Use

To use this dashboard, follow these steps:

### 1. Configure Sinclair Coefficients

Before uploading your data, you need to set up the coefficients used for calculating Sinclair points. Sinclair points are a way to compare lifters across different bodyweight categories.

* **Select Sinclair Gender**: At the top of the dashboard, you will find a dropdown menu labeled "Sinclair Gender". You **must** select either "Male" or "Female" from this menu. This choice determines the standard Sinclair 'A' and 'B' coefficients used in the calculation.
* **Adjust Coefficients (Optional)**: After selecting a gender, the corresponding 'A' and 'B' coefficients will be displayed in input fields. These are pre-filled with standard values. However, if you need to use different coefficients (for example, to match the very latest official IWF - International Weightlifting Federation - tables, or for a custom calculation), you can manually change the numbers in these fields.

### 2. Prepare Your Data CSV File

The dashboard expects your training data to be in a CSV (Comma Separated Values) file format. You need to ensure your CSV file has the correct columns and data types.

**Required Columns:**

The following columns **must** be present in your CSV file:

| Column Name            | Data Type        | Description                                                                 | Example         |
| ---------------------- | ---------------- | --------------------------------------------------------------------------- | --------------- |
| `date`                 | Text (YYYY-MM-DD) | The date of the training session or lift.                                   | `2023-10-27`    |
| `lift_name`            | Text             | The name of the lift. Common examples: "Snatch", "Clean & Jerk", "Front Squat" | `Snatch`        |
| `weight_kg`            | Number           | The weight lifted in kilograms.                                             | `105.5`         |
| `bodyweight_kg`        | Number           | Your bodyweight in kilograms on the day of the lift.                        | `77.2`          |
| `self_evaluated_shape` | Integer (1-5)    | A rating from 1 to 5 of how you felt during the session (1=bad, 5=great). | `4`             |

**Example CSV Data:**

Here's what a few rows of your CSV file might look like:

```csv
date,lift_name,weight_kg,bodyweight_kg,self_evaluated_shape
2023-01-15,Snatch,90,75.5,3
2023-01-15,Clean & Jerk,110,75.5,3
2023-01-17,Snatch,92.5,75.8,4
2023-01-17,Clean & Jerk,115,75.8,4
2023-01-19,Front Squat,150,76.0,5
```

**Important Notes for Data Preparation:**

* Ensure the column names in your CSV file exactly match those listed above (e.g., `lift_name`, not `Lift Name`).
* The date format should be Year-Month-Day (YYYY-MM-DD).
* Use a period (`.`) as the decimal separator for `weight_kg` and `bodyweight_kg` if you have fractional values.

### 3. Upload Your CSV File

Once you have:

1. Selected the Sinclair Gender and (if necessary) adjusted the A and B coefficients, and
2. Prepared your training data in a CSV file according to the template above,

you are ready to generate your statistics.

Click on the **"Upload Local CSV File"** button in the dashboard. A file dialog will open, allowing you to select the CSV file you prepared.

After you select and upload the file, the dashboard will automatically process the data and display various charts and statistics, including:

* Temporal evolution of your bodyweight.
* Temporal evolution of the weight you lifted (in kg).
* Temporal evolution of your Sinclair points for Snatch and Clean & Jerk.
* The spread between your Clean & Jerk and Snatch percentages.
* Your lift-to-bodyweight ratio over time.
* Your self-evaluated shape over time.

Et voilà:

![](./dashboard.png)

Enjoy analyzing your progress!
