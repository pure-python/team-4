from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from fb.views import (
    index, post_details, login_view, logout_view, profile_view,

    edit_profile_view, like_view, user_album, user_album_photos,
    edit_post_view, like_view_index, share_view, share_view_index

)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^post/(?P<pk>\d)/$', post_details, name='post_details'),
    url(r'^post/(?P<pk>\d)/like$', like_view, name='like'),
    url(r'^post/(?P<pk>\d)/edit$', edit_post_view, name='edit_post'),

    url(r'^post/(?P<pk>\d)/like_index$', like_view_index, name='like_index'),
    url(r'^post/(?P<pk>\d)/share$', share_view, name='share'),
    url(r'^post/(?P<pk>\d)/share_index$', share_view_index, name='share_index'),

    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^profile/(?P<user>\w+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<user>\w+)/albums$', user_album, name='albums'),
    url(r'^profile/(?P<user>\w+)/albums/(?P<pk>\d)$', user_album_photos, name='album_photos'), 
    url(r'^profile/(?P<user>\w+)/edit$', edit_profile_view, name='edit_profile'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
