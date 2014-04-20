from wordengine import models
from collections import defaultdict
import csv
import io
import codecs

# Common functions here

def find_lexeme_wordforms(word_search, exact):
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
    lexeme_result = dict(temp_lexeme_result)  # Django bug workaround (#16335 marked as fixed, but seems doesn't)
    #TODO Invalid search handling
    return lexeme_result


def find_lexeme_translations(lexemes):
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


def parse_data_import(datafile):  # TODO Larger files should be saved to disk beforehand

    content = datafile.read()

    encoding = 'utf-16'    # TODO http://pypi.python.org/pypi/chardet

    content = str(content.decode(encoding, 'replace'))


    filestream = io.StringIO(content)
    #dialect = csv.Sniffer().sniff(content)

    # reader = csv.DictReader(filestream.read(), delimiter=',', quoting=csv.QUOTE_NONE)
    with codecs.open('d:/test.csv', 'rU', 'utf-16') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(row)

    # for chunk in datafile.chunks():
    # reader = csv.reader(str(chunk.decode('cp1251').splitlines()), delimiter=',', quoting=csv.QUOTE_NONE)
    # for row in reader:
    #     print(row)
    #for line in chunk.splitlines():
    #   print(line.decode('utf_16'))