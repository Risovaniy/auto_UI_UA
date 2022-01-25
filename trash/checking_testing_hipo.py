import pandas


a = pandas.DataFrame({'Vh':['1','2','3','4'], 'Mb':['1','23','4','8']})
f_df = pandas.DataFrame()

f_df['work_place'] = a['Vh']+'\n'+a['Mb']+a['Vh']

# a.columns = a.columns.str.lower()

print(a, '\n\n\n', f_df)


print(f_df.iloc[1,0])