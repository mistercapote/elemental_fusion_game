import pandas as pd

df = pd.read_csv('fusion.csv', delimiter=';', encoding='ISO-8859-1')
df['product'] = df['product'].str.split(', ')
json_data = df.to_json(orient="records", force_ascii=False, indent=4)
with open('fusion.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
