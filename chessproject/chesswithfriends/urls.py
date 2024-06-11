from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('startgame', views.preaprechessboard, name='startgame'),
	path('about', views.about, name='about'),
	path('contactus', views.contactus, name='contactus'),
	path('privacy-policy', views.privacy_policy, name='privacy-policy'),
	path('terms-and-conditions', views.terms_and_conditions, name='terms-and-conditions'),
	path('disclaimer', views.disclaimer, name='disclaimer'),

	# re_path(r'[a-zA-Z0-9]+blog/(?P<id>\d+)/$]+', views.page_not_found),
]