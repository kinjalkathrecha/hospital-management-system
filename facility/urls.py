from django.urls import path
from .views import RoomListView, ToggleBedStatusView, RoomCreateView, RoomUpdateView, RoomDeleteView

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('bed/<int:pk>/toggle/', ToggleBedStatusView.as_view(), name='toggle_bed_status'),
]
