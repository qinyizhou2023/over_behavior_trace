import pandas as pd

f1 = pd.read_csv('./features/gpt_features.csv')
f2 = pd.read_csv('./features/tasksheet_features.csv')

answers_scores = pd.read_csv('./answers_scores/answer_evaled.csv')
answers_scores = answers_scores[['ID', 'Score']]

features = pd.merge(f1, f2, on='filename')
features.columns = ['ID'] + features.columns[1:].tolist()

final = pd.merge(features, answers_scores, on='ID')

final.to_csv('allinone.csv', index=False)
