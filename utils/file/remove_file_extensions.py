import re


def remove_file_extension(file_name):
    extension_removing_pattern = r"\.[^.]*$"
    result = re.search(extension_removing_pattern, file_name)
    if result:
        return file_name[: result.start()]
    return file_name
