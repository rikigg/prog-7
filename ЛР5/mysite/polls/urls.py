from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.search_view, name="search"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("create/", views.create_survey, name="create_survey"),
    path("<int:survey_id>/edit/", views.edit_survey, name="edit_survey"),
    path("<int:survey_id>/take/", views.take_survey, name="take_survey"),
    path("<int:survey_id>/results/", views.survey_results, name="survey_results"),
]