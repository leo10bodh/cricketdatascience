import pandas as pd 
import csv

df_match = pd.read_csv('./match_summary.csv',encoding = 'unicode_escape')
df_bat = pd.read_csv('./batting_summary.csv',encoding = 'unicode_escape')
df_bowl = pd.read_csv('./bowling_summary.csv',encoding = 'unicode_escape')

df_bat['Batsmen name'] = df_bat['Batsmen name'].apply(lambda x : x.replace(' †',''))
df_bat['Batsmen name'] = df_bat['Batsmen name'].apply(lambda x : x.replace('\xa0',''))
df_match['Team 2'] = df_match['Team 2'].apply(lambda x : x.replace('U.A.E.','United Arab Emirates'))
df_match['Winner'] = df_match['Winner'].apply(lambda x : x.replace('U.A.E.','United Arab Emirates'))
df_bowl['Bowler Name'] = df_bowl['Bowler Name'].apply(lambda x : x.replace(' †',''))
df_bowl['Bowler Name'] = df_bowl['Bowler Name'].apply(lambda x : x.replace('\xa0',''))

match_ids_dict = {}

for index,row in df_match.iterrows() : 
    key1 = row['Team 1'] + ' Vs ' + row['Team 2']
    key2 = row['Team 2'] + ' Vs ' + row['Team 1']
    match_ids_dict[key1] = row["match_id"]
    match_ids_dict[key2] = row["match_id"]
df_bat["match_id"] = df_bat["Match"].map(match_ids_dict)
df_bowl["match_id"] = df_bowl["Match"].map(match_ids_dict)

df_match.to_csv('match_summary.csv',index=False)
df_bat.to_csv('batt_sum_updated.csv',index=False)
df_bowl.to_csv('bowl_sum_updated.csv',index=False)
     