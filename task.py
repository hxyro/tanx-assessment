import pandas as pd
import os, sys

def read_csv(file_path):
    """
    Read the CSV file.

    Args:
        file_path (str): The path to the CSV file to be read.

    Returns:
        tuple: A tuple containing the DataFrame and an error message (if any).
    """

    ## Try to read the CSV file into a DataFrame.
    try:
        df = pd.read_csv(file_path)
        return df, None
    ## Handle the case where the file is not found.
    except FileNotFoundError:
        return None, f"[Error]: Expected '{file_path}' but found no matching results."
    ## Handle the case where the file is empty.
    except pd.errors.EmptyDataError:
        return None, f"[Error]: The file '{file_path}' is empty."
    ## Handle parsing errors.
    except pd.errors.ParserError:
        return None, f"[Error]: Unable to parse the file '{file_path}'. Please check the file format."

def validate_data(df):
    """
    Validate column(s) for empty values, non-numeric or non-positive values.
    
    Args:
        df (DataFrame): The DataFrame to validate.

    Returns:
        tuple: A tuple containing a boolean indicating validation success and an error message (if any).
    """

    ## Define the desired columns.
    columns = [
        'order_id',
        'customer_id',
        'order_date',
        'product_id',
        'product_name',
        'product_price',
        'quantity'
    ]

    try:
        ## Check for missing columns.
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"[ERROR]: Expected column(s) {', '.join(missing_columns)} not found in the file.")

        ## Check for empty values in the DataFrame.
        if df.isnull().values.any():
            raise ValueError("[Error]: The DataFrame contains empty values.")

        ## Convert 'product_price' and 'quantity' columns to numeric, while handling errors.
        df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

        ## Validate that 'product_price' and 'quantity' have positive values.
        if not (df['product_price'] > 0).all():
            raise ValueError("Column 'product_price' should contain positive numeric values.")

        if not (df['quantity'] > 0).all():
            raise ValueError("Column 'quantity' should contain positive numeric values.")

    ## Return False and the error message in case of a ValueError.
    except ValueError as ve:
        return False, str(ve)

    ## Return True and None if validation is successful.
    return True, None

def process_data(df):
    """
    Process the DataFrame.
    
    Args:
        df (DataFrame): The DataFrame to process.

    Returns:
        DataFrame: The processed DataFrame.
    """

    ## Convert 'order_date' to datetime and extract month.
    df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y %H:%M')
    df['month'] = df['order_date'].dt.to_period('M')

    ## Calculate the total value for each order.
    df['total_value'] = df['product_price'] * df['quantity']

    ## Return the processed DataFrame
    return df

def main():
    file = 'orders.csv'
    ## Get the absolute path of the file.
    file_path = os.path.abspath(file)

    ## Read the CSV file.
    df, error = read_csv(file_path)
    if error: ## Print error message if reading fails.
        print(f"\033[91m{error}\033[0m", file=sys.stderr)
        return
    
    ## Validate the DataFrame.
    if df is not None:
        valid, error = validate_data(df)
        if not valid: ## Print error message if validation fails.
            print(f"\033[91m{error}\033[0m", file=sys.stderr)
            return

        ## Process the DataFrame.
        df = process_data(df)

        ## Calculate and display various revenue metrics.
        monthly_revenue = df.groupby('month')['total_value'].sum() 
        product_revenue = df.groupby('product_id')['total_value'].sum().head(50) # NOTE: Limiting to 50 due to large size of dataset.
        customer_revenue = df.groupby('customer_id')['total_value'].sum().sort_values(ascending=False).head(50) # NOTE: Limiting to 50 due to large size of dataset.

        top_customers = customer_revenue.head(10)

        ## Print the revenue metrics in markdown format.
        print(f"Revenue by Months: \n{monthly_revenue.to_markdown()}")
        print(f"\nRevenue by Product: \n{product_revenue.to_markdown()}")
        print(f"\nRevenue by Customer: \n{customer_revenue.to_markdown()}")
        print(f"\nTop 10 Customers by Revenue: \n{top_customers.to_markdown()}")

if __name__ == "__main__":
    main()
