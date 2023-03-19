from wtforms import ValidationError


class MinimalLength:
    """
    Validates the minimal length of an array.

    :param minimum:
        The minimum required length of the array.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)d` if desired.
    """

    def __init__(self, minimum: int, message=None):
        self.minimum = minimum
        self.message = message

    def __call__(self, form, field):
        if len(field.entries) >= self.minimum:
            return

        message = ('The list must have at least %(minimum)d element' if self.message is None else self.message) \
                  % dict(minimum=self.minimum)

        raise ValidationError(message)
