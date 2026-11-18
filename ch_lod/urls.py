from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

def robots_txt(request):
    lines = [
        "User-agent: GPTBot",
        "Disallow: /",
        "",
        "User-agent: ClaudeBot",
        "Disallow: /",
        "",
        "User-agent: Baiduspider",
        "Disallow: /",
        "",
        "User-agent: *",
        "Crawl-delay: 10",
        "",
        "# Allow human-readable pages",
        "Allow: /events/*/about",
        "Allow: /names/*/about",
        "Allow: /works/*/about",
        "Allow: /venues/*/about",
        "Allow: /instruments/*/about",
        "Allow: /ensembles/*/about",
        "Allow: /genres/*/about",
        "Allow: /roles/*/about",
        "Allow: /vocabulary/roles/*/about",
        "",
        "# Block RDF serialization formats",
        "Disallow: /events/*/xml",
        "Disallow: /events/*/n3",
        "Disallow: /events/*/nt",
        "Disallow: /events/*/turtle",
        "Disallow: /events/*/jsonld",
        "Disallow: /names/*/xml",
        "Disallow: /names/*/n3",
        "Disallow: /names/*/nt",
        "Disallow: /names/*/turtle",
        "Disallow: /names/*/jsonld",
        "Disallow: /works/*/xml",
        "Disallow: /works/*/n3",
        "Disallow: /works/*/nt",
        "Disallow: /works/*/turtle",
        "Disallow: /works/*/jsonld",
        "Disallow: /venues/*/xml",
        "Disallow: /venues/*/n3",
        "Disallow: /venues/*/nt",
        "Disallow: /venues/*/turtle",
        "Disallow: /venues/*/jsonld",
        "Disallow: /instruments/*/xml",
        "Disallow: /instruments/*/n3",
        "Disallow: /instruments/*/nt",
        "Disallow: /instruments/*/turtle",
        "Disallow: /instruments/*/jsonld",
        "Disallow: /ensembles/*/xml",
        "Disallow: /ensembles/*/n3",
        "Disallow: /ensembles/*/nt",
        "Disallow: /ensembles/*/turtle",
        "Disallow: /ensembles/*/jsonld",
        "Disallow: /genres/*/xml",
        "Disallow: /genres/*/n3",
        "Disallow: /genres/*/nt",
        "Disallow: /genres/*/turtle",
        "Disallow: /genres/*/jsonld",
        "Disallow: /roles/*/xml",
        "Disallow: /roles/*/n3",
        "Disallow: /roles/*/nt",
        "Disallow: /roles/*/turtle",
        "Disallow: /roles/*/jsonld",
        "Disallow: /vocabulary/roles/*/xml",
        "Disallow: /vocabulary/roles/*/n3",
        "Disallow: /vocabulary/roles/*/nt",
        "Disallow: /vocabulary/roles/*/turtle",
        "Disallow: /vocabulary/roles/*/jsonld",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# I think this django serach or something, not using it
# from search import views as search_views

urlpatterns = [

    path('robots.txt', robots_txt),

    path('', include('data.urls')),

    path('admin/', admin.site.urls),

    path('wagtail-admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # not using it
    # path('search/', search_views.search, name='search'),
    path('', include('pages.urls')),
    path('datalab/', include(wagtail_urls))

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = urlpatterns + [
#     # For anything not caught by a more specific rule above, hand over to
#     # Wagtail's page serving mechanism. This should be the last pattern in
#     # the list:
#     path("", include(wagtail_urls)),

#     # Alternatively, if you want Wagtail pages to be served from a subpath
#     # of your site, rather than the site root:
#     #    path("pages/", include(wagtail_urls)),
# ]
