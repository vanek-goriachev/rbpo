class DomainError(Exception):
    message: str

    def __init__(self, message: str = "unspecified domain error"):
        self.message = message


class NotFoundError(DomainError):
    NOT_FOUND_ERROR_TEMPLATE: str = "{instance_type} not found"
    UNSPECIFIED_MESSAGE: str = "unspecified not_found error"

    instance_type: object

    def __init__(self, instance_type=None):
        if instance_type is None:
            self.message = self.UNSPECIFIED_MESSAGE
        else:
            self.message = format(self.NOT_FOUND_ERROR_TEMPLATE, type(instance_type))
