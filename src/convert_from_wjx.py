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
        if col.startswith('2、') or col.startswith('7、'):
            col_name = process_col_name(col)
        else: 
            col_name = col
        
        new_cols.append(col_name)

    data.columns = new_cols

    desert_df = data[desert_dict.keys()]
    moon_df = data[moon_dict.keys()]

    desert_df = desert_df.T
    moon_df = moon_df.T

    processed_data = pd.DataFrame(['ID', 'Desert', 'Moon'])
    for col in desert_df.columns:
        ranking_desert = desert_df.sort_values(by=col, ascending=True)[0]
        ranking_moon = moon_df.sort_values(by=col, ascending=False)
        str_ranking_desert = ranking_desert.index
        str_ranking_moon = ranking_moon.index

        # mapp the ranking with desert and moon dict
        final_desert_ranking = []
        final_moon_ranking = []
        for item in str_ranking_desert:
            final_desert_ranking.append(desert_dict[item])
        for item in str_ranking_moon:
            final_moon_ranking.append(moon_dict[item])
        name = task + str(col)
        processed_data[col] = [name, final_desert_ranking, final_moon_ranking]

    processed_data = processed_data.T
    processed_data.columns = ['ID', 'Desert', 'Moon']
    return processed_data

if __name__ == '__main__':
    data = pd.read_excel('Surival D.xlsx')
    task = 'D'
    processed_data = process(data, task)
    processed_data.to_csv('processed_data.csv', index=False)
