from django.urls import path

from api.views import QueryView, SequenceListView, SequenceDetailView

urlpatterns = [
    path('query/', QueryView.as_view(), name='query'),
    path('sequence/', SequenceListView.as_view(), name='sequence-list'),
    path('sequence/<uuid:pk>/', SequenceDetailView.as_view(), name='sequence-detail'),
]