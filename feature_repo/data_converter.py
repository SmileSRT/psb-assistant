import pandas as pd
from datetime import datetime
import os

# Define paths
input_path = os.path.join(os.path.dirname(__file__), 'data', 'resul_data.csv')
output_path = os.path.join(os.path.dirname(__file__), 'data', 'company_data.parquet')

# Read CSV file
df = pd.read_csv(input_path)

# Drop the Unnamed: 0 column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1)

# Convert event_timestamp to datetime if it exists, otherwise create it
if 'event_timestamp' in df.columns:
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
else:
    df['event_timestamp'] = datetime.now()

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save as Parquet
df.to_parquet(output_path, index=False) 