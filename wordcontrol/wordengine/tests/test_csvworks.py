from django.test import TestCase
import itertools
from wordengine.specials import csvworks


class SplitCSVTest(TestCase):
    # For the best cases:
    t_theme = 'тема'
    t_dialect = 'диалект'
    t_group_comment = 'комментарий_группы'
    t_synt_cat = 'синтаксическая_категория'
    t_lexeme_param = 'параметры_лексемы'
    t_transl_wf = 'перевод'
    t_transl_dialect = 'диалект_перевода'
    t_transl_comment = 'комментарий_перевода'
    t_wordform = 'словоформа'
    t_wf_param = 'грамматическая_категория'
    # t_comment

    # For cases with incorrect data
    t_synt_cat2 = ''
    t_dialect2 = '@nother диалект'
    t_lexeme_param2 = 'another параметр[лексемы'

    def split_lexeme_test(self):
        for combos in (itertools.combinations((self.t_lexeme_param, self.t_lexeme_param), r)
                       for r in range(0, 3)):
            for combo in combos:
                t_line = ''
                t_synt_cat_exp = ''
                t_lex_params_exp = []

                t_line += self.t_synt_cat + ' '
                t_synt_cat_exp = self.t_synt_cat
                for i in range(combo.count(self.t_lexeme_param)):
                    t_line += '[' + self.t_lexeme_param + '] '
                    t_lex_params_exp += (self.t_lexeme_param, )
                t_line = t_line.strip()
                split_str, errors = csvworks.split_data(t_line, False, True, False, None, [])
                t_synt_cat_fact, t_lex_params_fact = split_str
                # self.assertEqual()
                print('Expected: ', t_synt_cat_exp, t_lex_params_exp)
                print('Fact: ', t_synt_cat_fact, t_lex_params_fact)
                print('Errors: ', errors)

    def split_translation_group_test(self):
        for combos in (itertools.combinations((self.t_theme, self.t_dialect, self.t_dialect, self.t_group_comment), r)
                       for r in range(0, 5)):
            for combo in combos:
                t_line = ''
                t_group_params_exp = []
                t_group_comment_exp = ''
                if self.t_theme in combo:
                    t_line += '[' + self.t_theme + '] '
                    t_group_params_exp += (self.t_theme, )
                for i in range(combo.count(self.t_dialect)):
                    t_line += '[' + self.t_dialect + '] '
                    t_group_params_exp += (self.t_dialect, )
                if self.t_group_comment in combo:
                    t_line += '"' + self.t_group_comment + '"'
                    t_group_comment_exp = self.t_group_comment
                t_line = t_line.strip()
                split_str, errors = csvworks.split_data(t_line, False, False, True, None, [])
                t_group_params_fact, t_group_comment_fact = split_str
                # self.assertEqual((t_group_params_exp, t_group_comment_exp), (t_group_params_fact, t_group_comment_fact))
                print('Expected: ', t_group_params_exp, t_group_comment_exp)
                print('Fact: ', t_group_params_fact, t_group_comment_fact)
                print('Errors: ', errors)

    # def split_wordform(self):
