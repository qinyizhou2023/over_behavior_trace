import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler

# Load the data
df = pd.read_csv('behavior_result.csv')

# Identify numeric columns
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

# Exclude 'score_AI', 'score_alone', 'score_overreliance' from features
features = [col for col in numeric_columns if col not in ['score_AI', 'score_alone', 'score_overreliance']]

# Preprocessing steps
transformed_features = []

for feature in features:
    stat, p = stats.shapiro(df[feature])
    print(f'{feature}: p-value = {p}')
    if p < 0.005:
        transformed_features.append(feature)

# Log transform the features
for feature in transformed_features:
    df[feature] = np.log(df[feature] + 1e-10)  # Adding small constant to avoid log(0)

# Replace infinities with NaN
df = df.replace([np.inf, -np.inf], np.nan)

# Fill NaN values with the mean of the column (only for numeric columns)
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Standardize the features
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# Check for multicollinearity
corr = df[features].corr()
highly_correlated_features = []
for i in range(len(corr.columns)):
    for j in range(i):
        if abs(corr.iloc[i, j]) > 0.8:
            highly_correlated_features.append((corr.columns[i], corr.columns[j]))

# Randomly select one feature from each pair of highly correlated features
features_to_drop = []
for feature1, feature2 in highly_correlated_features:
    if feature1 not in features_to_drop:
        features_to_drop.append(feature2)

# Drop the highly correlated features
df = df.drop(features_to_drop, axis=1)

print(f'Features dropped due to high correlation: {features_to_drop}')

# List of variables to visualize
variables = [
    'total_mouse_movement_gpt', 'mousewheel_count_gpt', 'total_mousewheel_distance_gpt',
    'med_highlight_length_gpt', 'med_idle_duration_gpt', 'prompts_count_gpt',
    'delete_count_tasksheet', 'keypress_count_tasksheet', 'med_highlight_length_tasksheet',
    'med_idle_duration_tasksheet'
]

# Function to create and save a plot
def create_plot(x, y, data, filename):
    plt.figure(figsize=(10, 6))
    sns.regplot(x=x, y=y, data=data, scatter_kws={'alpha':0.5})
    plt.title(f'{x} vs {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig(filename)
    plt.close()

# Create a plot for each variable (if it exists in the dataframe)
for var in variables:
    if var in df.columns:
        create_plot(var, 'score_overreliance', df, f'{var}_vs_overreliance.png')
    else:
        print(f"Warning: {var} not found in the dataframe. Skipping this variable.")

print("All plots have been created and saved.")

# Create a correlation heatmap
plt.figure(figsize=(12, 10))
correlation_vars = [var for var in variables if var in df.columns] + ['score_overreliance']
sns.heatmap(df[correlation_vars].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

print("Correlation heatmap has been created and saved.")