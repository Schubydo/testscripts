import pandas as pd
import fuzzy_match 

def premium_drivers(df, current_date = "2024-12-31"):
    # Assume your DataFrame is called `df` and has a 'Date' column
    most_recent_date = pd.to_datetime(current_date)
    current_year = most_recent_date.year
    previous_year = current_year - 1

    # Step 1: Split the DataFrame into current and previous periods
    df['Date'] = pd.to_datetime(df['Date'])
    df_current = df[(df['Date'] >= f"{current_year}-01-01") & (df['Date'] <= f"{current_year}-12-31")]
    df_previous = df[(df['Date'] >= f"{previous_year}-01-01") & (df['Date'] <= f"{previous_year}-12-31")]

    # Step 2: Rename columns in df_previous
    columns_to_rename = {col: f"{col}_previous" for col in df_previous.columns if col not in ['Policy Number', 'Street Address']}
    df_previous = df_previous.rename(columns=columns_to_rename)

    # Step 3: Join the DataFrames using fuzzy match
    df_merged = fuzzy_match(df_current, df_previous, key_columns=['Policy Number', 'Street Address'])

    # Step 4: Calculate premium income change impacts
    df_merged['Participation_Impact'] = (df_merged['Participation'] - df_merged['Participation_previous']) * df_merged['Premium_previous']
    df_merged['Rate_Movement_Impact'] = (df_merged['Rate'] - df_merged['Rate_previous']) * df_merged['Premium_previous']
    df_merged['Inflation_Impact'] = df_merged['Inflation'] * df_merged['Premium_previous']

    # Step 5: Identify new business premiums
    df_current['New/Renew'] = 'New'  # Mark all current rows as new
    new_business_premium = df_current['Premium'].sum()

    # Optional: Summarize the impacts
    summary = {
        "Participation Impact": df_merged['Participation_Impact'].sum(),
        "Rate Movement Impact": df_merged['Rate_Movement_Impact'].sum(),
        "Inflation Impact": df_merged['Inflation_Impact'].sum(),
        "New Business Premium": new_business_premium,
    }

    print(summary)
