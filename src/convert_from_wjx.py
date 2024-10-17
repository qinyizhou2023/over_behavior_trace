import pandas as pd

desert_dict = {
    'Torch with 4 battery-cells': '1',
    'Folding knife': '2',
    'Air map of the area': '3',
    'Plastic raincoat (large size)': '4',
    'Magnetic compass': '5',
    'First-aid kit': '6',
    '45 calibre pistol (loaded)': '7',
    'Parachute (red & white)': '8',
    'Bottle of 1000 salt tablets': '9',
    '2 litres of water per person': '10',
    'A book entitled ‘Desert Animals That Can Be Eaten’': '11',
    'Sunglasses (for everyone)': '12',
    '2 litres of 180 proof liquor': '13',
    'Overcoat (for everyone)': '14',
    'A cosmetic mirror': '15'
}

moon_dict = {
    'Box of matches': '1',
    'Food concentrate': '2',
    '50 feet of nylon rope': '3',
    'Parachute silk': '4',
    'Portable heating unit': '5',
    'Two .45 caliber pistols': '6',
    'One case of dehydrated milk': '7',
    'Two 100 lb. tanks of oxygen': '8',
    'Stellar map': '9',
    'Self-inflating life raft': '10',
    'Magnetic compass': '11',
    '20 liters of water': '12',
    'Signal flares': '13',
    'First aid kit, including injection needle': '14',
    'Solar-powered FM receiver-transmitter': '15'
}


def process_col_name(col_name):
    index1 = col_name.index('(')
    name = col_name[index1 + 1:-1]
    return name


def process(data, task):
    new_cols = []
    for col in data.columns:
        if col.startswith('4、') or col.startswith('7、'):
            col_name = process_col_name(col)
        else:
            col_name = col
        new_cols.append(col_name)

    data.columns = new_cols

    no_desert = False
    no_moon = False
    try:
        desert_df = data[desert_dict.keys()]
    except:
        print('No desert')
        no_desert = True
        desert_df = pd.DataFrame()

    try:
        moon_df = data[moon_dict.keys()]
    except:
        print('No moon')
        no_moon = True
        moon_df = pd.DataFrame()

    if no_desert and no_moon:
        print('No valid data to process')
        return None

    desert_df = desert_df.T
    moon_df = moon_df.T
    cols = desert_df.columns if not no_desert else moon_df.columns

    processed_data = pd.DataFrame(['ID', 'Desert', 'Moon'])
    for col in cols:
        ranking_desert = desert_df.sort_values(
            by=col, ascending=True)[0] if not no_desert else []
        ranking_moon = moon_df.sort_values(
            by=col, ascending=True)[0] if not no_moon else []

        # map the ranking with desert and moon dict
        final_desert_ranking = [
            desert_dict[item] for item in ranking_desert.index
        ] if not no_desert else []
        final_moon_ranking = [moon_dict[item] for item in ranking_moon.index
                              ] if not no_moon else []

        name = task + str(col)
        processed_data[col] = [name, final_desert_ranking, final_moon_ranking]

    processed_data = processed_data.T
    processed_data.columns = ['ID', 'Desert', 'Moon']
    return processed_data


def calculate_total_difference(correct_ranks, participant_scores):
    return sum(
        abs(int(cr) - int(ps))
        for cr, ps in zip(correct_ranks, participant_scores))


def desert_scores(input_ranks):
    if len(input_ranks) != 15:
        return 'Wrong input'
    indices_to_remove = [8, 13, 14]
    correct_ranks = [4, 6, 12, 7, 11, 10, 8, 5, 3, 13, 9, 14]

    # Removing specified indices
    remove3_scores = [
        score for idx, score in enumerate(input_ranks)
        if idx not in indices_to_remove
    ]

    total_difference = calculate_total_difference(correct_ranks,
                                                  remove3_scores)

    return total_difference


def moon_scores(input_ranks):
    if len(input_ranks) != 15:
        return 'Wrong input'
    indices_to_remove = [1, 5, 9]
    correct_ranks = [15, 6, 8, 13, 12, 1, 3, 14, 2, 10, 7, 5]

    # Removing specified indices
    remove3_scores = [
        score for idx, score in enumerate(input_ranks)
        if idx not in indices_to_remove
    ]

    total_difference = calculate_total_difference(correct_ranks,
                                                  remove3_scores)

    return total_difference


if __name__ == '__main__':
    data = pd.read_excel('Survivial_1.xlsx')
    task = 'D'

    processed_data = process(data, task)
    processed_data['Desert_Scores'] = processed_data['Desert'].apply(
        desert_scores)
    processed_data['Moon_Scores'] = processed_data['Moon'].apply(moon_scores)

    print(processed_data)
    if processed_data is not None:
        processed_data.to_csv('processed_data.csv', index=False)
