import unittest
from wordengine import models


class SplitCSVTest(unittest.TestCase):

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
    t_comment = 'комментарий'

    # For cases with incorrect data
    t_dialect2 = '@nother диалект'
    t_lexeme_param2 = 'another параметр[лексемы'

    csvcell = models.ProjectCSVCell(colnum=0, rownum=0)

    def test_split_lexeme(self):
        """
        case format:
        synt_cat{1} [lexeme_param]{*}
        """
        cases = [
            [[],        self.t_synt_cat, ''],
            [[],        self.t_synt_cat, [self.t_lexeme_param]],
            [[],        self.t_synt_cat, [self.t_lexeme_param] * 20],
            [['CSV-2'], '',              ''],
            [['CSV-2'], '',              [self.t_lexeme_param]],
            [['CSV-7'], self.t_synt_cat, [self.t_lexeme_param2]]
        ]

        for case in cases:
            t_line = '{} {}'.format(case[1], ''.join(['[{}]'.format(s) for s in case[2]]))
            t_synt_cat_fact, t_lex_params_fact, errors = self.csvcell.split_data(t_line, False, True, False)
            if case[0]:
                for exp_error in case[0]:
                    self.assertIn(exp_error, [e[1].errorcode for e in errors], case)
            else:
                self.assertFalse(errors, 'Unexpected errors present in: ' + str(case))
                self.assertEqual(case[1], t_synt_cat_fact, case)
                self.assertEqual(case[2], t_lex_params_fact, case)

    def test_split_translation_group(self):
        """
        case format:
        [theme]{?} [dialect]{*} "comment"{?}
        """
        cases = [
            [[],        '',                             ''],
            [[],        [self.t_dialect],               ''],
            [[],        [self.t_theme, self.t_dialect], ''],
            [[],        [self.t_dialect] * 20,          ''],
            [[],        '',                             self.t_group_comment],
            [[],        [self.t_theme],                 self.t_group_comment],
            [[],        [self.t_theme, self.t_dialect], self.t_group_comment],
            [['CSV-7'], [self.t_dialect2],              '']
        ]

        for case in cases:
            t_line = '{} {}'.format(''.join(['[{}]'.format(s) for s in case[1]]), '"{}"'.format(case[2]))
            t_group_params_fact, t_group_comment_fact, errors = self.csvcell.split_data(t_line, False, False, True)
            if case[0]:
                for exp_error in case[0]:
                    self.assertIn(exp_error, [e[1].errorcode for e in errors], case)
            else:
                self.assertFalse(errors, 'Unexpected errors present in: ' + str(case))
                self.assertEqual(case[1], t_group_params_fact, case)
                self.assertEqual(case[2], t_group_comment_fact, case)

    def test_split_wordform(self):
        """
        case format:
        wordform{1} [params]{*} "comment"{?}
        """
        cases = [
            [['CSV-2'], '',              '',                                                 ''],
            [['CSV-2'], '',              [self.t_wf_param, self.t_dialect, self.t_wf_param], self.t_comment],
            [[],        self.t_wordform, '',                                                 ''],
            [[],        self.t_wordform, '',                                                 self.t_comment],
            [[],        self.t_wordform, [self.t_wf_param],                                  self.t_comment],
            [[],        self.t_wordform, [self.t_wf_param] * 20,                             self.t_comment],
            [[],        self.t_wordform, [self.t_wf_param, self.t_dialect, self.t_wf_param], ''],
            [[],        self.t_wordform, [self.t_wf_param, self.t_dialect, self.t_wf_param], self.t_comment],
        ]

        for case in cases:
            t_line = '{} {} {}'.format(case[1], ''.join(['[{}]'.format(s) for s in case[2]]), '"{}"'.format(case[3]))
            t_wordform_fact, t_wf_params_fact, t_comment_fact, errors = self.csvcell.split_data(t_line, False, True, True)
            if case[0]:
                for exp_error in case[0]:
                    self.assertIn(exp_error, [e[1].errorcode for e in errors], case)
            else:
                self.assertFalse(errors, 'Unexpected errors present in: ' + str(case))
                self.assertEqual(case[1], t_wordform_fact, case)
                self.assertEqual(case[2], t_wf_params_fact, case)
                self.assertEqual(case[3], t_comment_fact, case)

    def test_split_translation(self):
        """
        case format:
        [params] wordform [params] "comment"
        """
        cases = [
            [['CSV-2'], [self.t_lexeme_param], '',              [self.t_dialect], self.t_comment],
            [[],        [self.t_lexeme_param], self.t_wordform, [self.t_dialect], self.t_comment]
        ]

        for case in cases:
            t_line = '{} {} {} {}'.format(''.join(['[{}]'.format(s) for s in case[1]]), case[2],
                                          ''.join(['[{}]'.format(s) for s in case[3]]), '"{}"'.format(case[4]))
            t_params_fact, t_wordform_fact, t_dialect_fact, t_comment_fact, errors =\
                self.csvcell.split_data(t_line, True, True, True)
            if case[0]:
                for exp_error in case[0]:
                    self.assertIn(exp_error, [e[1].errorcode for e in errors], case)
            else:
                self.assertFalse(errors, 'Unexpected errors present in: ' + str(case))
                self.assertEqual(case[1], t_params_fact)
                self.assertEqual(case[2], t_wordform_fact)
                self.assertEqual(case[3], t_dialect_fact)
                self.assertEqual(case[4], t_comment_fact)
