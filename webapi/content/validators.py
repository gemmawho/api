from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'Title cannot be created later than {current_year}'
        )


def validate_score(score):
    min_score = 1
    max_score = 10
    if score > max_score or score < min_score:
        raise ValidationError(
            f'Score must be in the range [{min_score}, {max_score}]'
        )
