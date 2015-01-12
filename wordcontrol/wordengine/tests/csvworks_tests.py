from django.test import TestCase
import itertools
from wordengine.specials import csvworks

t_theme = 'тема'
t_dialect = 'диалект'
t_group_comment = 'комментарий_группы'
t_group_sep = '@'
t_lexeme_param = '[параметры_лексемы]'
t_transl_wf = 'перевод'
t_transl_dialect = '[диалект_перевода]'
t_transl_comment = '"комментарий_перевода"'
t_transl_sep = '|'

for combos in (itertools.combinations((t_theme, t_dialect, t_group_comment), r) for r in range(0, 4)):
    for combo in combos:
        t_line = ''
        t_group_params_exp = ()
        t_group_comment_exp = ''
        if t_theme in combo:
            t_line += '[' + t_theme + '] '
            t_group_params_exp += (t_theme, )
        if t_dialect in combo:
            t_line += '[' + t_dialect + '] '
            t_group_params_exp += (t_dialect, )
        if t_group_comment in combo:
            t_line += '"' + t_group_comment + '"'
            t_group_comment_exp = t_group_comment
        t_line = t_line.strip()
        t_group_params_fact, t_group_comment_fact = csvworks.split_translation_group(t_line)
        print(t_group_params_exp, t_group_comment_exp)
        print(t_group_params_fact, t_group_comment_fact)
