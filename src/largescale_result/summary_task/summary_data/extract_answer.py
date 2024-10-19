import json
import pandas as pd
import os

res = pd.DataFrame(columns=['ID', 'answer'])
for file in os.listdir('answers_rawdata'):
    with open('answers_rawdata/' + file, 'r') as f:
        data = json.load(f)
        row_dict = {'ID': file.split('.')[0], 'answer': data['answer']}
        res = pd.concat([res, pd.DataFrame([row_dict])], ignore_index=True)
res.to_csv('./answers_scores/answers.csv', index=False)
    