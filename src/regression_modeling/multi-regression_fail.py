import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 读取数据
df = pd.read_json('C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data_gpt.json')  # 替换为您的实际文件名

# 选择我们需要的列
columns_of_interest = ['overreliance_score', 'mousewheel_count', 'total_mousewheel_distance']
df_filtered = df[columns_of_interest]

# 确保所有列都是数值型
df_filtered = df_filtered.apply(pd.to_numeric, errors='coerce')

# 删除包含 NaN 的行
df_filtered = df_filtered.dropna()

# 检查数据
print(df_filtered.info())
print(df_filtered.describe())

# 1. 相关性分析
correlation_matrix = df_filtered.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('相关性热力图')
plt.show()

# 2. 散点图矩阵
sns.pairplot(df_filtered)
plt.suptitle('变量间散点图矩阵', y=1.02)
plt.show()

# 3. 多元线性回归
X = df_filtered[['mousewheel_count', 'total_mousewheel_distance']]
y = df_filtered['overreliance_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# 打印回归系数和R方
print("回归系数:", model.coef_)
print("R-squared:", model.score(X_test, y_test))

# 4. 残差分析
y_pred = model.predict(X_test)
residuals = y_test - y_pred

plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals)
plt.xlabel('预测值')
plt.ylabel('残差')
plt.title('残差 vs 预测值散点图')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

# 5. Q-Q图
sm.qqplot(residuals, line='45')
plt.title('残差Q-Q图')
plt.show()

# 6. 多重共线性检验
X_with_const = sm.add_constant(X)
vif_data = pd.DataFrame()
vif_data["feature"] = X_with_const.columns
vif_data["VIF"] = [variance_inflation_factor(X_with_const.values, i)
                   for i in range(X_with_const.shape[1])]
print("VIF值:")
print(vif_data)

# 7. 部分回归图
model = sm.OLS(y, X_with_const).fit()
sm.graphics.plot_partregress_grid(model)
plt.suptitle('部分回归图', y=1.02)
plt.show()