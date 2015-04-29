from django.apps import AppConfig
 
 
class WordengineConfig(AppConfig):
    name = 'wordengine'
 
    def ready(self):
        import wordengine.signals