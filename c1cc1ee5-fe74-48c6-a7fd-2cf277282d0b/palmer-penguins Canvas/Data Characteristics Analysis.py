import pandas as pd
import numpy as np

# Comprehensive data characteristics analysis
print("="*70)
print("DATA CHARACTERISTICS ANALYSIS")
print("="*70)

# 1. Dataset size and memory usage
print("\n1. DATASET SIZE & MEMORY")
print("-" * 70)
print(f"Total rows: {penguins_df.shape[0]:,}")
print(f"Total columns: {penguins_df.shape[1]}")
print(f"Total data points: {penguins_df.shape[0] * penguins_df.shape[1]:,}")
print(f"\nMemory usage:")
memory_usage = penguins_df.memory_usage(deep=True)
print(memory_usage)
print(f"\nTotal memory: {memory_usage.sum() / 1024:.2f} KB")

# 2. Data quality assessment
print("\n\n2. DATA QUALITY ASSESSMENT")
print("-" * 70)
missing_data = penguins_df.isnull().sum()
missing_pct = (missing_data / len(penguins_df) * 100).round(2)
quality_df = pd.DataFrame({
    'Missing Values': missing_data,
    'Missing %': missing_pct
})
print(quality_df[quality_df['Missing Values'] > 0])

# 3. Column types and cardinality
print("\n\n3. COLUMN TYPES & CARDINALITY")
print("-" * 70)
for col in penguins_df.columns:
    dtype = penguins_df[col].dtype
    unique_count = penguins_df[col].nunique()
    print(f"{col:25} | Type: {str(dtype):10} | Unique: {unique_count:4}")

# 4. Data distribution statistics
print("\n\n4. NUMERICAL COLUMNS DISTRIBUTION")
print("-" * 70)
numeric_cols = penguins_df.select_dtypes(include=[np.number]).columns
print(penguins_df[numeric_cols].describe())

# 5. Categorical columns summary
print("\n\n5. CATEGORICAL COLUMNS SUMMARY")
print("-" * 70)
categorical_cols = ['species', 'island', 'sex']
for col in categorical_cols:
    print(f"\n{col.upper()}:")
    print(penguins_df[col].value_counts())

# 6. Data complexity indicators
print("\n\n6. DATA COMPLEXITY INDICATORS")
print("-" * 70)
print(f"Numeric columns: {len(numeric_cols)}")
print(f"Categorical columns: {len(categorical_cols)}")
print(f"Average missing values per row: {penguins_df.isnull().sum(axis=1).mean():.2f}")
print(f"Rows with any missing data: {penguins_df.isnull().any(axis=1).sum()} ({penguins_df.isnull().any(axis=1).sum()/len(penguins_df)*100:.1f}%)")

# Store insights for downstream blocks
data_insights = {
    'total_rows': penguins_df.shape[0],
    'total_columns': penguins_df.shape[1],
    'memory_kb': memory_usage.sum() / 1024,
    'missing_rows': penguins_df.isnull().any(axis=1).sum(),
    'numeric_cols': len(numeric_cols),
    'categorical_cols': len(categorical_cols)
}

print("\n" + "="*70)