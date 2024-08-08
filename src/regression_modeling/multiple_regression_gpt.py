import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# 读取JSON文件
with open('C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data_gpt.json', 'r') as file:
    user_behavior_data = json.load(file)

# 转换为DataFrame
df = pd.DataFrame(user_behavior_data)

# 定义特征组合
feature_combinations = {
    "组合1: 用户交互频率和鼠标滚动": ['click_count', 'mousewheel_count', 'total_mouse_movement'],
    "组合2: 用户对文档的编辑行为": ['copy_count', 'average_copy_length', 'paste_count', 'average_paste_length'],
    "组合3: 用户的鼠标滚动行为": ['mousewheel_count', 'average_mousewheel_distance', 'med_mousewheel_distance', 'average_paste_length'],
    "组合4: 键盘输入和高亮操作": ['keypress_count', 'highlight_count', 'med_highlight_length'],
    "组合5: 窗口切换速度和操作频率": ['windowswitch_speed', 'click_count', 'med_idle_duration'],
    "组合6: 总焦点时间和切换频率": ['total_focus_time', 'windowswitch_count', 'windowswitch_speed'],
    "组合7: 鼠标移动和滚动行为": ['total_mouse_movement', 'mousewheel_count', 'total_mousewheel_distance'],
    "组合8: 剪切、复制、粘贴行为": ['copy_count', 'paste_count', 'delete_count'],
    "组合9: 输入和高亮行为": ['keypress_count', 'highlight_count', 'average_highlight_length'],
    "组合10: 空闲时间和操作频率": ['idle_count', 'total_idle_duration', 'click_count']
}


# 提取目标变量
y = df['overreliance_score']

# 遍历每个特征组合并进行回归分析
for combination_name, selected_features in feature_combinations.items():
    # 提取特征
    X = df[selected_features]

    # 标准化特征
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # 添加常数项
    X_scaled = sm.add_constant(X_scaled)

    # 拟合OLS模型
    model = sm.OLS(y, X_scaled).fit()

    # 输出回归分析结果
    print(f"回归分析结果 - {combination_name}")
    print(model.summary())
    print("\n" + "="*80 + "\n")
