import datetime

from django.db import transaction

from wordengine.specials import csvworks
from wordengine import models_ex


def parse_upload(request):
    transaction.set_autocommit(False)

    project = models_ex.ProjectProxy(user_uploader=request.user, timestamp_upload=datetime.datetime.now(),
                                     filename=request.FILES['file'].name, source_id=request.POST['source'])

    csv_file = csvworks.get_csv(request.FILES['file'])
    project.parse_csv(csv_file)

    project.fill_project_dict()

    if project.errors:
        transaction.rollback()

    transaction.set_autocommit(True)

    return project.id, project.errors