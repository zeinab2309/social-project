
from  django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
app_name="social"

urlpatterns=[
    path('',views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('register/', views.register, name="register"),
    path('user/edit', views.edit_user, name="edit_account"),
    path('ticket', views.ticket, name="ticket"),

    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset', auth_views.PasswordResetView.as_view(success_url='password-reset/done/'),
         name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('posts/', views.post_list, name="post_list"),
    path('posts/post<slug:tag_slug>/', views.post_list, name="post_list_by_tag"),
    path('posts/create_posts/', views.create_post, name="create_post"),
    path('posts/detail<pk>/', views.post_detail, name="post_detail"),
    path('search/',views.post_search, name="post_search"),
    path('posts/<int:post_id>/comment', views.post_comment, name="post_comment"),
    path('profile/create/<int:post_id>', views.edit_post, name="edit_post"),
    path('profile/delete_post/<int:post_id>', views.delete_post, name="delete_post"),
    path('profile/delete_image/<int:image_id>', views.delete_image, name="delete_image"),
    path('like_post/', views.like_post,name='like_post'),
    path('save_post/', views.save_post,name='save_post'),
    path('users/',views.user_list,name='user_list'),
    path('users/<username>',views.user_detail,name='user_detail'),
    path('follow/', views.user_follow, name='user_follow'),
    path('followers/', views.user_followers, name='user_followers'),
    path('following/', views.user_following, name='user_following'),
    path('posts/<int:post_id>/likes/', views.user_liked, name='user_liked'),
]