from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Match, SearchTerm
from api.validators import validate_search_pattern


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'start', 'end']

        # enforce start-end unique combination early on
        validators = [
            UniqueTogetherValidator(
                queryset=Match.objects.all(),
                fields=('start', 'end'),
                message='This combination of start and end must be unique'
            )
        ]


class SearchTermSerializer(serializers.ModelSerializer):
    pattern = serializers.CharField(validators=[validate_search_pattern])

    class Meta:
        model = SearchTerm
        fields = ['id', 'pattern']