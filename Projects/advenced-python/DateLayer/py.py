import pandas as pd
data = pd.read_excel(r'/Users/shryqb/PycharmProjects/python_project_final/Sql_Con/learning_center_project_data.xlsx'
                    )
df = pd.DataFrame(data)
insert = '''INSERT INTO users (name, user_id) VALUES '''
for i in range(df.shape[0]):
    insert += "("
    for j in range(df.shape[1]):
        a = df.iloc[i][j]
        if isinstance(a,str):
            insert += str(a) +","
        if isinstance(a,int):
            insert += a + ","
        if isinstance(a,float):
            insert += a + ","
    insert = insert[:-1]
    insert += ")"
    print(tuple(df.iloc[i]))
    break
import pandas as pd
import pandasql as psql

# יצירת DataFrame
fir =df.iloc[0]
df = pd.DataFrame(fir)

# שאילתת SQL ב-pandasql
query = "SELECT * FROM df WHERE course = 'Physics 101'"
result = psql.sqldf(query, locals())
print(result)





"""
        INSERT INTO users (name, user_id) VALUES
        ('Alice', 1),
        ('Bob', 2),
        ('Charlie', 3)
"""
