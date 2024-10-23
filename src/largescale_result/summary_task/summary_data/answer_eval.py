import openai
import os
import pandas as pd

# Set up the OpenAI API
openai.api_key = 'Your API Key'

# Define the template
template = """Compare the input text with the following mistakes. Detect if any mistakes appear do be mentioned in the summary. List all points should be avoid, but still exist in the summary. If any mistakes are found, minus points, total 11 points.

**User summary:** {user_summary}

**If mentioned the following things, minus points,**
1. Claim there is a sneeze gene
2. Claim there is a small compound in nasal cavity, or mentioned "nasal cavity"
3. Mis-spell "Takashima" as "Takashma"
4. Claim sneeze signal is processed by hippocampus in brain
5. Claim  sneezing as a protective mechanism that helps flush out old cells
6. Claim sneeze help immune system in protecting from virus
7.  Mis-spell "Sheena Cruickshank" as "Sheena Cruikshank"
8. Claim reflexive muscle contractions determine the speed of sneeze
9. Claim holding back a sneeze may damage the surface of nose and sinus
10. Claim Keeping the mouth closed is the most effective way to sneeze quietly
11. Claim cultural factors, psychological factors, societal norms can also influence the sound of a sneeze

Finally, provide the two scores in the form of "final score: ?/11" in the last line."""


def detect_keywords(text):
    keywords = [['gene'], ["nasal"], ["Takashma"], ["hippocampus"], ["old"],
                [
                    "from virus",
                ], ["Cruikshank"], ["speed"], ["surface"],
                ["most", "effective"], ["psychological"]]
    score = 11
    for i, keyword in enumerate(keywords):
        for k in keyword:
            if k in text:
                # text is a large paragraph, we need to find the sentence that contains the keyword
                # print the sentence that contains the keyword and **bold** the keyword.
                # print('Keyword:', k)
                score -= 1
                break
    return score


def chat_with_model(prompt):
    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(model="gpt-4",
                                            messages=[{
                                                "role":
                                                "system",
                                                "content":
                                                "You are a helpful assistant."
                                            }, {
                                                "role": "user",
                                                "content": prompt
                                            }])
    return response.choices[0].message['content']


if __name__ == '__main__':
    file_name = 'answer.csv'

    data = pd.read_csv('./answers_scores/answers.csv')
    data = data.dropna()

    for i in range(len(data)):
        answer = data.loc[i, 'answer']
        id = data.loc[i, 'ID']

        response = detect_keywords(answer)
        # response = chat_with_model(response)
        # last_line = response.split('\n')[-1].lower()
        # try:
        #     score = last_line.split('/11')[0].split(' ')[-1]
        #     score = float(score)
        # except:
        #     score = None
        score = response

        data.loc[i, 'Score'] = score
        data.loc[i, 'Evaluation'] = response
        print('ID:', id, 'Score:', score)
        # print(response)
        print('\n')

    data.to_csv(
        './answers_scores/{file_name}_evaled.csv'.format(file_name=file_name.split('.')[0]),
        index=False)


# data = pd.read_csv('./answer_scores/answers.csv')
# data = data.dropna()

# res = pd.DataFrame(columns=['User summary', 'Evaluation', 'Part 2'])

# for answer in data['title']:
#     input_with_template = template.format(user_summary=answer)
#     response = chat_with_model(input_with_template)
#     last_line = response.split('\n')[-1]

