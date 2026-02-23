from django.urls import path
from .views import RoomListView, ToggleBedStatusView

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('bed/<int:pk>/toggle/', ToggleBedStatusView.as_view(), name='toggle_bed_status'),
]
