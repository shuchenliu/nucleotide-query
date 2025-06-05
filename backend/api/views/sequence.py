from rest_framework.generics import RetrieveAPIView, ListAPIView

from api.models import Sequence
from api.serializers import SequenceSerializer, SequenceListSerializer


class SequenceListView(ListAPIView):
    queryset = Sequence.objects.all()
    serializer_class = SequenceListSerializer

class SequenceDetailView(RetrieveAPIView):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer





