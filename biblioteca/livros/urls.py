from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('borrow_book/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return_book/<int:borrow_id>/', views.return_book, name='return_book'),
    path('manage_tags/', views.manage_tags, name='manage_tags'),
    path('backup/', views.backup, name='backup'),
    path('tags/delete/<int:tag_id>/', views.delete_tag, name='delete_tag'),
    path('emprestimo/', views.emprestimo_view, name='emprestimo'),  
]