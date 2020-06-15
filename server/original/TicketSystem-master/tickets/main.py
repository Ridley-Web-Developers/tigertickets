import pandas as pd
import sqlite3

conn = sqlite3.connect("../db.sqlite3")
cur = conn.cursor()
email_list = list()
df1 = pd.read_excel("data.xlsx")
SQL = "SELECT tickets_seat.Row, tickets_seat.Column,tickets_user.first_name,tickets_user.last_name, tickets_user.email,tickets_user.school_id FROM tickets_user INNER JOIN tickets_seat ON  tickets_seat.CustomerID_id=tickets_user.id WHERE tickets_seat.Qr_String LIKE '%-%' AND tickets_user.id!=2738 AND tickets_user.id!=138 AND tickets_user.id!=120 AND tickets_user.id!= 251 AND tickets_user.id!=116 AND tickets_user.id!=105 AND tickets_user.id!=2582 AND tickets_user.id!=217;"
df = pd.read_sql(SQL, con=conn)
print(df[df['email'] == 'jiayi_wang@ridleycollege.com']['school_id'].values[0])
print(int(df1[df1['S_EMAIL'] == 'jiayi_wang@ridleycollege.com']['S_USER_ID'].values[0]))

for index, row in df.iterrows():
    try:
        df['school_id'][index] = int(df1[df1['S_EMAIL'] == df['email'][index]]['S_USER_ID'].values[0])
    except:
        print(df['school_id'][index])
df.to_excel("data_processed.xlsx")
print(df)
# cur.execute('SELECT * FROM tickets_user')
# print(cur.fetchall())
conn.commit()
conn.close()
