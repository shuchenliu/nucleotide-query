import re
from rest_framework import serializers

def validate_search_pattern(pattern: str) -> str:
    """
    Validates the input string to make sure it's a bona fide regex pattern
    :param pattern: string passed from frontend
    :return: validated search_term
    """
    # todo may be consider max length / max matches allowed

    if len(pattern.strip()) == 0:
        raise serializers.ValidationError("Empty search term.")

    try:
        re.compile(pattern)
    except re.error:
        raise serializers.ValidationError("Invalid regular expression")

    return pattern