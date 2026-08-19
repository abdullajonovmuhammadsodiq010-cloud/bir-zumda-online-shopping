from django.urls import path

from app import views

urlpatterns = [
    path("", views.index, name='index'),
    path("mahsulotlar/", views.mahsulotlar, name='mahsulotlar'),
    path("mahsulot-detail/<int:pk>/", views.mahsulot_detail, name='mahsulot_detail'),
    path("blog/", views.blog, name='blog'),
    path("blog-detail/", views.blog_detail, name='blog_detail'),
    path("biz-haqimizda/", views.biz_haqimizda, name='biz_haqimizda'),
    path("aloqa/", views.aloqa, name='aloqa'),
    path("login/", views.login_view, name='login'),
    path("register/", views.register_view, name='register'),
    path("checkout/", views.checkout, name='checkout'),
    path("savatcha/", views.savatcha, name='savatcha'),
    path("forgot-password/", views.forgot_password, name='forgot_password'),
    path("reset-password/", views.reset_password, name='reset_password'),
    path("confirm-password/", views.confirm_password, name='confirm_password'),
]
