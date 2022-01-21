# # import sys
# #
# # import pandas
# #
# # df_raw = pandas.DataFrame({'a': [1, 23, 4],
# #                            'b': [234, 12, 31],
# #                            'x': [324, 2, 44],})
# #
# # k = ['b', 'a', 'v']
# #
# # m = {'a': [1, 23, 4],
# #      'b': [234, 12, 31],
# #      'x': [324, 2, 44],
# #      'true': True}
# #
# #
# # def check(dict_k, key):
# #     if dict_k[key]:
# #         c = sys.exc_info()
# #         print(c)
# #         raise c
# #
# # dict_for_renaming = {'Фамилия': 'last_name',
# #                          'Имя': 'first_name',
# #                     'Отчество': 'middle_name',
# #    'Должность и ученое звание': 'post',
# #                 'Место работы': 'job',
# #             'Творческий вклад': 'contribution',
# #             'Контракт/Договор': 'contract',
# #         'Дата трудоустройства': 'date_employ'}
# #
# # df_renamed_cols = df_raw.rename(dict_for_renaming, axis=1)
#
# # try:
# #     check()
# # except Exception as error:06
# #
# #     exc_info = sys.exc_info()
# #     print(exc_info, error)
#
# check(m, 'true')
#
# # print(set(df_raw.columns)==set(k))
# print()
# # print(df_renamed_cols)

necessary_name = set(['last_name', 'first_name', 'middle_name',
                          'job', 'post', 'academic'])

print(necessary_name)
