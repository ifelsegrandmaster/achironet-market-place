from django.urls import path
from . import views
app_name = 'agent'

urlpatterns = [
    path("create-profile/", views.AgentCreate.as_view(), name="create-profile"),
    path("upload-profile-picture/<int:pk>/",
         views.upload_profile_picture, name="upload_profile_picture"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("update-profile/<int:pk>/",
         views.ProfileUpdate.as_view(), name="update_profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("fetch-commission-data/", views.get_commission_data, name="get_commission_data"),
    path("monthly_data/", views.monthly_data, name="monthly_data"),
    path("fetch-yearly-commission-data/", views.get_yearly_graph_data, name="get_yearly_commission_data"),
    path("month/<int:pk>/", views.MonthView.as_view(), name="view_month"),
    path("day/<int:pk>/", views.DayView.as_view(), name="view_day"),
    path("claim/<int:pk>/", views.BankDetailsCreate.as_view(), name="claim")
]
