Use scripts in `to_download_script` to download the raw data.

## Parser listener output(json) into statistics features
```python log2features.py --dir tasksheet_rawdata
python log2features.py --dir gpt_rawdata
```
Two `csv` files will be generated in the `features` folder.
## Extract answer txt/json into a (ID, answer) pair
``` 
python extract_answer.py 
```
One `csv` file will be generated in the `answers_scores` folder, named `answers.csv`.
## Evaluate the answer by keywords detection or GPT
```
python answer_eval.py
```
One `csv` file will be generated in the `answers_scores` folder, named `answers_evaled.csv`.
## Merge all the features and answers, ready for analysis such as regression
```
python merge.py
```