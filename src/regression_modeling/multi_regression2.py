import pandas as pd
import json
import numpy as np
from statsmodels.regression import linear_model
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures

# 读取JSON文件
with open(r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\scorecounting_30ppl\merge_data_gpt.json', 'r') as file:
    data = json.load(file)

# 将JSON数据转换为DataFrame
df = pd.DataFrame(data)

# 移除'filename'列，因为它不是数值型变量
df = df.drop('filename', axis=1)

# 将所有列转换为数值型
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 处理缺失值（如果有的话）
df = df.fillna(df.median())

# 设置因变量y为'overreliance_score'
y = df['overreliance_score']

# 设置自变量X，不包括'overreliance_score'和'paste_count'
X = df.drop(['overreliance_score', 'paste_count'], axis=1)

# 生成交互项
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
x_interaction = poly.fit_transform(X)

# 获取特征名称
feature_names = poly.get_feature_names_out(X.columns)

# 创建包含交互项的新DataFrame
interaction_df = pd.DataFrame(x_interaction, columns=feature_names)

# 使用OLS拟合模型
interaction_model = linear_model.OLS(y, interaction_df).fit()

# 打印模型摘要
print(interaction_model.summary())

# 找出p值小于0.05的显著交互项
significant_interactions = interaction_model.pvalues[interaction_model.pvalues < 0.05]

print("\n显著的交互项（p < 0.05）：")
for var, p_val in significant_interactions.items():
    print(f"{var}: p-value = {p_val}")

# 按p值排序，找出最显著的5个交互项
most_significant = significant_interactions.sort_values().head(5)

print("\n最显著的5个交互项：")
for var, p_val in most_significant.items():
    print(f"{var}: p-value = {p_val}")