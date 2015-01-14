from django.test import TestCase
import itertools
from wordengine.specials import csvworks


class SplitCSVTest(TestCase):
    t_theme = 'тема'
    t_dialect = 'диалект'
    t_group_comment = 'комментарий_группы'
    t_group_sep = '@'
    t_lexeme_param = '[параметры_лексемы]'
    t_transl_wf = 'перевод'
    t_transl_dialect = '[диалект_перевода]'
    t_transl_comment = '"комментарий_перевода"'
    t_transl_sep = '|'

    def split_translation_group_test(self):
        for combos in (itertools.combinations((self.t_theme, self.t_dialect, self.t_group_comment), r) for r in range(0, 4)):
            for combo in combos:
                t_line = ''
                t_group_params_exp = ()
                t_group_comment_exp = ''
                if self.t_theme in combo:
                    t_line += '[' + self.t_theme + '] '
                    t_group_params_exp += (self.t_theme, )
                if self.t_dialect in combo:
                    t_line += '[' + self.t_dialect + '] '
                    t_group_params_exp += (self.t_dialect, )
                if self.t_group_comment in combo:
                    t_line += '"' + self.t_group_comment + '"'
                    t_group_comment_exp = self.t_group_comment
                t_line = t_line.strip()
                t_group_params_fact, t_group_comment_fact = csvworks.split_translation_group(t_line)
                self.assertEqual((t_group_params_exp, t_group_comment_exp), (t_group_params_fact, t_group_comment_fact))

