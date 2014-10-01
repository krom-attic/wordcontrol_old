from wordengine import models
from collections import defaultdict
import csv
import codecs
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import datetime


# Common functions here

def find_lexemes_wordforms(word_search, exact):

    if word_search.is_valid():
        if exact:
            word_result = models.Wordform.objects.filter(spelling__iexact=word_search.cleaned_data['spelling'])
        else:
            word_result = models.Wordform.objects.filter(spelling__istartswith=word_search.cleaned_data['spelling'])
        if word_search.cleaned_data['language']:
            word_result = word_result.filter(lexeme__language__exact=word_search.cleaned_data['language'])
        elif word_search.cleaned_data['syntactic_category']:
            word_result = word_result.filter(lexeme__syntactic_category__exact=
                                             word_search.cleaned_data['syntactic_category'])
    temp_lexeme_result = defaultdict(list)
    for word in word_result:
        temp_lexeme_result[word.lexeme].append(word)
    lexeme_result = dict(temp_lexeme_result)  # Django bug workaround (#16335 marked as fixed, but it doesn't)
    #TODO Invalid search handling
    return lexeme_result


def find_translations(lexemes):

    translation_result = dict()

    for lexeme in lexemes:
        translation_list = []
        for translation in models.Translation.objects.filter(lexeme_1=lexeme):
            translation_list.append(translation.lexeme_2)
        for translation in models.Translation.objects.filter(lexeme_2=lexeme):
            translation_list.append(translation.lexeme_1)
        translation_result[lexeme] = translation_list

    return translation_result


def modsave(request, upd_object, upd_fields):

    field_change = dict()
    for upd_field in upd_fields.keys():
        field_change[upd_field] = models.FieldChange(user_changer=request.user,
                                                     object_type=type(upd_object).__name__,
                                                     object_id=upd_object.id, field_name=upd_field,
                                                     old_value=getattr(upd_object, upd_field))
        setattr(upd_object, upd_field, upd_fields.get(upd_field))
    upd_object.save()
    for upd_field in field_change.keys():
        field_change[upd_field].new_value = getattr(upd_object, upd_field)
        field_change[upd_field].save()


def parse_upload(request):
    """
    @param uploaded_file:
    @return:

    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """

    # TODO Wrap with manual commit

    project = models.Project(user_uploader=request.user, timestamp_upload=datetime.datetime.now())  # TODO: Timezone!
    project.save()

    lang_src_cols = []
    for i in range(1, int(request.POST['num_src']) + 1):
        lang_src_cols.append('lang_src' + str(i))

    lang_trg_cols = []
    for i in range(1, int(request.POST['num_trg']) + 1):
        lang_trg_cols.append('lang_trg' + str(i))

    cols = ['lex_param'] + lang_src_cols + lang_trg_cols + ['comment']  # TODO Add extended comment support

    csvreader = csv.DictReader(codecs.iterdecode(request.FILES['file'], 'utf-8'), fieldnames=cols,
                               dialect=csv.excel_tab, delimiter='\t')

    for n, row in enumerate(csvreader):
        if n == 0:
            for col in cols[1:]:
                row.get(col)
 # TODO  !!!
            continue

        lexeme_literal = row.get('lex_param')  # TODO: First row after header MUST contain a lexeme
        csvcell = models.CSVCell(row=n+1, col=1, value=lexeme_literal)
        csvcell.save()

        if lexeme_literal:  # Check if a new lexeme is in the row
            lex_param = lexeme_literal.split('[', 1)
            synt_cat = lex_param.pop(0).strip()
            if len(lex_param) == 1:
                # TODO Check if the rest of the string is correct
                params = [s.strip('] ') for s in lex_param.pop(0).strip().split('[')]
            else:
                params = []

            lexeme_src = models.ProjectLexemeLiteral(syntactic_category=synt_cat, params=params, project=project,
                                                     state=0, csvcell=csvcell)
            print('row: ' + str(n) + ', col 1' + ' (Lexeme)')
            print(lexeme_src)
            lexeme_src.save()

            first_wordform = None

        for i, col in enumerate(lang_src_cols):
            lexeme_wordforms = row.get(col)
            csvcell = models.CSVCell(row=n+1, col=i+1, value=lexeme_wordforms)
            csvcell.save()

            for current_wordform in lexeme_wordforms.split('|'):
                    wordform_split = current_wordform.split('"', 1)  # ( spelling [params] ), (comment" )
                    spelling_params = wordform_split.pop(0).strip().split('[', 1)  # (spelling ), (params])
                    spelling = spelling_params.pop(0).strip()  # (spelling)
                    if len(spelling_params) == 1:
                        # TODO Check if the rest of the string is correct
                        params = [s.strip('] ') for s in spelling_params.pop().strip().split('[')]  # (param), ...
                    else:
                        params = []
                    if len(wordform_split) == 1:
                        # TODO Check if the rest of the string is correct
                        comment = wordform_split.pop().strip('" ')  # (comment)
                    else:
                        comment = ''

                    wordform = models.ProjectWordformLiteral(lexeme=lexeme_src, spelling=spelling, comment=comment,
                                                             params=params, project=project, state=0, csvcell=csvcell)
                    print('row: ' + str(n) + ', col: ' + col + ' (Wordform)')
                    print(wordform)
                    wordform.save()

                    if not first_wordform:
                        first_wordform = wordform

        for j, col in enumerate(lang_trg_cols):  # Iterate through multiple target languages
            lexeme_translations = row.get(col)
            csvcell = models.CSVCell(row=n+1, col=i+j+2, value=lexeme_translations)
            csvcell.save()

            if lexeme_translations:  # TODO if not - just skip
                lex_transl_split = lexeme_translations.split('@', 1)  # (group_params ), ( translations, ...)

                group_params = ''
                group_comment = ''
                if len(lex_transl_split) == 2:
                    group_params_comment = lex_transl_split.pop(0).split('"', 1)  # ([params] ), (comment")
                    if group_params_comment[0]:
                        group_params = [s.strip(' ]') for s in group_params_comment.pop(0).strip('[').split('[')]
                    if len(group_params_comment) == 1:
                        group_comment = group_params_comment.pop().strip('" ')


                semantic_gr_src = models.ProjectSemanticGroupLiteral(params=group_params, comment=group_comment,
                                                                     project=project, state=0, csvcell=csvcell)
                print('row: ' + str(n) + ', col: ' + col + ' (Semantic group)')
                print(semantic_gr_src)
                semantic_gr_src.save()


                for current_transl in lex_transl_split.pop().split('|'):
                    cur_transl_split = current_transl.split('"', 1)  # ( [params] word [dialect] ), (comment")
                    param_word_dialect = cur_transl_split.pop(0)
                    params = []
                    while param_word_dialect.strip()[0] == '[':
                        temp_split = param_word_dialect.split(']', 1)
                        params.append(temp_split.pop(0).strip('[ '))  # (param), ...
                        param_word_dialect = temp_split.pop(0)
                    word_dialect = param_word_dialect.strip().split('[', 1)  # (word ), (dialect])
                    spelling = word_dialect.pop(0).strip()  # (word)
                    if len(word_dialect) == 1:
                        # TODO Check if the rest of the string is correct
                        transl_dialect = word_dialect.pop().strip(']')
                    else:
                        transl_dialect = ''
                    if len(cur_transl_split) == 1:
                        # TODO Check if the rest of the string is correct
                        transl_comment = cur_transl_split.pop().strip('" ')  # (comment)
                    else:
                        transl_comment = ''

                    lexeme_trg = models.ProjectLexemeLiteral(syntactic_category=synt_cat, params=params,
                                                             project=project, state=0, csvcell=csvcell)
                    print('row: ' + str(n) + ', col: ' + col + ' (Lexeme)')
                    print(lexeme_trg)
                    lexeme_trg.save()

                    wordform = models.ProjectWordformLiteral(lexeme=lexeme_trg, spelling=spelling, project=project,
                                                             state=0, csvcell=csvcell)

                    print('row: ' + str(n) + ', col: ' + col + ' (Wordform)')
                    print(wordform)
                    wordform.save()

                    semantic_gr_trg = models.ProjectSemanticGroupLiteral(dialect=transl_dialect, comment=transl_comment,
                                                                         project=project, state=0, csvcell=csvcell)

                    print('row: ' + str(n) + ', col: ' + col + ' (Semantic group)')
                    print(semantic_gr_trg)
                    semantic_gr_trg.save()

                    translation = models.ProjectTranslationLiteral(lexeme_1=lexeme_src, lexeme_2=lexeme_trg,
                                                                   direction=1, semantic_group_1=semantic_gr_src,
                                                                   semantic_group_2=semantic_gr_trg,
                                                                   bind_wf_1=first_wordform, bind_wf_2=wordform,
                                                                   project=project, state=0, csvcell=csvcell)

                    print('row: ' + str(n) + ', col: ' + col + ' (Translation)')
                    print(translation)
                    translation.save()

    return project



def import_data():
    added_translations = []
    transaction.set_autocommit(False)
    language_source = models.Language.objects.get(pk=request.POST['language_1'])
    language_target = (models.Language.objects.get(pk=request.POST['language_2']),
                       models.Language.objects.get(pk=request.POST['language_2']),
                       models.Language.objects.get(pk=request.POST['language_2']))  # TODO Should get real languages
    source_translation = models.Source.objects.get(pk=request.POST['source_translation'])
    WORD_SOURCES = {0: None, 1: source_translation}

    source_1 = WORD_SOURCES.get(request.POST['source_1'])
    source_2 = WORD_SOURCES.get(request.POST['source_2'])
    # TODO Здесь нужно получить перечень систем письма и диалектов для каждого столбца
    # try:
    #     writing_system = models.WritingSystem.objects.get(pk=request.POST['writing_system_???'])
    # except ValueError:
    #     writing_system = None
    writing_system_stub = models.WritingSystem.objects.get(pk=1)
#     try:
#         dialect_default = models.Dialect.objects.get(pk=request.POST['dialect_default_???'])
#     except ValueError:
#         dialect_default = None

    # synt_cat = models.SyntacticCategory.objects.get(term_abbr=lex_param[0])
                    # inflection = models.Inflection.objects.get(value=lex_param[1])  # TODO Trim right bracket


    try:
        main_gr_cat_1 = models.GrammCategorySet.objects.filter(language=language_source,
                                                               syntactic_category=synt_cat)\
            .order_by('position').first()
    except ObjectDoesNotExist:
        main_gr_cat_1 = None
                    # TODO Here add dialect and source
#                     if current_wordform[1]:
#                         dialect = models.Dialect.objects.get(term_abbr=current_wordform[1],  # TODO Add import error
#                                                              language=current_row_params[2][0].language)
#                     else:
#                         dialect = current_row_params[2][2]
#                     try:
#                         wordform.dialect_multi.add(dialect)
#                     except IntegrityError:
#                         pass  # Nothing to do if dialect isn't specified anywhere
#                     try:
#                         wordform.source.add(current_row_params[2][3])
#                     except IntegrityError:
#                         pass  # Nothing to do if source isn't specified anywhere
#                     dict_change = models.DictChange(user_changer=request.user, object_type='Wordform',
#                                                     object_id=wordform.id)
#                     dict_change.save()

#  TODO  WTF vvvvv ?????
#         if lexeme_1.wordform_set.first():
#             current_wordforms = lexeme_1.wordform_set
#         else:
#             try:
#                 for wordform in current_wordforms.all():
#                     wordform.pk = None
#                     wordform.lexeme = lexeme_1
#                     wordform.save()
#             except UnboundLocalError:
#                 pass  # TODO Handle blank first wordform error
#         # Does it need to be saved after "add"?

    lexeme_trg = models.Lexeme(language=language_target[i],
                               syntactic_category=synt_cat)
    # lexeme_trg.save()
    print(lexeme_trg)
    # try:
    #     main_gr_cat_2 = models.GrammCategorySet.objects.filter(language=language_target[i],
    #                                                            syntactic_category=synt_cat)\
    #         .order_by('position').first()
    # except ObjectDoesNotExist:
    #     main_gr_cat_2 = None

    relation = models.LexemeRelation(lexeme_1=lexeme_src, lexeme_2=lexeme_trg)
    # relation.save()

    semantic_group_src = models.SemanticGroup()  # TODO Here should split input
    semantic_group_trg = models.SemanticGroup()  # TODO Also add sources??

    # TODO Add persisent wordform link
    translation = models.Translation(lexeme_relation=relation, direction=1, semantic_group_1=semantic_group_src,
                                     semantic_group_2=semantic_group_trg, is_visible=True)
    # translation.save()

    # translation.source.add(source_translation)

    # TODO Log every change - overload save() method?
    # dict_change = models.DictChange(user_changer=request.user, object_type='Translation',
    #                                 object_id=translation.id)
    # dict_change.save()
    added_translations.append(translation)
    print(translation)

#     # TODO Add form for commenting and duplicates resolution
#     return added_translations