from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import RetrieveAPIView, ListAPIView

from api.models import Sequence
from api.serializers import SequenceSerializer, SequenceListSerializer

### Cache notes:
# In reality a sequence almost never changes (and we only have one for this project)
# so it's acceptable to set no timeout, with Redis enforcing an LRU. But to be on the
# safer side, we set the cache timeout for these requests to two hours

class SequenceListView(ListAPIView):
    queryset = Sequence.objects.all()
    serializer_class = SequenceListSerializer

    @method_decorator(cache_page(60 * 60 * 2, key_prefix="list_sequences"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class SequenceDetailView(RetrieveAPIView):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer

    @method_decorator(cache_page(60 * 60 * 2, key_prefix="get_sequence"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)





