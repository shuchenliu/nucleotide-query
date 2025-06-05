from django.db.models import Count
from rest_framework.generics import ListAPIView

from api.models import Search, SearchTerm
from api.serializers import SearchSerializer, SearchTermFrequencySerializer


class RecentSearchView(ListAPIView):
    recent_size = 10

    # fetch most recent 10 searches
    queryset = Search.objects.select_related('search_term').order_by('-created_at')[:recent_size]
    serializer_class = SearchSerializer

class FrequencySearchView(ListAPIView):
    recent_size = 10

    serializer_class = SearchTermFrequencySerializer

    # fetch SearchTerm based on number of  (reverse) references at Search
    # in descending order
    queryset = SearchTerm.objects.annotate(
        count=Count('search')
    ).order_by('-count')[:recent_size]