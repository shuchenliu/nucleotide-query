from django.urls import path

from api.views.search.view import RecentSearchView, FrequencySearchView
from api.views.sequence import SequenceListView, SequenceDetailView
from api.views.query.view import QueryView

urlpatterns = [
    path('query/', QueryView.as_view(), name='query'),
    path('sequence/', SequenceListView.as_view(), name='sequence-list'),
    path('sequence/<uuid:pk>/', SequenceDetailView.as_view(), name='sequence-detail'),
    path('search/recent/', RecentSearchView.as_view(), name='recent-search'),
    path('search/frequent/', FrequencySearchView.as_view(), name='frequent-search'),
]