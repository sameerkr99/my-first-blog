from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from . import views as core_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'home/$', views.post_list, name = 'post_list'),
    #url(r'login/$', auth_views.login, {'template_name': 'blog/login.html'}, name='login'),
    url(r'^$', views.welcome, name='welcome'),
    url(r'logout/$',auth_views.logout, {'template_name': 'blog/login.html'},name = 'logout'),
    url(r'home/post/$',views.post_new, name = 'post_new'),
    url(r'home/myposts/$',views.myposts,  name = 'myposts'),
    url(r'home/deletepost/$', views.deletepost, name = 'deletepost'),
    url(r'login/$', views.login_view, name = 'login_view'),
    url(r'signup/$', core_views.signup, name = 'signup'),
    url(r'home/profile/(?P<pk>\d+)/$',views.profile_view, name = 'profile_view'),
    url(r'home/search/$',views.searchresult,name = 'searchresult'),
    #url(r'home/comment/$', views.comments,name = 'comments' ),
    url(r'^post/(?P<pk>\d+)/$', views.post_details, name = 'post_details'),
    url(r'^post/(?P<pk>\d+)/comment/',views.comment,name = 'comment'),
    url(r'^post/(?P<pk>\d+)/edit/',views.edit,name = 'edit'),
    url(r'^post/(?P<pk>\d+)/delete/',views.delete,name = 'delete'),
    url(r'home/profile/(?P<pk>\d+)/update/$', views.profileupdate, name = 'profileupdate'),
    url(r'home/post/(?P<pk>\d+)/$', views.upvotes, name = 'upvote'),
    url(r'home/post/(?P<pk>\d+)/users/$',views.upvoted_users, name = 'upvoted_users'),
    url(r'home/post/editpost/(?P<pk>\d+)/$',views.editpost,name= 'editpost'),
    url(r'home/profile/updatedp/$',views.updateDp, name = 'updateDp'),
    url(r'^weather/$',views.weather, name='weather'),
    url(r'home/(?P<pk>\d+)/$',views.filter,name='filter'),
    url('^', include('django.contrib.auth.urls')),
    url(r'createpost/$',views.createPost.as_view(), name = 'createpost'),
    url(r'removepost/(?P<pk>\d+)/$',views.removePost.as_view()),
    url(r'apitesting/$',views.testapi),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)