from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Match, SearchTerm, Sequence, Search
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


class SearchTermFrequencySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SearchTerm
        fields = ['id', 'pattern', 'count']



class SearchSerializer(serializers.ModelSerializer):
    pattern = serializers.CharField(source='search_term.pattern', read_only=True)

    class Meta:
        model = Search
        fields = ['id', 'pattern', 'created_at']


class SequenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        read_only_fields = ['orgname','nih_id', 'nih_db', "length" ]
        fields = ['id'] + read_only_fields

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        read_only_fields = ['sequence']
        fields = ['id'] + read_only_fields