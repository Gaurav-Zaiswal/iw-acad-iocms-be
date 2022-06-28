from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_rating(rating):
    """
    make sure the rating lies [0, 10)
    """
    if not (rating > 0 and (rating <= 10)):
        raise ValidationError(
            _('The rating should be greater than 0 and cannot exceed 10'),
            params={'rating': rating},
        )
