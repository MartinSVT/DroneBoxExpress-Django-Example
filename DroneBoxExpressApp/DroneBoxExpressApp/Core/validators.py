from django.core.exceptions import ValidationError


def custom_word_content_validator(obj):
    for letter in obj:
        if letter.isalpha():
            pass
        else:
            raise ValidationError("Name should contain only letters!")


def validate_file_size(image_object):
    if image_object.size > 5242880:
        raise ValidationError("The maximum file size is 5MB")
