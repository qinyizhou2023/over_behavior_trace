# import json
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_squared_error, mean_absolute_error
# from scipy.stats import pearsonr
# import statsmodels.api as sm
#
# # 改1：读取JSON文件
# #gpt
# with open('C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data_gpt.json','r') as file:
#     user_behavior_data = json.load(file)
# # #tasksheet
# # with open('C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data_tasksheet.json', 'r') as file:
# #     user_behavior_data = json.load(file)
#
#
# # 提取所需数据并转换为DataFrame
# df = pd.DataFrame(user_behavior_data)
# scores_series = df['overreliance_score']
# df = df.drop(columns=['filename', 'overreliance_score'])  # 移除不需要的列
#
# # 归一化特征
# scaler = StandardScaler()
# df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
#
# # 计算相关性和误差指标
# results = {
#     'Pearson Coeff': [],
#     'MSE': [],
#     'MAE': []
# }
#
# for col in df_scaled.columns:
#     pearson_coeff, _ = pearsonr(df_scaled[col], scores_series)
#     mse = mean_squared_error(scores_series, df_scaled[col])
#     mae = mean_absolute_error(scores_series, df_scaled[col])
#
#     results['Pearson Coeff'].append(pearson_coeff)
#     results['MSE'].append(mse)
#     results['MAE'].append(mae)
#
# results_df = pd.DataFrame(results, index=df_scaled.columns)
#
# # 线性回归分析
# X = sm.add_constant(df_scaled)  # 添加常数项
# model = sm.OLS(scores_series, X).fit()
#
# # 输出结果
# print("Pearson 相关系数、MSE 和 MAE：")
# print(results_df)
#
# print("\n线性回归分析结果：")
# print(model.summary())
#


# csv
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# 读取CSV文件
file_path = r"C:\Users\zqy\Documents\over regression\over_behavior_trace\src\regression_modeling\behavior_transformed_features.csv"
df = pd.read_csv(file_path)

# 将 'overreliance_score' 设置为目标变量
target_variable = 'overreliance_score'
scores_series = df[target_variable]

# 删除不需要的列
columns_to_drop = ['filename', target_variable]
features_df = df.drop(columns=columns_to_drop)

# 归一化特征
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(features_df), columns=features_df.columns)

# 计算相关性和误差指标
results = {
    'Pearson Coeff': [],
    'MSE': [],
    'MAE': []
}

for col in df_scaled.columns:
    pearson_coeff, _ = pearsonr(df_scaled[col], scores_series)
    mse = mean_squared_error(scores_series, df_scaled[col])
    mae = mean_absolute_error(scores_series, df_scaled[col])

    results['Pearson Coeff'].append(pearson_coeff)
    results['MSE'].append(mse)
    results['MAE'].append(mae)

results_df = pd.DataFrame(results, index=df_scaled.columns)

# 线性回归分析
X = sm.add_constant(df_scaled)  # 添加常数项
model = sm.OLS(scores_series, X).fit()

# 输出结果
print("Pearson 相关系数、MSE 和 MAE：")
print(results_df)

print("\n线性回归分析结果：")
print(model.summary())

# 保存结果到CSV文件
results_df.to_csv('correlation_results.csv')