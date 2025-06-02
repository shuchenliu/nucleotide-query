from rest_framework import serializers

from nucleotide_query.api.models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'start', 'end']


