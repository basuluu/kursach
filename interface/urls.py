from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.pug_store, name='pug_store'),
    url(r'^add_item/$', views.add_item, name='add_item'),
    url(r'^add_sup/$', views.add_sup, name='add_sup'),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^detail/(?P<id>\d+)/del', views.delete_item, name='delete_item'),
    url(r'^edit/(?P<id>\d+)/$', views.edit_item, name='edit_item'),
    url(r'^search/$', views.search_form, name='search_form'),
    url(r'^bin/$', views.bin_v, name='bin_v'),
    url(r'^add_request/$', views.add_request, name='add_request'),
    url(r'^add_income/$', views.add_income, name='add_income'),
    url(r'^journal_req/$', views.journal_req, name='journal_req'),
    url(r'^journal_sup/$', views.journal_sup, name='journal_sup'),
    url(r'^journal_income/$', views.journal_income, name='journal_income'),
    url(r'^income/$', views.income, name="income"),
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^logout/', views.logout_view, name='logout_view'),
    url(r'^register/', views.register_view, name='register_view'),
    url(r'^statistic/', views.statistic, name='statistic'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
