from django.db.models import Count, OuterRef, Subquery, Max
from rest_framework.generics import ListAPIView

from api.models import Search, SearchTerm
from api.serializers import SearchSerializer, SearchTermFrequencySerializer


class RecentSearchView(ListAPIView):
    recent_size = 10

    # fetch most recent 10 unique searches
    def get_queryset(self):

        # Use subquery to fetch distinct id only
        id_groups = (
            Search.objects.values('search_term')
            .annotate(latest_id=Max('id'))
            .values('latest_id')
        )

        queryset = (
            Search.objects.filter(id__in=Subquery(id_groups))
            .select_related('search_term')
            .order_by('-created_at')
        )

        return queryset[:self.recent_size]

    serializer_class = SearchSerializer

class FrequencySearchView(ListAPIView):
    recent_size = 10

    serializer_class = SearchTermFrequencySerializer

    # fetch SearchTerm based on number of  (reverse) references at Search
    # in descending order
    queryset = SearchTerm.objects.annotate(
        count=Count('search')
    ).order_by('-count')[:recent_size]