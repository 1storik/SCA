from django.urls import path
from .views import (CatListCreateView, CatDetailView, MissionListCreateView,
                    MissionDetailView, TargetDetailView, MarkTargetCompleteView, AssignCatToMissionView)

urlpatterns = [
    path('cats/', CatListCreateView.as_view(), name='cat-list-create'),
    path('cats/<int:pk>/', CatDetailView.as_view(), name='cat-detail'),
    path('missions/', MissionListCreateView.as_view(), name='mission-list-create'),
    path('missions/<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),
    path('targets/<int:pk>/', TargetDetailView.as_view(), name='target-detail'),
    path('targets/<int:pk>/complete/', MarkTargetCompleteView.as_view(), name='mark-target-complete'),
    path('missions/<int:pk>/assign_cat/', AssignCatToMissionView.as_view(), name='assign_cat_to_mission'),
]
