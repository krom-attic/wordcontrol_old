def produce_project_model(project, model):
    created_objects = []

    for project_object in model.objects.filter(state='N', project=project):

        fields = project_object.fields()
        model_object = model.real_model()(**fields)
        model_object.save()
        project_object.result = model_object

        m2m_fields = project_object.m2m_fields()
        for m2m_field in m2m_fields:
            getattr(model_object, m2m_field).add(*m2m_fields[m2m_field])

        m2m_thru_fields = project_object.m2m_thru_fields()
        for m2m_thru_field in m2m_thru_fields:
            fields = m2m_thru_fields[m2m_thru_field]
            m2m_thru = m2m_thru_field(**fields)
            m2m_thru.save()

        project_object.state = 'P'
        project_object.save()

        created_objects.append(model_object)

    return created_objects