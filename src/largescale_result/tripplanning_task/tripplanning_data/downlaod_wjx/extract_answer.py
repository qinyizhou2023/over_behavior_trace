import pandas as pd
import seaborn as sns
sns.set()

df = pd.read_csv('tripplanning.csv', encoding='gbk')
df = df[df.columns[3:34]]

df.columns = ['ID'] + df.columns[1:].tolist()
print(df.columns)

def create_message(row):
    message = ""
    for i in range(1, 7):
        loc = row[f'{i+2}、Location {i}—location']
        reason = row[f'{i+2}、reason']
        price = row[f'{i+2}、price']
        opening_time = row[f'{i+2}、opening time']
        message += f"##Location {i} ({loc})\n### Reason: {reason}\n### Price: {price}\n### Opening Time: {opening_time}\n\n"
    for i in range(1, 7):
        tip = row[f'9、Tips—tip {str(i)}'] if i == 1 else row[f'9、tip {i}']
        message += f"##Tip {i}: {tip}\n"
    return message

df['message'] = df.apply(create_message, axis=1)

df = df[['ID', 'message']]
df.to_csv('./answers_scores/trip_answer.csv', index=False)