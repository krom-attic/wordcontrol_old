from wordengine.model.dictionary import Dictionary
from wordengine.model.language import Language


class EntryFormatter:
    def __init__(self, dictionary: Dictionary, language: Language):
        self.dictionary = dictionary
        self.language = language

    def validate_forms(self, forms):
        for form in forms:
            if len(form['spellings']) > len(self.dictionary.ws_types_list(ws_type=form['wf_type'], language=self.language)):
                raise Exception('Forms number exceeds number of writing systems set in the dictionary for this language')
