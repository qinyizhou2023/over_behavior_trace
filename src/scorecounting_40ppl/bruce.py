import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler

# 读取CSV文件
df = pd.read_csv('merge_gpt.csv')

# 显示数据的前几行和描述性统计
print(df.head())
print(df.describe())

# 确定可能需要转换的特征
features = df.columns.drop(['filename', 'overreliance_score'])
transformed_features = []
for feature in features:
    if df[feature].dtype == 'object':
        print(f"Skipping {feature} as it's not numeric")
        continue
    if df[feature].isnull().any() or (df[feature] <= 0).any():
        print(f"Skipping {feature} due to null or non-positive values")
        continue
    try:
        stat, p = stats.shapiro(df[feature])
        print(f'{feature}: p-value = {p}')
        if p < 0.05:  # 使用更常见的0.05作为阈值
            transformed_features.append(feature)
    except Exception as e:
        print(f"Error processing {feature}: {str(e)}")

print(f'Transformed features: {transformed_features}')

# 转换特征
for feature in transformed_features:
    df[feature] = np.log1p(df[feature])  # 使用log1p来处理可能的零值

# 标准化特征
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# 检查多重共线性
corr = df[features].corr()

# 高度相关的特征列表
highly_correlated_features = []
for i in range(len(corr.columns)):
    for j in range(i):
        if abs(corr.iloc[i, j]) > 0.8:
            highly_correlated_features.append((corr.columns[i], corr.columns[j]))

# 从每对高度相关的特征中随机选择一个
features_to_drop = []
for feature1, feature2 in highly_correlated_features:
    if feature1 not in features_to_drop:
        features_to_drop.append(feature2)

# 删除高度相关的特征
df = df.drop(features_to_drop, axis=1)

print(f'Features to drop: {features_to_drop}')

# 更新特征列表
features = [col for col in df.columns if col not in ['filename', 'overreliance_score']]

# 多元线性回归
X = df[features]
y = df['overreliance_score']

# 添加常数项
X = sm.add_constant(X)

# 拟合模型
model = sm.OLS(y, X).fit()

# 打印摘要
print(model.summary())

# 创建p值小于0.05的特征列表
significant_features = model.pvalues[model.pvalues < 0.05].index.tolist()
print(f'Significant features: {significant_features}')