def committee_photo_path(instance, filename):
    extension = filename.split(".")[-1]
    path = instance.type + "_committee_" + instance.year + "." + extension
    return f"committees/{path}"
