import io
import requests
import sqlalchemy
import pandas as pd
import pandera as pa

# Set base URL and URL extensions
base_url = 'https://1f12d5f7-2ab1-47a2-a83f-e14e4f5465a1.mock.pstmn.io/'
url_extensions = ['test-one', 'test-two']

# Define data table schema using Pandera
schema = pa.DataFrameSchema({
    'timestamp': pa.Column(pa.DateTime, nullable=False),
    'value': pa.Column(pa.Int),
    'category': pa.Column(pa.String, checks=[pa.Check.isin(['A', 'B', 'C'])])
})

# Setup database connection
DB_USER = 'postgres'
DB_PASSWORD = 'password'
DB_HOST = 'postgres'
DB_PORT = '5432'
DB_NAME = 'technical_test'
engine = sqlalchemy.create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Iterate over URL extensions
for extension in url_extensions:
    url = base_url + extension

    print('*' * 80)

    try:
        # Request CSV data from the API 
        response = requests.get(url)
        response.raise_for_status()

        # Read CSV data into a pandas dataframe
        df = pd.read_csv(io.BytesIO(response.content))
    except requests.RequestException as e:
        print(f'Error fetching data for {extension}: {e}')
        continue

    try:
        # Convert column data types
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Validate schema
        schema.validate(df)
    except pa.errors.SchemaError as e:
        print(f"Schema validation error for {extension}: {e}")
        continue

    # Check for outliers using the interquartile range
    q1 = df['value'].quantile(0.25)
    q3 = df['value'].quantile(0.75)
    iqr = q3 - q1
    df['outlier'] = (df['value'] < (q1 - 1.5 * iqr)) | (df['value'] > (q3 + 1.5 * iqr))

    # Insert into SQL container if no outliers are detected 
    if not df['outlier'].any():
        df = df.drop(columns='outlier')
        df.to_sql('output_table', engine, if_exists='replace', index=False)