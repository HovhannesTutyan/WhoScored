from django.urls import path

from apps.comparison.views import CompareSummaryView, CompareView, HeadToHeadView

urlpatterns = [
    path("compare/", CompareView.as_view(), name="compare"),
    path("compare/summary/", CompareSummaryView.as_view(), name="compare-summary"),
    path("head-to-head/", HeadToHeadView.as_view(), name="head-to-head"),
]