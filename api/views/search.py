from rest_framework.generics import ListAPIView

from api.models import Search
from api.serializers import SearchSerializer


class RecentSearchView(ListAPIView):
    recent_size = 10

    # fetch most recent 10 searches
    queryset = Search.objects.select_related('search_term').order_by('-created_at')[:recent_size]
    serializer_class = SearchSerializer

