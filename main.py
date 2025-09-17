import pandas as pd
import re
import numpy as np
from datetime import datetime

def snake_case(col_name):
    # Convert column names to snake_case
    col_name = str(col_name).strip()
    col_name = re.sub(r'[-\s]+', '_', col_name)
    col_name = col_name.lower()
    return col_name

def report_date(df):
    def make_last_day(row):
        month = int(row["reporting_month"])
        year = int(row["reporting_year"])
        
        # Get last day of the month
        date = pd.Period(f"{year}-{month}").end_time.date()
        return date.strftime('%Y-%m-%d')
    
    # Create new report_date column
    df['report_date'] = df.apply(make_last_day, axis=1)
    
    # Drop original month/year columns
    df = df.drop(columns=['reporting_month', 'reporting_year'])
    
    # Put report_date first
    cols = [col for col in df.columns if col != 'report_date']
    df = df[['report_date'] + cols]
    
    return df

def clean_jurisdiction(df):
    jurisdiction_col = 'jurisdiction_name'
    
    def clean_name(name):
        name_str = str(name).strip()
        # Keep only text up to and including "County"
        county_match = re.search(r'^(.*?county)', name_str, re.IGNORECASE)
        if county_match:
            return county_match.group(1).strip()
        return name_str
    
    df[jurisdiction_col] = df[jurisdiction_col].apply(clean_name)
    
    return df

def convert_types(df):
    for col in df.columns:
        if col == 'report_date':
            # Convert to datetime.date objects
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d').dt.date
        elif col == 'jurisdiction_name':
            df[col] = df[col].astype('string')
        else:
            def convert_to_numeric(val):
                if pd.isna(val):
                    return np.nan
                val_str = str(val).strip().upper()
                # Convert non numeric indicators to np.nan
                if val_str in ['D', 'U', 'N/A', 'NA', '', 'NULL', 'NONE']:
                    return np.nan
                try:
                    return float(val_str)
                except:
                    return np.nan
            
            numeric_series = df[col].apply(convert_to_numeric)
            if numeric_series.notna().sum() > 0:
                non_na_values = numeric_series.dropna()
                # Use integer type if all values are whole numbers
                if len(non_na_values) > 0 and all(val == int(val) for val in non_na_values):
                    df[col] = numeric_series.astype('Int64')
                else:
                    df[col] = numeric_series.astype('float64')
            else:
                df[col] = df[col].astype('string')
    
    return df

if __name__ == "__main__":
    file = "September_2024.xlsx"
    output_file = "processed_september_2024.csv"
    
    # Read and process data
    df = pd.read_excel(file)
    df.columns = [snake_case(col) for col in df.columns]
    df = report_date(df)
    df = clean_jurisdiction(df)
    df = convert_types(df)
    df.to_csv(output_file, index=False)