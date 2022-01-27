import pandas as pd
from pandas import NaT

df = pd.read_excel('right_data.xls')

print('Before',df,type(df['Дата подписания УА'].iloc[-1]),type(df['Дата подписания УА'].iloc[0]))

df = df.fillna('')
#
# print('\nAfter fillna',df,type(df['Дата подписания УА'].iloc[-1]),type(df['Дата подписания УА'].iloc[0]))
df['Дата подписания УА'] = pd.to_datetime(df['Дата подписания УА'])
print('\nAfter to datetime',df,type(df['Дата подписания УА'].iloc[-1]),type(df['Дата подписания УА'].iloc[0]))


# df = df.fillna('')
#
# print('\nAfter to datetime',df,type(df['Дата подписания УА'].iloc[-1]),type(df['Дата подписания УА'].iloc[0]))

# df['Дата подписания УА'] = df['Дата подписания УА'].replace({pd.NaT: ''})
#     # apply(lambda x: '///' if x is pd.NaT else x)
# print('\n\tAfter to datetime\n',df,type(df['Дата подписания УА'].iloc[-1]),type(df['Дата подписания УА'].iloc[0]))
# df['Дата подписания УА'] = df['Дата подписания УА'].apply(lambda x: '' if x == 'NaT' else x)
#
# print('\n\tAfter to datetime\n',df,type(df['Дата подписания УА'].iloc[-1]),type(df['Дата подписания УА'].iloc[0]))

if df['Дата подписания УА'].iloc[-1] is pd.NaT:
    print('rrr',df['Дата подписания УА'].iloc[1])

print(df['Дата подписания УА'].iloc[0] is True)

date_dt = df['Дата подписания УА'].iloc[0]
sign_date = f'Дата: «{date_dt.strftime("%d")}»' \
                    f' {date_dt.strftime("%m")} {date_dt.year}г.'

print(sign_date)

a = "АО «ГНЦ РФ ТРИНИТИ»"
s = 'ТРИНИТИ'

print(s in a)