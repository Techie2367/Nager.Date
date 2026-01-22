import pandas as pd
import time
import os

print("="*70)
print("DATA LOADING PERFORMANCE BENCHMARK")
print("="*70)

# File information
file_path = 'penguins.csv'
file_size = os.path.getsize(file_path)
print(f"\n1. FILE INFORMATION")
print("-" * 70)
print(f"File: {file_path}")
print(f"File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")

# Benchmark different loading methods
results = {}

print(f"\n2. LOADING METHOD BENCHMARKS")
print("-" * 70)

# Method 1: Standard pd.read_csv
iterations = 10
times = []
for i in range(iterations):
    start = time.perf_counter()
    _df1 = pd.read_csv(file_path)
    end = time.perf_counter()
    times.append(end - start)

avg_time = sum(times) / len(times)
min_time = min(times)
max_time = max(times)
results['standard_read_csv'] = avg_time

print(f"\nMethod 1: pd.read_csv() [Standard]")
print(f"  Iterations: {iterations}")
print(f"  Average time: {avg_time*1000:.3f} ms")
print(f"  Min time: {min_time*1000:.3f} ms")
print(f"  Max time: {max_time*1000:.3f} ms")
print(f"  Std dev: {(sum((t - avg_time)**2 for t in times) / len(times))**0.5 * 1000:.3f} ms")

# Method 2: With dtype specification
times = []
dtypes = {
    'rowid': 'int32',
    'species': 'category',
    'island': 'category',
    'bill_length_mm': 'float32',
    'bill_depth_mm': 'float32',
    'flipper_length_mm': 'float32',
    'body_mass_g': 'float32',
    'sex': 'category',
    'year': 'int16'
}

for i in range(iterations):
    start = time.perf_counter()
    _df2 = pd.read_csv(file_path, dtype=dtypes)
    end = time.perf_counter()
    times.append(end - start)

avg_time_dtype = sum(times) / len(times)
results['read_csv_with_dtypes'] = avg_time_dtype

print(f"\nMethod 2: pd.read_csv() [With dtype optimization]")
print(f"  Iterations: {iterations}")
print(f"  Average time: {avg_time_dtype*1000:.3f} ms")
print(f"  Speedup: {(avg_time/avg_time_dtype - 1)*100:+.1f}%")

# Method 3: With engine specification
times = []
for i in range(iterations):
    start = time.perf_counter()
    _df3 = pd.read_csv(file_path, engine='c')
    end = time.perf_counter()
    times.append(end - start)

avg_time_engine = sum(times) / len(times)
results['read_csv_c_engine'] = avg_time_engine

print(f"\nMethod 3: pd.read_csv() [C engine explicit]")
print(f"  Iterations: {iterations}")
print(f"  Average time: {avg_time_engine*1000:.3f} ms")
print(f"  Speedup: {(avg_time/avg_time_engine - 1)*100:+.1f}%")

# Memory comparison
print(f"\n3. MEMORY USAGE COMPARISON")
print("-" * 70)
df_standard = pd.read_csv(file_path)
df_optimized = pd.read_csv(file_path, dtype=dtypes)

mem_standard = df_standard.memory_usage(deep=True).sum()
mem_optimized = df_optimized.memory_usage(deep=True).sum()

print(f"Standard loading: {mem_standard/1024:.2f} KB")
print(f"Optimized dtypes: {mem_optimized/1024:.2f} KB")
print(f"Memory savings: {(1 - mem_optimized/mem_standard)*100:.1f}%")

# Processing rate calculation
print(f"\n4. PROCESSING RATES")
print("-" * 70)
rows_per_sec = df_standard.shape[0] / avg_time
data_points_per_sec = (df_standard.shape[0] * df_standard.shape[1]) / avg_time
mb_per_sec = (file_size / (1024*1024)) / avg_time

print(f"Rows/second: {rows_per_sec:,.0f}")
print(f"Data points/second: {data_points_per_sec:,.0f}")
print(f"MB/second: {mb_per_sec:.2f}")

# Store performance baseline
performance_baseline = {
    'file_size_kb': file_size / 1024,
    'avg_load_time_ms': avg_time * 1000,
    'optimized_load_time_ms': avg_time_dtype * 1000,
    'memory_standard_kb': mem_standard / 1024,
    'memory_optimized_kb': mem_optimized / 1024,
    'rows_per_second': rows_per_sec
}

print("\n" + "="*70)