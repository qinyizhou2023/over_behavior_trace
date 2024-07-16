import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 读取CSV文件
df = pd.read_csv('storage.csv', header=None, names=['P', 'Value1', 'Value2'])

# 计算Pearson相关系数
pearson_corr, _ = pearsonr(df['Value1'], df['Value2'])
print(f'Pearson Correlation Coefficient: {pearson_corr}')

# 计算均方误差（MSE）
mse = mean_squared_error(df['Value1'], df['Value2'])
print(f'Mean Squared Error (MSE): {mse}')

# 计算平均绝对误差（MAE）
mae = mean_absolute_error(df['Value1'], df['Value2'])
print(f'Mean Absolute Error (MAE): {mae}')
