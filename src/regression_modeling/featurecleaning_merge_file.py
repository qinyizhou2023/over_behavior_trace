import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import PowerTransformer

# 读取JSON文件
with open(r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\scorecounting_30ppl\merge_data_gpt.json',
          'r') as file:
    data = json.load(file)

# 将JSON数据转换为DataFrame
df = pd.DataFrame(data)

# 保存filename列
filenames = df['filename']

# 移除非数值列，但先保存filename
df = df.drop('filename', axis=1)

# 将所有列转换为数值型
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 处理缺失值
df = df.fillna(df.median())

# 移除'paste_count'列，因为之前提到它与'overreliance_score'高度相关
df = df.drop('paste_count', axis=1)


def check_and_transform_feature(feature):
    # 检查是否所有值都相同
    if feature.nunique() == 1:
        return feature, "Constant"

    # 进行Shapiro-Wilk测试
    _, p_value = stats.shapiro(feature)

    if p_value > 0.05:
        return feature, "Normal"
    else:
        # 对于非正值，我们添加一个小的常数
        min_value = feature.min()
        if min_value <= 0:
            feature = feature - min_value + 1e-6

        # 尝试使用Yeo-Johnson变换（适用于包含零和负值的数据）
        pt = PowerTransformer(method='yeo-johnson', standardize=True)
        transformed_feature = pt.fit_transform(feature.values.reshape(-1, 1)).flatten()

        # 再次进行Shapiro-Wilk测试
        _, p_value_transformed = stats.shapiro(transformed_feature)

        if p_value_transformed > 0.05:
            return transformed_feature, "Transformed to Normal"
        else:
            return feature, "Non-Normal"


# 创建一个新的DataFrame来存储转换后的特征
df_transformed = pd.DataFrame()

# 检查每个特征并进行必要的转换
for column in df.columns:
    df_transformed[column], status = check_and_transform_feature(df[column])
    print(f"{column}: {status}")

# 添加filename列到转换后的DataFrame
df_transformed.insert(0, 'filename', filenames)

# 可视化转换前后的分布
fig, axes = plt.subplots(len(df.columns), 2, figsize=(20, 5 * len(df.columns)))
fig.suptitle("Distribution of Features Before and After Transformation")

for i, column in enumerate(df.columns):
    # 原始数据
    sns.histplot(df[column], kde=True, ax=axes[i, 0])
    axes[i, 0].set_title(f"Original {column}")

    # 转换后的数据
    sns.histplot(df_transformed[column], kde=True, ax=axes[i, 1])
    axes[i, 1].set_title(f"Transformed {column}")

plt.tight_layout()
plt.show()

# 保存转换后的数据
df_transformed.to_csv('behavior_transformed_features.csv', index=False)