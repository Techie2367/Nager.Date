import pandas as pd

# Load the penguins dataset from the filesystem
penguins_df = pd.read_csv('penguins.csv')

# Display basic information about the dataset
print(f"Dataset shape: {penguins_df.shape}")
print(f"\nColumn names and types:")
print(penguins_df.dtypes)
print(f"\nFirst few rows:")

# Preview the dataset
penguins_df.head(10)