from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap

from pdl.feeds import LatestEntriesFeed
from pdl.sitemaps import ProyectoSitemap, CongresistaSitemap
from seguimientos import views as seg_views
# from django.contrib import admin
from rest_framework import routers

sitemaps = {
    'static': ProyectoSitemap,
    'congresista': CongresistaSitemap,
    }

router = routers.DefaultRouter()
router.register(r'users', seg_views.UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^api', include(router.urls)),
    url(r'^', include('pdl.urls', namespace='pdl')),
    url(r'^p/', include('pdl.urls', namespace='pdl-proyecto')),
    url(r'^p/(?P<short_url>[0-9a-z]+/seguimiento/)', seg_views.index),
    url(r'^rss.xml$', LatestEntriesFeed(), name='pdl-rss'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
    # url(r'^admin/', include(admin.site.urls)),
)
