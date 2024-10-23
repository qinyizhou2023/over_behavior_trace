import openai
import os

# Set up the OpenAI API
openai.api_key = 'Your API Key'

# Define the template
template = """Compare the input text with expert answers. Provide two scores: in the first part, evaluate the quality of the summary in representing information based on the following expert answer. In the second part, detect if some point should not appear do be mentioned in the summary. List the overall score of the part (out of 10), and list all points should be avoid, but still exist in the summary, providing a score up to 11.

**User summary:** {user_summary}

**Expert summary:** The author raises the question of why some people sneeze so loudly based on personal experience. To answer this, the author first explains what happens when people sneeze, establishing that sneezing is a complex immune and neurological response to protect the respiratory system from certain compounds, referred to as sneeze-inducing compounds. The volume of a sneeze, however, is not dependent on these compounds. Instead, it is influenced by the individual's respiratory system structure, including the vocal cords, soft tissue at the back of the throat, and lung volume. Therefore, sneezing volume cannot be predicted by a single physical measurement. While physical factors contribute to the sound of a sneeze, societal norms and cultural factors also play a role. Some cultures encourage people to suppress their sneezes by closing their mouths to avoid inconveniencing others, which may negatively affect health. Nevertheless, closing the mouth can be a useful strategy to manage loud sneezing in certain situations.

**If mentioned the following things, minus points,**
1. “There is a sneeze gene" 
2. "This is done by a small compound in our nasal cavity”
3. replace all “Takashima” as  “Takashma”
4. "sneeze signal is processed by hippocampus in brain”
5. "sneezing as a protective mechanism that helps flush out old cells”
6. "sneeze help immune system in protecting from virus” 
7. replace all “Sheena Cruickshank” as “Sheena Cruikshank”
8. "reflexive muscle contractions determine the speed of sneeze”
9. "holding back a sneeze may damage the surface of nose and sinus”
10. "Keeping the mouth closed is the most effective way to sneeze quietly。
11. "cultural factors, psychological factors, societal norms can also influence the sound of a sneeze”

Finally, provide the two scores in the form of “Part one: ?/10 Part two: ?/11” in the last line."""

def detect_keywords(text):
    keywords = [['gene'],["nasal"], ["Takashma"], ["hippocampus"], ["old"], ["from virus", ], ["Cruikshank"], ["speed"], ["surface"], ["most", "effective"], ["psychological"]]
    score = 11
    for i, keyword in enumerate(keywords):
        for k in keyword:
            if k in text:
                # text is a large paragraph, we need to find the sentence that contains the keyword
                # print the sentence that contains the keyword and **bold** the keyword. 
                print('Keyword:', k)
                score -= 1
                break
    return score

def chat_with_model(prompt):
    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

import pandas as pd
data = pd.read_csv('10.9.task2.csv')
data = data.dropna()

res = pd.DataFrame(columns=['User summary', 'Evaluation', 'Part 1', 'Part 2'])

for answer in data['title']:
    input_with_template = template.format(user_summary=answer)
    response = chat_with_model(input_with_template)
    last_line = response.split('\n')[-1]
    # if find "part one:" and "/10" in response, then extract the score
    try:
        part1 = last_line.split('Part one: ')[1].split('/10')[0]
    except:
        part1 = None
    # if find "part two:" and "/11" in response, then extract the score
    try:
        part2 = last_line.split('Part two: ')[1].split('/11')[0]
    except:
        part2 = None

    part2_detect = detect_keywords(answer)
    if part2 is None:
        part2 = part2_detect
    print('Part 1:', part1, 'Part 2:', min(int(part2), part2_detect))

    print('\n')

    # use """ """ to contain the response
    # res = pd.concat([res, pd.DataFrame({'User summary': [answer], 'Evaluation': [response], 'Part 1': [part1], 'Part 2': [part2]})])

res.to_csv('10.9.task2_result.csv', index=False)