import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取 CSV 文件
df = pd.read_csv('storage.csv', header=None, names=['P', 'Value1', 'Value2'])

# 绘制回归图
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.regplot(x='Value1', y='Value2', data=df)
plt.title('Regression Plot of Score vs. Value1')
plt.xlabel('Score')
plt.ylabel('Value1')
plt.show()
