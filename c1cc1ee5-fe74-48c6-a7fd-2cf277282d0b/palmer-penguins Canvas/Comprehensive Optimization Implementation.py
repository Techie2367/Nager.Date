import pandas as pd
import numpy as np
import time

print("="*80)
print("COMPREHENSIVE DATA OPTIMIZATION IMPLEMENTATION")
print("="*80)

print("\n📊 PART 1: OPTIMIZED DATA LOADING")
print("-"*80)

# Load with optimal settings
optimal_dtypes = {
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

# Benchmark loading performance
iterations = 20
baseline_times = []
optimized_times = []

print(f"Running {iterations} iterations for statistically robust benchmarks...\n")

# Baseline approach
for _ in range(iterations):
    start = time.perf_counter()
    df_baseline = pd.read_csv('penguins.csv')
    baseline_times.append((time.perf_counter() - start) * 1000)

# Optimized approach
for _ in range(iterations):
    start = time.perf_counter()
    df_optimized = pd.read_csv('penguins.csv', dtype=optimal_dtypes)
    optimized_times.append((time.perf_counter() - start) * 1000)

baseline_avg = np.mean(baseline_times)
baseline_std = np.std(baseline_times)
optimized_avg = np.mean(optimized_times)
optimized_std = np.std(optimized_times)

print(f"✓ Baseline Loading (default dtypes):")
print(f"  Average: {baseline_avg:.3f} ± {baseline_std:.3f} ms")
print(f"  Min: {min(baseline_times):.3f} ms | Max: {max(baseline_times):.3f} ms")

print(f"\n✓ Optimized Loading (categorical + smaller numeric dtypes):")
print(f"  Average: {optimized_avg:.3f} ± {optimized_std:.3f} ms")
print(f"  Min: {min(optimized_times):.3f} ms | Max: {max(optimized_times):.3f} ms")

memory_baseline = df_baseline.memory_usage(deep=True).sum()
memory_optimized = df_optimized.memory_usage(deep=True).sum()
memory_reduction = ((memory_baseline - memory_optimized) / memory_baseline) * 100

print(f"\n💾 Memory Optimization:")
print(f"  Baseline: {memory_baseline/1024:.2f} KB")
print(f"  Optimized: {memory_optimized/1024:.2f} KB")
print(f"  🎯 Memory Reduction: {memory_reduction:.1f}%")


print("\n\n⚡ PART 2: VECTORIZED PROCESSING OPTIMIZATION")
print("-"*80)

# Create clean dataset for processing benchmarks
df_clean = df_optimized.dropna()

# Test 1: Loop vs Vectorization for calculations
print("\n1. Calculation Performance: Loop vs Vectorization")
print("   Task: Calculate body mass index (BMI) metric\n")

# Loop approach (inefficient)
start = time.perf_counter()
bmi_loop = []
for _, row in df_clean.iterrows():
    bmi_loop.append(row['body_mass_g'] / (row['flipper_length_mm'] ** 2))
loop_time = (time.perf_counter() - start) * 1000

# Vectorized approach
start = time.perf_counter()
bmi_vectorized = df_clean['body_mass_g'] / (df_clean['flipper_length_mm'] ** 2)
vectorized_time = (time.perf_counter() - start) * 1000

vectorization_speedup = ((loop_time - vectorized_time) / loop_time) * 100
speedup_factor = loop_time / vectorized_time

print(f"   Loop approach: {loop_time:.3f} ms")
print(f"   Vectorized approach: {vectorized_time:.3f} ms")
print(f"   🎯 Speedup: {speedup_factor:.1f}x faster ({vectorization_speedup:.1f}% improvement)")


# Test 2: GroupBy with optimized dtypes
print("\n\n2. GroupBy Performance: Standard vs Optimized dtypes")
print("   Task: Multi-column aggregation by species and island\n")

df_standard = pd.read_csv('penguins.csv').dropna()

# Standard dtypes
start = time.perf_counter()
agg_standard = df_standard.groupby(['species', 'island']).agg({
    'bill_length_mm': ['mean', 'std', 'min', 'max'],
    'body_mass_g': ['mean', 'std', 'min', 'max'],
    'flipper_length_mm': ['mean', 'std', 'min', 'max']
})
standard_agg_time = (time.perf_counter() - start) * 1000

# Optimized dtypes
start = time.perf_counter()
agg_optimized = df_clean.groupby(['species', 'island']).agg({
    'bill_length_mm': ['mean', 'std', 'min', 'max'],
    'body_mass_g': ['mean', 'std', 'min', 'max'],
    'flipper_length_mm': ['mean', 'std', 'min', 'max']
})
optimized_agg_time = (time.perf_counter() - start) * 1000

groupby_speedup = ((standard_agg_time - optimized_agg_time) / standard_agg_time) * 100

print(f"   Standard dtypes: {standard_agg_time:.3f} ms")
print(f"   Optimized dtypes: {optimized_agg_time:.3f} ms")
print(f"   🎯 Speedup: {groupby_speedup:.1f}% improvement")


# Test 3: Filtering optimization
print("\n\n3. Filtering Performance: Query vs Boolean indexing")
print("   Task: Complex multi-condition filter\n")

# Boolean indexing
start = time.perf_counter()
for _ in range(100):
    filtered_bool = df_clean[(df_clean['bill_length_mm'] > 40) & 
                              (df_clean['body_mass_g'] > 3500) & 
                              (df_clean['species'] == 'Adelie')]
boolean_time = (time.perf_counter() - start) * 1000

# Query method (optimized)
start = time.perf_counter()
for _ in range(100):
    filtered_query = df_clean.query('bill_length_mm > 40 & body_mass_g > 3500 & species == "Adelie"')
query_time = (time.perf_counter() - start) * 1000

filter_speedup = ((boolean_time - query_time) / boolean_time) * 100

print(f"   Boolean indexing: {boolean_time:.3f} ms (100 iterations)")
print(f"   Query method: {query_time:.3f} ms (100 iterations)")
print(f"   🎯 Speedup: {abs(filter_speedup):.1f}% {'improvement' if filter_speedup > 0 else 'slower'}")


print("\n\n📈 PART 3: OPTIMIZATION SUMMARY")
print("-"*80)

# Calculate overall improvements
total_baseline_time = baseline_avg + loop_time + standard_agg_time
total_optimized_time = optimized_avg + vectorized_time + optimized_agg_time
overall_speedup = ((total_baseline_time - total_optimized_time) / total_baseline_time) * 100

optimization_results = {
    'loading_baseline_ms': baseline_avg,
    'loading_optimized_ms': optimized_avg,
    'memory_baseline_kb': memory_baseline / 1024,
    'memory_optimized_kb': memory_optimized / 1024,
    'memory_reduction_pct': memory_reduction,
    'calculation_loop_ms': loop_time,
    'calculation_vectorized_ms': vectorized_time,
    'vectorization_speedup_factor': speedup_factor,
    'groupby_standard_ms': standard_agg_time,
    'groupby_optimized_ms': optimized_agg_time,
    'groupby_speedup_pct': groupby_speedup,
    'overall_speedup_pct': overall_speedup
}

print(f"\n🏆 KEY PERFORMANCE WINS:")
print(f"\n1. Memory Efficiency:")
print(f"   ✓ {memory_reduction:.1f}% memory reduction through dtype optimization")
print(f"   ✓ Enables processing {1/(1-memory_reduction/100):.1f}x more data in same RAM")

print(f"\n2. Processing Speed:")
print(f"   ✓ {speedup_factor:.1f}x faster calculations with vectorization")
print(f"   ✓ {groupby_speedup:.1f}% faster aggregations with categorical dtypes")

print(f"\n3. Overall Pipeline Improvement:")
print(f"   ✓ Baseline total: {total_baseline_time:.3f} ms")
print(f"   ✓ Optimized total: {total_optimized_time:.3f} ms")
print(f"   ✓ 🎯 Overall speedup: {overall_speedup:.1f}%")

print(f"\n💡 SCALABILITY INSIGHTS:")
rows = len(df_clean)
print(f"   Current dataset: {rows} rows")
print(f"   At 1M rows, estimated time savings:")
print(f"     • Vectorization: ~{(loop_time - vectorized_time) * (1_000_000/rows) / 1000:.1f} seconds saved")
print(f"     • Memory saved: ~{(memory_baseline - memory_optimized) * (1_000_000/rows) / (1024*1024):.1f} MB")

print("\n" + "="*80)