"""
Definition of urls for TradingSystemWebSite.
"""

from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#admin.autodiscover()
from TradingSystemApp import views

urlpatterns = [
    # Examples:
    url(r'^$', views.goToMainPage),
    # url(r'^$', TradingSystemWebSite.views.home, name='home'),
    # url(r'^TradingSystemWebSite/', include('TradingSystemWebSite.TradingSystemWebSite.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^gogo/$',views.pylinkweb),
    url(r'^home/$',views.goToMainPage),   
    url(r'^TurtleResult$',views.calTurtleResultMethod),
    url(r'^UpdatingStockDb$',views.UpdatingStockDbMethod),
    
]
