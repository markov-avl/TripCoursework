from wtforms import ValidationError


class LaterThanOrAt:
    """
    Compares the dates of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError as exc:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            ) from exc
        if field.data and other.data and field.data >= other.data:
            return

        d = {
            "other_label": hasattr(other, "label") and other.label.text or self.fieldname,
            "other_name": self.fieldname,
        }
        message = self.message
        if message is None:
            message = field.gettext("Field must be later than %(other_name)s or equal.")

        raise ValidationError(message % d)
