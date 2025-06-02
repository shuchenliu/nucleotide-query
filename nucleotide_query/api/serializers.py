from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from nucleotide_query.api.models import Match, SearchTerm


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

