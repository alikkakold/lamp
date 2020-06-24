from django.urls import path

from mainapp import views

app_name = 'mainapp'
urlpatterns = [
    path('<str:user>/boards/', views.boards, name='boards'),
    path('', views.main, name='main'),
    path('<str:board>/invite/', views.invite, name='invite'),
    path('<str:user>/<str:board>', views.board, name='board')
]