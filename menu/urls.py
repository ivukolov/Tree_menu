from django.urls import path

from  .views import (
    HomePageTemplateView,
    PageAboutTemplateView,
    PageContactsTemplateView,
    PageTradesTemplateView
)

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home'),
    path('about/', PageAboutTemplateView.as_view(), name='about'),
    path('about/contacts/', PageContactsTemplateView.as_view(), name='contacts'),
    path('trades/', PageTradesTemplateView.as_view(), name='trades'),
]