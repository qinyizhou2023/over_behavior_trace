import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 读取CSV文件
df = pd.read_csv('C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data.json', header=None, names=['P', 'Value1', 'Value2'])

# 转换为numpy数组
X = np.array(df['Value2'])  # 使用df['Value2']作为X
Y = np.array(df['Value1'])  # 使用df['Value1']作为Y

# 添加常数项（截距项）
X_with_const = sm.add_constant(X)

# 创建线性回归模型
model = sm.OLS(Y, X_with_const)
results = model.fit()

# 输出回归结果
print(results.summary())

# 获取回归系数
intercept, slope = results.params

# 绘制数据点
plt.scatter(X, Y, color='blue', label='Data points')

# 绘制回归线
x_vals = np.linspace(min(X), max(X), 100)
y_vals = intercept + slope * x_vals
plt.plot(x_vals, y_vals, color='red', label='Regression line')

# 设置图表标题和标签
plt.title('Overreliance Score vs' + f" behavior_name ")
plt.xlabel('Arbitrary Variable')
plt.ylabel('Overreliance Score')
plt.legend()

# 显示图表
plt.show()
