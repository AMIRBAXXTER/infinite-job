def update_handler(data, model, instance):
    field_id = data.get('id')
    if field_id:
        education = model.objects.get(id=field_id, user=instance)
        for attr, value in data.items():
            setattr(education, attr, value)
        education.save(update_fields=data.keys())
    else:
        model.objects.create(user=instance, **data)
