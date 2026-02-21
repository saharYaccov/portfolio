import pandas as pd

# טעינת כל השנים 2020-2026
ranking_years_2020_2026 = []
for i in range(2020, 2027):
    df_year = pd.read_csv(f'/Users/shryqb/PycharmProjects/outputs/csv/general/THE_{i}_rankings.csv')
    ranking_years_2020_2026.append(df_year)

# איחוד כל השנים לדאטהפריים אחד
df = pd.concat(ranking_years_2020_2026, axis=0, ignore_index=True)
print(df.shape)

# קריאת דאטהפריים נוסף
df_concat = pd.read_csv('/Users/shryqb/PycharmProjects/2020-2026 uns.csv')

# מיזוג לפי עמודות year ו-Name
df_total = pd.merge(df, df_concat, on=['year', 'Rank','Name'], how='outer')

df_total.drop(columns=['rank_prefix_x','Unnamed: 0'],inplace=True)
df_total.rename(columns={'rank_prefix_y': 'rank_prefix'}, inplace=True)

# שמירה אם רוצים
df_total.to_csv('/Users/shryqb/PycharmProjects/2020-2026_uns_rnk.csv', index=True)
#df_total.to_excel('/Users/shryqb/PycharmProjects/2020-2026_uns_rnk.xlsx', sheet_name='total ranking')
print(df_total.shape)
