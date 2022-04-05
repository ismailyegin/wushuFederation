from django.conf.urls import url
from django.urls import path

from wushu.Views import DashboardViews, AthleteViews, CompetitionViews

app_name = 'wushu'

urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
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
    url(r'musabaka/musabaka-duzenle/(?P<pk>\d+)$', CompetitionViews.musabaka_duzenle, name='musabaka-duzenle'),
    url(r'musabaka/musabaka-duzenle/taolu-kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil_taolu,
        name='musabaka-sporcu-kaldir_taolu'),
    url(r'musabaka/musabaka-duzenle/sanda-kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil,
        name='musabaka-sporcu-kaldir'),

    url(r'musabaka/SporcuSecim/Sanda/$', CompetitionViews.return_sporcu_sec_sanda, name='sanda-sporcu-sec-ajax'),
    url(r'musabaka/musabaka-sanda-sporcu-kaydet/$', CompetitionViews.musabaka_sanda_sporcu_ekle,
        name='sanda-sporcu-kaydet'),
    url(r'sporcu/sporcuDuzenle/(?P<pk>\d+)$', AthleteViews.updateathletes, name='update-athletes'),

]
