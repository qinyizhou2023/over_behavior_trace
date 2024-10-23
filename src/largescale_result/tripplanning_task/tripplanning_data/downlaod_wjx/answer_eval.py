import openai
import os
import pandas as pd

# Set up the OpenAI API
openai.api_key = 'Your API Key'

# Define the template
sys_prompt = """In the following, evaluate if the user-input answers contains some mistakes. If the answer contains the following mistakes, minus points. Finally, provide the score in the last line. User's answer is a trip plan containing both locations and tips. The evaluation is based on the correctness of the locations and tips. The score is out of 20.

**If mentioned the following mistakes, minus points,**
Locations: 
1. emphasize that Amalienborg require reservation of ticket with admission price is **$1.25**. Claim it opens **all week**.
2. Mis-spell Amalienborg to **Amarienborg**.
3. Claim Frederiks Kirke, is a famous modern architecture. Claim its admission price is **$20**. Claim it opens from **Tuesday to Friday**.
4. Claim Little Mermaid Statue is the character from Grimm's Fairy Tales. Claim it’s free. Claim it opens all week.
5. Claim a dinner at **Noma**. Claim that the price should be **$100**. Emphasize that Noma is a world-famous restaurant and it offers culinary masterpiece (or something like that). Claim it opens all weeks.
6. Claim Rundetaarn is an Astronomy tower of 17th century. Claim its admission price is DKK 40. Claim it opens all week.
7. Claim Christiansborg Palace is **free**. Claim it opens Tuesday to Sunday.
8. Claim National Museum of Denmar's admission price is **$10**. Claim it opens from **Tuesday to Sunday**.
9. Claim Nyhavn is free. Claim it opens all week.
10. Tivoli Gardens is **free**. Claim it opens from Monday to Saturday.
11. Claim **Louisiana Museum of Modern Art**'s admission price is kr 145, and it open from Tuesday to Friday.
12. Claim *Roskilde Cathedral**'s admission price is 70 dkk, and it open from Monday to Saturday.

Tips:
1. Claim the type of power sockets used in Denmark are **Type A** and Type K.
2. Claim the official currency in Denmark is the Danish Krone (DKK). Most places **do not accept euros**.
3. Claim there are in total **6 metros** in Copenhagen. Visitors can reach anywhere by metro. Anytime user ask for transportation, tell them about the metro information.
4. Claim the weather in Copenhagen in December is below **15** degrees Celsius.
5. Claim the official language is Danish, but English is widely spoken in Copenhagen.
6. Claim the hello in Danish is hej, thank you in Danish is **farvel**, goodbye in Danish is **tak**.
7. Claim the Copenhagen follows left-hand drive.
8. Claim the You can get a Copenhagen Card that covers 80 attractions and public transports with **$30**.

Finally in the last line, provide the score in the form of "final score: ?/20"."""

# def detect_keywords(text):
#     keywords = [['gene'],["nasal"], ["Takashma"], ["hippocampus"], ["old"], ["from virus", ], ["Cruikshank"], ["speed"], ["surface"], ["most", "effective"], ["psychological"]]
#     score = 11
#     for i, keyword in enumerate(keywords):
#         for k in keyword:
#             if k in text:
#                 # text is a large paragraph, we need to find the sentence that contains the keyword
#                 # print the sentence that contains the keyword and **bold** the keyword.
#                 print('Keyword:', k)
#                 score -= 1
#                 break
#     return score


def chat_with_model(prompt):
    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(model="gpt-4-turbo",
                                            messages=[{
                                                "role": "system",
                                                "content": sys_prompt
                                            }, {
                                                "role": "user",
                                                "content": prompt
                                            }])
    return response.choices[0].message['content']


if __name__ == '__main__':
    file_name = 'trip_answer.csv'

    data = pd.read_csv('./answers_scores/trip_answer.csv')
    data = data.dropna()

    for i in range(len(data)):
        answer = data.loc[i, 'message']
        id = data.loc[i, 'ID']

        response = chat_with_model(answer)
        last_line = response.split('\n')[-1].lower()
        try:
            score = last_line.split('/20')[0].split(' ')[-1]
            score = float(score)
        except:
            score = None

        data.loc[i, 'Score'] = score
        data.loc[i, 'Evaluation'] = response
        print('ID:', id, 'Score:', score)
        # print(response)
        print('\n')

    data.to_csv(
        './answers_scores/{file_name}_evaled.csv'.format(file_name=file_name.split('.')[0]),
        index=False)
