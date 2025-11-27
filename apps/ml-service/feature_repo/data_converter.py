import pandas as pd
from datetime import datetime

# Read CSV file
df = pd.read_csv('data/resul_data.csv')

# Add event_timestamp column (required by Feast)
df['event_timestamp'] = datetime.now()

# Save as Parquet
df.to_parquet('data/company_data.parquet', index=False) 