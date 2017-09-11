from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


app_name = 'music'
urlpatterns = [
          #/music/
          url(r'^$',views.index,name='index'),

          url(r'^register/$',views.UserFormView.as_view(),name='register'),
         
          url(r'^login/$',views.login_user,name='login'),
          url(r'^logout/$',views.user_logout,name='logout'),
         
          
   
  
          #/music/<album_id>/
          url(r'^(?P<slug>[\w-]+)/$',views.DetailView.as_view(),name = 'detail'),
           url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),

          # /music/album/add/
          url(r'^album/add/$',views.AlbumCreate.as_view(),name='album-add'),

          # /music/song/add/
          url(r'^(?P<pk>[0-9]+)/song/add/$',views.SongCreate.as_view(),name='song-add'),

           # /music/album/2/
          url(r'^(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),

           # /music/album/2/delete
          url(r'^(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),

           url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='song-delete'),
            url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
             url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),

]
