import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler

# Load the rawdata
df = pd.read_csv('C:\\Users\\zqy\\Documents\\over regression\\git_behavior_trace\\merge_alldata.csv')

# Identify numeric columns
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

# Exclude 'score_AI', 'score_alone', 'score_overreliance' from features
features = [col for col in numeric_columns if col not in ['score_AI', 'score_alone', 'score_overreliance']]

# Preprocessing steps
transformed_features = []


# List of variables to visualize
# variables = [
#     'average_copy_length','average_highlight_length','average_mousewheel_distance','average_paste_length','average_prompt_duration','average_prompt_length','click_count','copy_count','delete_count','highlight_count','idle_count','keypress_count','med_copy_length','med_highlight_length','med_idle_duration','med_mousewheel_distance','med_paste_length','median_prompt_duration','median_prompt_length','mousewheel_count','paste_count','prompt_count','total_focus_time','total_idle_duration','total_mouse_movement','total_mousewheel_distance','total_prompt_duration','total_prompt_length','totaltime','windowswitch_count','windowswitch_speed'
# ]

variables = [
    'windowswitch_count_gpt',	'windowswitch_speed_gpt',	'totaltime_gpt',	'click_count_gpt',	'total_mouse_movement_gpt',	'mousewheel_count_gpt',	'total_mousewheel_distance_gpt',	'average_mousewheel_distance_gpt',	'med_mousewheel_distance_gpt',	'copy_count_gpt',	'average_copy_length_gpt',	'med_copy_length_gpt',	'paste_count_gpt',	'average_paste_length_gpt',	'med_paste_length_gpt',	'delete_count_gpt',	'keypress_count_gpt',	'highlight_count_gpt',	'average_highlight_length_gpt',	'med_highlight_length_gpt',	'idle_count_gpt',	'med_idle_duration_gpt',	'total_idle_duration_gpt',	'prompts_count_gpt',	'total_prompts_duration_gpt',	'total_prompts_length_gpt',	'med_prompts_length_gpt',	'totaltime_tasksheet',	'click_count_tasksheet',	'total_mouse_movement_tasksheet',	'mousewheel_count_tasksheet',	'total_mousewheel_distance_tasksheet',	'average_mousewheel_distance_tasksheet',	'med_mousewheel_distance_tasksheet',	'copy_count_tasksheet',	'average_copy_length_tasksheet',	'med_copy_length_tasksheet',	'paste_count_tasksheet',	'average_paste_length_tasksheet',	'med_paste_length_tasksheet',	'delete_count_tasksheet',	'keypress_count_tasksheet',	'highlight_count_tasksheet',	'average_highlight_length_tasksheet',	'med_highlight_length_tasksheet',	'idle_count_tasksheet',	'med_idle_duration_tasksheet',	'total_idle_duration_tasksheet'

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