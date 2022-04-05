from django.conf.urls import url
from django.urls import path

from wushu.Views import DashboardViews, AthleteViews, CompetitionViews

app_name = 'wushu'

urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/sehir-sporcu-sayisi/$', DashboardViews.City_athlete_cout, name='sehir-sporcu-sayisi'),
    url(r'anasayfa/sporcu/$', DashboardViews.return_athlete_dashboard, name='sporcu'),
    url(r'anasayfa/hakem/$', DashboardViews.return_referee_dashboard, name='hakem'),
    url(r'anasayfa/antrenor/$', DashboardViews.return_coach_dashboard, name='antrenor'),

    # Sporcular
    url(r'sporcu/sporcu-ekle/$', AthleteViews.return_add_athlete, name='sporcu-ekle'),
    url(r'sporcu/sporcular/$', AthleteViews.return_athletes, name='sporcular'),

    # Competition
    url(r'musabaka/musabakalar/$', CompetitionViews.return_competitions, name='musabakalar'),
    url(r'musabaka/musabaka-sanda-sporcu-sec/(?P<pk>\d+)$', CompetitionViews.musabaka_sanda,
        name='musabaka-sanda-ekle'),
    url(r'musabaka/musabaka-taolu-sporcu-sec/(?P<pk>\d+)/$', CompetitionViews.musabaka_taolu,
        name='musabaka-taolu-ekle'),
    url(r'musabaka/SporcuSecim/Taolu/$', CompetitionViews.return_sporcu_sec_taolu, name='taolu-sporcu-sec-ajax'),
    url(r'musabaka/musabaka-taolu-sporcu-kaydet/$', CompetitionViews.musabaka_taolu_sporcu_ekle,
        name='taolu-sporcu-kaydet'),

]
