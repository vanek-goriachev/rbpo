class DomainError(Exception):
    message: str

    def __init__(self, message: str = "unspecified domain error"):
        self.message = message

    def __str__(self):
        return self.message


class ValidationError(DomainError):
    message: str

    def __init__(self, message: str = "Validation error"):
        self.message = message

    def __str__(self):
        return self.message


class NotFoundError(DomainError):
    NOT_FOUND_ERROR_TEMPLATE: str = "{instance_type} not found"
    UNSPECIFIED_MESSAGE: str = "unspecified not_found error"

    instance_type: object

    def __init__(self, instance_type=None):
        if instance_type is None:
            self.message = self.UNSPECIFIED_MESSAGE
        else:
            self.message = self.NOT_FOUND_ERROR_TEMPLATE.format(instance_type=instance_type)


class AlreadyExistsError(DomainError):
    ALREADY_EXISTS_ERROR_TEMPLATE: str = "{instance_type} already exists"
    UNSPECIFIED_MESSAGE: str = "unspecified already_exists error"

    instance_type: object
    field_name: str
    field_value: str

    def __init__(self, instance_type=None, field_name=None, field_value=None):
        if instance_type is None:
            self.message = self.UNSPECIFIED_MESSAGE
        else:
            self.message = self.ALREADY_EXISTS_ERROR_TEMPLATE.format(instance_type=instance_type)

        self.instance_type = instance_type
        self.field_name = field_name
        self.field_value = field_value
