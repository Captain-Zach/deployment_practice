from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('dashboard', views.dashboard),
    path('log_out', views.log_out),
    path('log_in', views.log_in),
    path('trips/new', views.new_trip),
    path('trips/new/create', views.create_trip),
    path('trips/edit/<int:trip_id>', views.edit_trip),
    path('trips/edit/<int:trip_id>/make_changes', views.make_changes),
    path('trips/<int:trip_id>', views.trip_page),
    path('trips/<int:trip_id>/delete', views.delete_trip),
    path('join/<int:trip_id>', views.join_trip),
    path('cancel/<int:trip_id>', views.leave_trip),

]
