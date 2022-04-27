from django.conf.urls import url

from wushu.Views import DashboardViews, AthleteViews, CompetitionViews, CoachViews, ObserverViews, OfficerViews, \
    JudgeViews, FederationViews, UsersViews

app_name = 'wushu'

urlpatterns = [

    # Dashboard
    url(r'anasayfa/admin/$', DashboardViews.return_admin_dashboard, name='admin'),
    url(r'anasayfa/federation/$', DashboardViews.return_federation_dashboard, name='federasyon'),

    # Sporcular
    url(r'sporcu/sporcu-ekle/$', AthleteViews.return_add_athlete, name='sporcu-ekle'),
    url(r'sporcu/sporcular/$', AthleteViews.return_athletes, name='sporcular'),
    url(r'sporcu/sporcuDuzenle/(?P<pk>\d+)$', AthleteViews.updateathletes, name='update-athletes'),
    url(r'sporcu/sporcu-sil/(?P<pk>\d+)$', AthleteViews.delete_athlete, name='delete-athlete'),

    # Competition
    url(r'musabaka/musabakalar/$', CompetitionViews.return_competitions, name='musabakalar'),
    url(r'musabaka/musabaka-ekle/$', CompetitionViews.musabaka_ekle, name='musabaka-ekle'),
    url(r'musabaka/musabaka-duzenle/(?P<pk>\d+)$', CompetitionViews.musabaka_duzenle, name='musabaka-duzenle'),
    url(r'musabaka/musabakalar/musabaka-sil(?P<pk>\d+)$', CompetitionViews.musabaka_sil, name='musabaka-sil'),

    url(r'musabaka/musabaka-sanda-sporcu-sec/(?P<pk>\d+)$', CompetitionViews.musabaka_sanda,
        name='musabaka-sanda-ekle'),
    url(r'musabaka/musabaka-taolu-sporcu-sec/(?P<pk>\d+)/$', CompetitionViews.musabaka_taolu,
        name='musabaka-taolu-ekle'),
    url(r'musabaka/SporcuSecim/Taolu/$', CompetitionViews.return_sporcu_sec_taolu, name='taolu-sporcu-sec-ajax'),
    url(r'musabaka/musabaka-taolu-sporcu-kaydet/$', CompetitionViews.musabaka_taolu_sporcu_ekle,
        name='taolu-sporcu-kaydet'),
    url(r'musabaka/musabaka-duzenle/taolu-kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil_taolu,
        name='musabaka-sporcu-kaldir_taolu'),
    url(r'musabaka/musabaka-duzenle/sanda-kaldir/(?P<pk>\d+)/$', CompetitionViews.musabaka_sporcu_sil,
        name='musabaka-sporcu-kaldir'),
    url(r'musabaka/SporcuSecim/Sanda/$', CompetitionViews.return_sporcu_sec_sanda, name='sanda-sporcu-sec-ajax'),
    url(r'musabaka/musabaka-sanda-sporcu-kaydet/$', CompetitionViews.musabaka_sanda_sporcu_ekle,
        name='sanda-sporcu-kaydet'),
    url(r'musabaka/taolu_year_transmission/$', CompetitionViews.taolu_year_transmission,
        name='taolu_year_transmission'),

    # Coachs
    url(r'coach/add-coach/$', CoachViews.return_add_coach, name='add-coach'),
    url(r'coach/coaches/$', CoachViews.return_coaches, name='coaches'),
    url(r'coach/update-coach/(?P<pk>\d+)$', CoachViews.updatecoaches, name='update-coaches'),
    url(r'coach/delete-coach/(?P<pk>\d+)$', CoachViews.delete_coach, name='delete-coach'),

    # Observers
    url(r'observer/add-observer/$', ObserverViews.return_add_observer, name='add-observer'),
    url(r'observer/observers/$', ObserverViews.return_observers, name='observers'),
    url(r'observer/update-observer/(?P<pk>\d+)$', ObserverViews.updateobservers, name='update-observers'),
    url(r'observer/delete-observer/(?P<pk>\d+)$', ObserverViews.delete_observer, name='delete-observer'),

    # Officers
    url(r'officer/add-officer/$', OfficerViews.return_add_officer, name='add-officer'),
    url(r'officer/officers/$', OfficerViews.return_officers, name='officers'),
    url(r'officer/update-officer/(?P<pk>\d+)$', OfficerViews.updateofficers, name='update-officers'),
    url(r'officer/delete-officer/(?P<pk>\d+)$', OfficerViews.delete_officer, name='delete-officer'),

    # Judge
    url(r'judge/add-judge/$', JudgeViews.return_add_judge, name='add-judge'),
    url(r'judge/judges/$', JudgeViews.return_judges, name='judges'),
    url(r'judge/update-judge/(?P<pk>\d+)$', JudgeViews.updatejudges, name='update-judges'),
    url(r'judge/delete-judge/(?P<pk>\d+)$', JudgeViews.delete_judge, name='delete-judge'),

    # Federation
    url(r'federation/add-registration/$', FederationViews.addFederationGroup, name='add-registration'),
    url(r'federation/add-federation/$', FederationViews.return_add_federation, name='add-federation'),
    url(r'federation/update-federation/(?P<pk>\d+)$', FederationViews.update_federation, name='update-federations'),
    url(r'federation/federations/$', FederationViews.return_federations, name='federations'),
    url(r'federation/delete-federation/(?P<pk>\d+)$', FederationViews.delete_federation, name='delete-federation'),

    url(r'federation/registration-list/$', FederationViews.registration_list, name='registration-list'),

    url(r'musabaka/taoluekle/$', AthleteViews.return_taolu, name='taolu-katagori'),
    url(r'musabaka/taolu/sil/(?P<pk>\d+)$', AthleteViews.categoryTaoluDelete, name='taolu-katagori-sil'),
    url(r'musabaka/taolu/Duzenle/(?P<pk>\d+)$', AthleteViews.categoryTaoluUpdate, name='taolu-katagori-duzenle'),

    # Taoulu yaş eklendisi
    url(r'musabaka/taoluekleyas/$', AthleteViews.return_taolu_years, name='yas-taolu-katagori'),
    url(r'musabaka/taoluekleyas/sil/(?P<pk>\d+)$', AthleteViews.categoryTaoluyearsDelete,
        name='yas-taolu-katagori-sil'),
    url(r'musabaka/taoluekleyas/Duzenle/(?P<pk>\d+)$', AthleteViews.categoryTaoluyearsUpdate,
        name='yas-taolu-katagori-duzenle'),

    # Sanda Yaş
    url(r'sporcu/sanda-ekleyas/$', AthleteViews.return_sanda_years, name='return_sanda_years'),
    url(r'sporcu/sanda-ekleyas/sil/(?P<pk>\d+)$', AthleteViews.categorySandayearsDelete, name='yas-sanda-katagori-sil'),
    url(r'sporcu/sanda-ekleyas/Duzenle/(?P<pk>\d+)$', AthleteViews.categorySandayearsUpdate,
        name='yas-sanda-katagori-duzenle'),

    url(r'competition/sanda-weight-category/$', CompetitionViews.return_sanda_weight_category,
        name='sanda-weight-category'),
    url(r'competition/sanda-weight-category-delete/(?P<pk>\d+)$', CompetitionViews.sanda_weight_category_delete,
        name='sanda-weight-category-delete'),
    url(r'competition/sanda-weight-category-update/(?P<pk>\d+)$', CompetitionViews.sanda_weight_category_update,
        name='sanda-weight-category-update'),
    url(r'competition/get_sanda-weight-category', CompetitionViews.get_weight_category, name='get_weight_category'),
    # url(r'showproducts', PdfConvertViews.show_products, name='showproducts'),
    # url(r'create-pdf', PdfConvertViews.pdf_report_create, name='create-pdf'),
    # url(r'java-test', PdfConvertViews.java, name='java-test'),
    url(r'profile/image/$', UsersViews.profile_image, name='profile_image'),

]
