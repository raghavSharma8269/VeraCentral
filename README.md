# Overview

## Issues Encountered

### 1. Duplicate Columns

- **Problem**: clean_jurisdiction() function was creating duplicate report_date columns
- **Solution**: Removed column reordering since columns were already in correct order

## Verification Steps

1. **Column Count**: Verified no columns were lost during processing
2. **Data Shape**: Confirmed row count remained unchanged
3. **Date Format**: Manually checked sample dates match expected YYYY-mm-dd format
4. **Jurisdiction Cleaning**: Spot-checked that county names were properly cleaned
5. **Data Types**: Verified numeric columns converted correctly and non-numeric values became NaN

## Why This Approach

### Code Structure

- **4 Functions**: Split cleaning into separate functions (snake_case, report_date, clean_jurisdiction, convert_types) for clarity
- **Sequential Processing**: Applied transformations in order - first rename columns, then create dates, then clean jurisdiction, finally convert types
- **Direct Column Access**: Used exact column names ("reporting_month", "reporting_year", "jurisdiction_name") since I had access to the Excel file and knew the structure
- **Simple Logic**: Each function does one thing - rename columns, combine dates, clean text, or convert types
- **String Operations**: Used regex for snake_case conversion and county name cleaning
- **Loop-based Type Conversion**: Iterated through each column to determine if it should be string or numeric

### Technical Choices

- **Pandas**: Used read_excel() and to_csv() as requested
- **String Dates**: Kept dates as strings instead of datetime objects to avoid pandas conversion errors
- **Regex Cleaning**: Used re.search() to find "County" in jurisdiction names and keep only that part
- **Numeric Detection**: Applied conversion function to each value, converted non-numeric indicators to np.nan
