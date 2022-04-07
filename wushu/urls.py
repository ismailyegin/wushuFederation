from django.conf.urls import url
from django.urls import path

from wushu.Views import DashboardViews, AthleteViews, CompetitionViews, CoachViews, ObserverViews, OfficerViews, \
    JudgeViews, FederationViews

app_name = 'wushu'

urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/federation/$', DashboardViews.return_federation_dashboard, name='federasyon'),

    # Sporcular
    url(r'sporcu/sporcu-ekle/$', AthleteViews.return_add_athlete, name='sporcu-ekle'),
    url(r'sporcu/sporcular/$', AthleteViews.return_athletes, name='sporcular'),
    url(r'sporcu/sporcuDuzenle/(?P<pk>\d+)$', AthleteViews.updateathletes, name='update-athletes'),

    # Competition
    url(r'musabaka/musabakalar/$', CompetitionViews.return_competitions, name='musabakalar'),
    url(r'musabaka/musabaka-sanda-sporcu-sec/(?P<pk>\d+)$', CompetitionViews.musabaka_sanda,
        name='musabaka-sanda-ekle'),
    url(r'musabaka/musabaka-taolu-sporcu-sec/(?P<pk>\d+)/$', CompetitionViews.musabaka_taolu,
        name='musabaka-taolu-ekle'),
    url(r'musabaka/SporcuSecim/Taolu/$', CompetitionViews.return_sporcu_sec_taolu, name='taolu-sporcu-sec-ajax'),
    url(r'musabaka/musabaka-taolu-sporcu-kaydet/$', CompetitionViews.musabaka_taolu_sporcu_ekle,
        name='taolu-sporcu-kaydet'),
    url(r'musabaka/musabaka-ekle/$', CompetitionViews.musabaka_ekle, name='musabaka-ekle'),

    url(r'musabaka/musabaka-duzenle/(?P<pk>\d+)$', CompetitionViews.musabaka_duzenle, name='musabaka-duzenle'),
    url(r'musabaka/musabakalar/musabaka-sil(?P<pk>\d+)$', CompetitionViews.musabaka_sil, name='musabaka-sil'),

    url(r'musabaka/musabaka-duzenle/taolu-kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil_taolu,
        name='musabaka-sporcu-kaldir_taolu'),
    url(r'musabaka/musabaka-duzenle/sanda-kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil,
        name='musabaka-sporcu-kaldir'),

    url(r'musabaka/SporcuSecim/Sanda/$', CompetitionViews.return_sporcu_sec_sanda, name='sanda-sporcu-sec-ajax'),
    url(r'musabaka/musabaka-sanda-sporcu-kaydet/$', CompetitionViews.musabaka_sanda_sporcu_ekle,
        name='sanda-sporcu-kaydet'),

    # Coachs
    url(r'coach/add-coach/$', CoachViews.return_add_coach, name='add-coach'),
    url(r'coach/coaches/$', CoachViews.return_coaches, name='coaches'),
    url(r'coach/update-coach/(?P<pk>\d+)$', CoachViews.updatecoaches, name='update-coaches'),

    # Observers
    url(r'observer/add-observer/$', ObserverViews.return_add_observer, name='add-observer'),
    url(r'observer/observers/$', ObserverViews.return_observers, name='observers'),
    url(r'observer/update-observer/(?P<pk>\d+)$', ObserverViews.updateobservers, name='update-observers'),

    # Officers
    url(r'officer/add-officer/$', OfficerViews.return_add_officer, name='add-officer'),
    url(r'officer/officers/$', OfficerViews.return_officers, name='officers'),
    url(r'officer/update-officer/(?P<pk>\d+)$', OfficerViews.updateofficers, name='update-officers'),

    # Judge
    url(r'judge/add-judge/$', JudgeViews.return_add_judge, name='add-judge'),
    url(r'judge/judges/$', JudgeViews.return_judges, name='judges'),
    url(r'judge/update-judge/(?P<pk>\d+)$', JudgeViews.updatejudges, name='update-judges'),

    # Federation
    url(r'federation/add-registration/$', FederationViews.addFederationGroup, name='add-registration'),
]
