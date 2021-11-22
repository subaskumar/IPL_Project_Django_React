
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from IPL_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Ipl_Team/', views.IPLTeam_API.as_view()),
    path('Ipl_Team/<int:id>/', views.IPLTeam_API.as_view()),
    path('player/', views.Player_API.as_view()),
    path('player/<int:id>/', views.Player_API.as_view()),
    # path('Ipl_Team_list/<int:id>/', views.IPLTeamList_API.as_view()),
    # path('Ipl_Team_list/', views.IPLTeamList_API.as_view()),
    path('addPlayer/', views.Addplayer_view)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
