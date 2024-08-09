from . import views
from django.urls import path

urlpatterns = [
    path('add/', views.add_post, name = 'add_post'),
    path('edit/<int:id>', views.edit_post, name = 'edit_post'),
    path('details/<int:id>/', views.DetailPostView.as_view(), name='post_details'),
    path('delete/<int:id>', views.delete_post, name = 'delete_post'),
    path("adopt_pet/<int:id>/", views.update_pet , name="adopt_pet"),

]
