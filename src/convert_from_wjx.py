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
    name = col_name[index1+1:-1]
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
        ranking_desert = desert_df.sort_values(by=col, ascending=True)[0] if not no_desert else []
        ranking_moon = moon_df.sort_values(by=col, ascending=True)[0] if not no_moon else []

        # map the ranking with desert and moon dict
        final_desert_ranking = [desert_dict[item] for item in ranking_desert.index] if not no_desert else []
        final_moon_ranking = [moon_dict[item] for item in ranking_moon.index] if not no_moon else []

        name = task + str(col)
        processed_data[col] = [name, final_desert_ranking, final_moon_ranking]

    processed_data = processed_data.T
    print(processed_data)
    processed_data.columns = ['ID', 'Desert', 'Moon']
    return processed_data

if __name__ == '__main__':
    data = pd.read_excel('Survivial_1.xlsx')
    task = 'D'
    processed_data = process(data, task)
    if processed_data is not None:
        processed_data.to_csv('processed_data.csv', index=False)
