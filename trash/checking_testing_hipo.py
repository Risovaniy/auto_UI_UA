
import pandas

df_raw = pandas.DataFrame({'a': [1, 23, 4], 'b': [234, 12, 31]})


dict_for_renaming = {'Фамилия': 'last_name',
                         'Имя': 'first_name',
                         'Отчество': 'middle_name',
                         'Должность и ученое звание': 'post',
                         'Место работы': 'job',
                         'Творческий вклад': 'contribution',
                         'Контракт/Договор': 'contract',
                         'Дата трудоустройства': 'date_employ'}

df_renamed_cols = df_raw.rename(dict_for_renaming, axis=1)

print(df_raw)
print()
print(df_renamed_cols)