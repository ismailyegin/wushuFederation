import traceback
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework.decorators import api_view

from wushu.Forms.SandaWeightCategoryForm import SandaWeightCategoryForm
from wushu.Forms.CompetitionForm import CompetitionForm
from wushu.Forms.DisabledCompetitionForm import DisabledCompetitionForm
from wushu.Forms.JudgeForm import JudgeForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.UserForm import UserForm
from wushu.Forms.competitonSearchForm import CompetitionSearchForm
from wushu.models import Competition, YearsSandaCategory, TaoluCategory, YearsTaoluCategory, Federation, Athlete, \
    EnumFields, \
    TaoluAthlete, SandaAthlete, Coach, Observer, Officer, Judge, SandaWeightCategory, Person
from wushu.models.Hotel import Hotel
from wushu.models.SandaCoach import SandaCoach
from wushu.models.SandaHotel import SandaHotel
from wushu.models.SandaJudge import SandaJudge
from wushu.models.SandaObserver import SandaObserver
from wushu.models.SandaOfficer import SandaOfficer
from wushu.models.TaoluCoach import TaoluCoach
from wushu.models.TaoluHotel import TaoluHotel
from wushu.models.TaoluJudge import TaoluJudge
from wushu.models.TaoluOfficer import TaoluOfficer
from wushu.models.TaoluObserver import TaoluObserver
from wushu.serializers.SandaWeightCategorySerializer import SandaWeightCategorySerializer
from wushu.services import general_methods
from itertools import chain


@login_required
def return_competitions(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.user.groups.filter(name='Federation'):
        competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                                 registerFinishDate__gte=timezone.now())
    elif request.user.groups.filter(name='Admin'):
        competition = Competition.objects.all()
    else:
        competition = None

    competitions = Competition.objects.all().order_by('-startDate')
    if request.user.groups.filter(name='Federation'):
        athletes = Athlete.objects.filter(federation__user=request.user)
    elif request.user.groups.filter(name='Admin'):
        athletes = Athlete.objects.all()
    else:
        athletes = None

    return render(request, 'musabaka/musabakalar.html', {'competitions': competitions,
                                                         'application': competition,
                                                         'athletes': athletes, })


@login_required
def musabaka_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = CompetitionForm()
    if request.method == 'POST':
        competition_form = CompetitionForm(request.POST)
        if competition_form.is_valid():
            competition = competition_form.save(commit=False)
            competition.save()

            mesaj = str(competition.name) + ' added.  '
            log = general_methods.logwrite(request, request.user, mesaj)

            messages.success(request, 'The competition has been successfully registered.')

            return redirect('wushu:musabakalar')
        else:

            messages.warning(request, 'Check Fields')

    return render(request, 'musabaka/musabaka-ekle.html',
                  {'competition_form': competition_form, })


@login_required
def musabaka_duzenle(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    categori = None
    athletes = None
    competition_form = None

    user = request.user

    if request.user.groups.filter(name__in=['Admin']):
        competition_form = CompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            athletes = SandaAthlete.objects.filter(competition=musabaka)
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            athletes = TaoluAthlete.objects.filter(competition=musabaka)
    if request.user.groups.filter(name__in=['Federation']):
        competition_form = DisabledCompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            athletes = SandaAthlete.objects.filter(competition=musabaka).filter(athlete__federation__user=request.user)
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            athletes = TaoluAthlete.objects.filter(competition=musabaka).filter(athlete__federation__user=request.user)

    if request.method == 'POST':
        if competition_form.is_valid():
            if request.user.groups.filter(name__in=['Admin']):
                competition = competition_form.save(commit=False)
                competition.save()
                mesaj = str(competition.name) + 'The competition has been updated.   '
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Competition Successfully Updated.')
            return redirect('wushu:musabaka-duzenle', pk=pk)
        else:

            messages.warning(request, 'Check Fields')

    return render(request, 'musabaka/musabaka-duzenle.html',
                  {'competition_form': competition_form, 'competition': musabaka, 'athletes': athletes,
                   'categori': categori})


@login_required
def musabaka_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Competition.objects.get(pk=pk)
            log = str(obj.name) + "  Competition deleted."
            log = general_methods.logwrite(request, request.user, log)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_sanda(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    weightCategory = SandaWeightCategory.objects.all().order_by('categoryName')

    categori = None
    athletes = None
    coaches = None
    observers = None
    officers = None
    judges = None
    taoluHotels = None
    hotels = None

    federations = None
    athleteSec = None
    antrenorSec = None
    gozlemciSec = None
    resmiGorevliSec = None
    hakemSec = None
    otelSec = None

    user = request.user

    if request.user.groups.filter(name__in=['Admin']):
        competition_form = CompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            federations = Federation.objects.all()
            athleteSec = Athlete.objects.all().order_by('person__name')
            antrenorSec = Coach.objects.all().order_by('person__name')
            gozlemciSec = Observer.objects.all().order_by('person__name')
            resmiGorevliSec = Officer.objects.all().order_by('person__name')
            hakemSec = Judge.objects.all().order_by('person__name')

            taoluHotelPersons = TaoluHotel.objects.all().values('hotel__person')
            sandaHotelPersons = SandaHotel.objects.all().values('hotel__person')
            athleteSec2 = Athlete.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            antrenorSec2 = Coach.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            gozlemciSec2 = Observer.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            resmiGorevliSec2 = Officer.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            hakemSec2 = Judge.objects.all().exclude(person__in=taoluHotelPersons).exclude(person__in=sandaHotelPersons)
            otelSec = list(chain(athleteSec2, antrenorSec2, gozlemciSec2, resmiGorevliSec2, hakemSec2))

            athletes = SandaAthlete.objects.filter(competition=musabaka)
            coaches = SandaCoach.objects.filter(competition=musabaka)
            observers = SandaObserver.objects.filter(competition=musabaka)
            officers = SandaOfficer.objects.filter(competition=musabaka)
            judges = SandaJudge.objects.filter(competition=musabaka)
            sandaHotels = SandaHotel.objects.filter(competition=musabaka)
            hotels = Hotel.HOTELTYPE
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            athletes = TaoluAthlete.objects.filter(competition=musabaka)
    if request.user.groups.filter(name__in=['Federation']):
        competition_form = DisabledCompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            federation = Federation.objects.get(user=request.user)
            athleteSec = Athlete.objects.filter(federation=federation)
            antrenorSec = Coach.objects.filter(federation=federation)
            gozlemciSec = Observer.objects.filter(federation=federation)
            resmiGorevliSec = Officer.objects.filter(federation=federation)
            hakemSec = Judge.objects.filter(federation=federation)

            taoluHotelPersons = TaoluHotel.objects.all().filter(
                hotel__federation__user=request.user).values('hotel__person')
            sandaHotelPersons = SandaHotel.objects.all().filter(
                hotel__federation__user=request.user).values('hotel__person')
            athleteSec2 = Athlete.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            antrenorSec2 = Coach.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            gozlemciSec2 = Observer.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            resmiGorevliSec2 = Officer.objects.filter(federation=federation).exclude(
                person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            hakemSec2 = Judge.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            otelSec = list(chain(athleteSec2, antrenorSec2, gozlemciSec2, resmiGorevliSec2, hakemSec2))

            athletes = SandaAthlete.objects.filter(competition=musabaka).filter(athlete__federation__user=request.user)
            coaches = SandaCoach.objects.filter(competition=musabaka).filter(coach__federation__user=request.user)
            observers = SandaObserver.objects.filter(competition=musabaka).filter(
                observer__federation__user=request.user)
            officers = SandaOfficer.objects.filter(competition=musabaka).filter(officer__federation__user=request.user)
            judges = SandaJudge.objects.filter(competition=musabaka).filter(judge__federation__user=request.user)
            sandaHotels = SandaHotel.objects.filter(competition=musabaka).filter(hotel__federation__user=request.user)
            hotels = Hotel.HOTELTYPE
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            athletes = TaoluAthlete.objects.filter(competition=musabaka).filter(athlete__federation__user=request.user)

    return render(request, 'musabaka/musabaka-SandaSporcusec.html',
                  {'competition': musabaka, 'weightCategory': weightCategory, 'athletes': athletes,
                   'categori': categori, 'athleteSec': athleteSec, 'antrenorSec': antrenorSec,
                   'gozlemciSec': gozlemciSec, 'resmiGorevliSec': resmiGorevliSec, 'hakemSec': hakemSec,
                   'coaches': coaches, 'observers': observers, 'officers': officers, 'judges': judges,
                   'federations': federations, 'otelSec': otelSec, 'sandaHotels': sandaHotels, 'hotels': hotels, })


@login_required
def musabaka_taolu(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    user_form = UserForm()
    judge_form = JudgeForm()

    musabaka = Competition.objects.get(pk=pk)
    yearscategory = YearsTaoluCategory.objects.all()
    category = TaoluCategory.objects.all()

    categori = None
    athletes = None
    coaches = None
    observers = None
    officers = None
    judges = None
    taoluHotels = None
    hotels = None

    user = request.user

    federations = None
    athleteSec = None
    antrenorSec = None
    gozlemciSec = None
    resmiGorevliSec = None
    hakemSec = None
    otelSec = None

    if request.user.groups.filter(name__in=['Admin']):
        competition_form = CompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            athletes = SandaAthlete.objects.filter(competition=musabaka)
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            federations = Federation.objects.all().order_by('person__name')
            athleteSec = Athlete.objects.all().order_by('person__name')
            antrenorSec = Coach.objects.all().order_by('person__name')
            gozlemciSec = Observer.objects.all().order_by('person__name')
            resmiGorevliSec = Officer.objects.all().order_by('person__name')
            hakemSec = Judge.objects.all().order_by('person__name')

            taoluHotelPersons = TaoluHotel.objects.all().values('hotel__person')
            sandaHotelPersons = SandaHotel.objects.all().values('hotel__person')
            athleteSec2 = Athlete.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            antrenorSec2 = Coach.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            gozlemciSec2 = Observer.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            resmiGorevliSec2 = Officer.objects.all().exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            hakemSec2 = Judge.objects.all().exclude(person__in=taoluHotelPersons).exclude(person__in=sandaHotelPersons)
            otelSec = list(chain(athleteSec2, antrenorSec2, gozlemciSec2, resmiGorevliSec2, hakemSec2))

            athletes = TaoluAthlete.objects.filter(competition=musabaka)
            coaches = TaoluCoach.objects.filter(competition=musabaka)
            observers = TaoluObserver.objects.filter(competition=musabaka)
            officers = TaoluOfficer.objects.filter(competition=musabaka)
            judges = TaoluJudge.objects.filter(competition=musabaka)
            taoluHotels = TaoluHotel.objects.filter(competition=musabaka)
            hotels = Hotel.HOTELTYPE
    if request.user.groups.filter(name__in=['Federation']):
        competition_form = DisabledCompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            athletes = SandaAthlete.objects.filter(competition=musabaka).filter(athlete__federation__user=request.user)
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            federation = Federation.objects.get(user=request.user)
            athleteSec = Athlete.objects.filter(federation=federation).order_by('person__name')
            antrenorSec = Coach.objects.filter(federation=federation).order_by('person__name')
            gozlemciSec = Observer.objects.filter(federation=federation).order_by('person__name')
            resmiGorevliSec = Officer.objects.filter(federation=federation).order_by('person__name')
            hakemSec = Judge.objects.filter(federation=federation).order_by('person__name')

            taoluHotelPersons = TaoluHotel.objects.all().filter(
                hotel__federation__user=request.user).values('hotel__person')
            sandaHotelPersons = SandaHotel.objects.all().filter(
                hotel__federation__user=request.user).values('hotel__person')
            athleteSec2 = Athlete.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            antrenorSec2 = Coach.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            gozlemciSec2 = Observer.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            resmiGorevliSec2 = Officer.objects.filter(federation=federation).exclude(
                person__in=taoluHotelPersons).exclude(person__in=sandaHotelPersons)
            hakemSec2 = Judge.objects.filter(federation=federation).exclude(person__in=taoluHotelPersons).exclude(
                person__in=sandaHotelPersons)
            otelSec = list(chain(athleteSec2, antrenorSec2, gozlemciSec2, resmiGorevliSec2, hakemSec2))

            athletes = TaoluAthlete.objects.filter(competition=musabaka).filter(athlete__federation__user=request.user)
            coaches = TaoluCoach.objects.filter(competition=musabaka).filter(coach__federation__user=request.user)
            observers = TaoluObserver.objects.filter(competition=musabaka).filter(
                observer__federation__user=request.user)
            officers = TaoluOfficer.objects.filter(competition=musabaka).filter(officer__federation__user=request.user)
            judges = TaoluJudge.objects.filter(competition=musabaka).filter(judge__federation__user=request.user)
            taoluHotels = TaoluHotel.objects.filter(competition=musabaka).filter(hotel__federation__user=request.user)
            hotels = Hotel.HOTELTYPE

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        judge_form = JudgeForm(request.POST)

    return render(request, 'musabaka/musabaka-taolu-sporcu-sec.html',
                  {'competition': musabaka, 'yearscategory': yearscategory, 'category': category,
                   'user_form': user_form, 'person_form': person_form, 'judge_form': judge_form, 'athletes': athletes,
                   'categori': categori, 'athleteSec': athleteSec, 'coaches': coaches, 'observers': observers,
                   'officers': officers, 'judges': judges, 'antrenorSec': antrenorSec, 'gozlemciSec': gozlemciSec,
                   'resmiGorevliSec': resmiGorevliSec, 'hakemSec': hakemSec, 'federations': federations,
                   'otelSec': otelSec, 'taoluHotels': taoluHotels, 'hotels': hotels, })


@login_required
def return_sporcu_sec_taolu(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    total = 0

    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        musabaka = Competition.objects.get(pk=request.GET.get('competition'))



    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10

    coa = []
    # for item in TaoluAthlete.objects.filter(competition=musabaka):
    #     coa.append(item.athlete.pk)

    if length == -1:
        if user.groups.filter(name='Federation'):
            federation = Federation.objects.get(user=request.user)
            modeldata = Athlete.objects.exclude(id__in=coa).filter(federation=federation).distinct()
            for item in modeldata:
                print(item)
            total = modeldata.count()
        elif user.groups.filter(name__in=['Yonetim', 'Admin']):

            modeldata = Athlete.objects.exclude(id__in=coa).distinct()

            total = modeldata.count()
    else:
        if search:
            if user.groups.filter(name='Federation'):
                federation = Federation.objects.get(user=request.user)

                modeldata = Athlete.objects.exclude(id__in=coa).filter(federation=federation).filter(
                    Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                        user__email__icontains=search)).distinct()

                total = modeldata.count()
                # .exclude(belts=None).exclude(licenses=None).exclude(beltexam__athletes__user__in = exam_athlete).filter(licenses__branch=sinav.branch,licenses__status='Onaylandı').filter(belts__branch=sinav.branch,belts__status='Onaylandı').distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                modeldata = Athlete.objects.exclude(id__in=coa).filter(
                    Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                        user__email__icontains=search)).distinct()
                total = modeldata.count()
        else:
            if user.groups.filter(name='Federation'):
                federation = Federation.objects.get(user=request.user)
                modeldata = Athlete.objects.exclude(id__in=coa).filter(federation=federation).distinct()[
                            start:start + length]
                total = Athlete.objects.exclude(id__in=coa).filter(federation=federation).distinct().count()
                # .exclude(belts=None).exclude(licenses=None).exclude(beltexam__athletes__user__in = exam_athlete).filter(licenses__branch=sinav.branch,licenses__status='Onaylandı').filter(belts__branch=sinav.branch,belts__status='Onaylandı').distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):

                modeldata = Athlete.objects.exclude(id__in=coa)[start:start + length]
                total = Athlete.objects.count()

    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        data = {
            'say': say,
            'pk': item.pk,
            'name': item.person.name + ' ' + item.person.surName,

        }
        beka.append(data)
        say += 1

    response = {
        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def musabaka_taolu_sporcu_ekle(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            compettion = Competition.objects.get(pk=request.POST.get('competition'))
            id = int(request.POST.get('id'))

            if compettion.subBranch == EnumFields.SUBBRANCH.TAOLU.value:
                if id == 1:
                    category = TaoluCategory.objects.get(pk=request.POST.get('category'))
                    athlete = Athlete.objects.get(pk=request.POST.get('athleteId'))
                    athDulianComp = TaoluAthlete.objects.filter(athlete=athlete).filter(category__isDuilian=1).count()
                    athComp = TaoluAthlete.objects.filter(athlete=athlete).filter(category__isDuilian=0).count()

                    if SandaAthlete.objects.filter(athlete=athlete).filter(competitiontype='Sanda'):
                        return JsonResponse({'status': 'Warning',
                                             'messages': 'Athletes registered in Sanda cannot be registered in Taolu.'})
                    else:
                        if not TaoluAthlete.objects.filter(athlete=athlete).filter(category=category):
                            if (category.isDuilian == 1 and athDulianComp < 2) or (
                                    category.isDuilian == 0 and athComp < 2):
                                taoluAthlete = TaoluAthlete(
                                    competition=compettion,
                                    category=category,
                                    athlete=athlete,
                                )
                                taoluAthlete.save()
                                mesaj = str(
                                    compettion.name) + ' to the competition ' + taoluAthlete.athlete.person.name + ' ' + taoluAthlete.athlete.person.surName + '  added'
                                log = general_methods.logwrite(request, request.user, mesaj)
                                return JsonResponse({'status': 'Success', 'messages': 'Athlete Successfully Added'})

                            else:
                                return JsonResponse({'status': 'Warning',
                                                     'messages': 'It is not possible to register for more than two competitions.'})
                        else:
                            return JsonResponse({'status': 'Warning',
                                                 'messages': 'It is not possible to register twice in the same category.'})

                elif id == 2:
                    coach = Coach.objects.get(pk=request.POST.get('antrenorId'))
                    if not TaoluCoach.objects.filter(coach=coach):
                        taoluCoach = TaoluCoach(
                            competition=compettion,
                            coach=coach,
                        )
                        taoluCoach.save()
                        mesaj = str(
                            compettion.name) + ' to the competition ' + taoluCoach.coach.person.name + ' ' + taoluCoach.coach.person.surName + '  added'
                        log = general_methods.logwrite(request, request.user, mesaj)
                        return JsonResponse({'status': 'Success', 'messages': 'Coach Successfully Added'})
                    else:
                        return JsonResponse({'status': 'Warning', 'messages': 'Coach already added'})

                elif id == 3:
                    observer = Observer.objects.get(pk=request.POST.get('gozlemciId'))
                    taoluObserver = TaoluObserver(
                        competition=compettion,
                        observer=observer,
                    )
                    taoluObserver.save()
                    mesaj = str(
                        compettion.name) + ' to the competition ' + taoluObserver.observer.person.name + ' ' + taoluObserver.observer.person.surName + '  added'
                    log = general_methods.logwrite(request, request.user, mesaj)
                    return JsonResponse({'status': 'Success', 'messages': 'Observer Successfully Added'})

                elif id == 4:
                    officer = Officer.objects.get(pk=request.POST.get('resmiGorevliId'))
                    if not TaoluOfficer.objects.filter(officer=officer):
                        taoluOfficer = TaoluOfficer(
                            competition=compettion,
                            officer=officer,
                        )
                        taoluOfficer.save()
                        mesaj = str(
                            compettion.name) + ' to the competition ' + taoluOfficer.officer.person.name + ' ' + taoluOfficer.officer.person.surName + '  added'
                        log = general_methods.logwrite(request, request.user, mesaj)
                        return JsonResponse({'status': 'Success', 'messages': 'Official Successfully Added'})
                    else:
                        return JsonResponse({'status': 'Warning', 'messages': 'Official already added'})


                elif id == 5:
                    judge = Judge.objects.get(pk=request.POST.get('hakemId'))
                    if not TaoluJudge.objects.filter(judge=judge):
                        if judge.category == 1 and TaoluJudge.objects.filter(judge__federation__user=request.user).filter(
                                judge__category=1):
                            return JsonResponse({'status': 'Warning',
                                                 'messages': 'More than one referee cannot be registered.Please add a Candıdate judge '})

                        taoluJudge = TaoluJudge(
                            competition=compettion,
                            judge=judge,
                        )

                        taoluJudge.save()
                        mesaj = str(
                            compettion.name) + ' to the competition ' + taoluJudge.judge.person.name + ' ' + taoluJudge.judge.person.surName + '  added'
                        log = general_methods.logwrite(request, request.user, mesaj)
                        return JsonResponse({'status': 'Success', 'messages': 'Referee Successfully Added'})
                    else:
                        return JsonResponse({'status': 'Warning', 'messages': 'Referee already added'})

                elif id == 6:
                    person = None
                    federation = None
                    personId = int(request.POST.get('personId'))
                    name = request.POST.get('hotelRoom')
                    registerStartDate = request.POST.get('registerStartDate')
                    registerFinishDate = request.POST.get('registerFinishDate')
                    finishDate = datetime.strptime(registerFinishDate, "%Y-%m-%d").date()
                    startDate = datetime.strptime(registerStartDate, "%Y-%m-%d").date()
                    totalDay = finishDate - startDate
                    totalDay = totalDay.days
                    if name == 'SINGLE ROOM-81€':
                        price = totalDay * 81
                    else:
                        price = totalDay * 63
                    person = Person.objects.get(pk=personId)
                    if request.user.groups.filter(name='Admin'):
                        if Athlete.objects.filter(person=person):
                            federation = Athlete.objects.get(person=person).federation
                        elif Coach.objects.filter(person=person):
                            federation = Coach.objects.get(person=person).federation
                        elif Observer.objects.filter(person=person):
                            federation = Observer.objects.get(person=person).federation
                        elif Officer.objects.filter(person=person):
                            federation = Officer.objects.get(person=person).federation
                        elif Judge.objects.filter(person=person):
                            federation = Judge.objects.get(person=person).federation
                    elif request.user.groups.filter(name='Federation'):
                        federation = Federation.objects.get(user=request.user)

                    hotel = Hotel(
                        person=person, name=name, registerStartDate=registerStartDate,
                        registerFinishDate=registerFinishDate, federation=federation, totalDay=totalDay, price=price
                    )
                    hotel.save()

                    taoluHotel = TaoluHotel(
                        hotel=hotel, competition=compettion
                    )
                    taoluHotel.save()

                    mesaj = ' Hotel registration has been made.'
                    log = general_methods.logwrite(request, request.user, mesaj)
                    return JsonResponse({'status': 'Success', 'messages': 'Hotel registration has been made.'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'The sub-category of the competition is not Sanda'})



        except Exception as e:

            traceback.print_exception()
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_sporcu_sil_taolu(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            id = int(request.POST.get('id'))
            if id == 1:
                athlete = TaoluAthlete.objects.get(pk=pk)
                athlete.delete()
            elif id == 2:
                coach = TaoluCoach.objects.get(pk=pk)
                coach.delete()
            elif id == 3:
                observer = TaoluObserver.objects.get(pk=pk)
                observer.delete()
            elif id == 4:
                officer = TaoluOfficer.objects.get(pk=pk)
                officer.delete()
            elif id == 5:
                judge = TaoluJudge.objects.get(pk=pk)
                judge.delete()
            elif id == 6:
                taoluHotel = TaoluHotel.objects.get(pk=pk)
                hotel = taoluHotel.hotel
                taoluHotel.delete()
                hotel.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_sporcu_sil(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            id = int(request.POST.get('id'))
            if id == 1:
                athlete = SandaAthlete.objects.get(pk=pk)
                athlete.delete()
            elif id == 2:
                coach = SandaCoach.objects.get(pk=pk)
                coach.delete()
            elif id == 3:
                observer = SandaObserver.objects.get(pk=pk)
                observer.delete()
            elif id == 4:
                officer = SandaOfficer.objects.get(pk=pk)
                officer.delete()
            elif id == 5:
                judge = SandaJudge.objects.get(pk=pk)
                judge.delete()
            elif id == 6:
                sandaHotel = SandaHotel.objects.get(pk=pk)
                hotel = sandaHotel.hotel
                sandaHotel.delete()
                hotel.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_sporcu_sec_sanda(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    total = 0

    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        musabaka = Competition.objects.get(pk=request.GET.get('competition'))



    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10

    coa = []
    for item in SandaAthlete.objects.filter(competition=musabaka):
        coa.append(item.athlete.pk)

    if length == -1:
        if user.groups.filter(name='Federation'):
            federation = Federation.objects.get(user=request.user)
            modeldata = Athlete.objects.exclude(id__in=coa).filter(federation=federation).distinct()
            for item in modeldata:
                print(item)
            total = modeldata.count()
            # .exclude(belts=None).exclude(licenses=None).exclude(beltexam__athletes__user__in = exam_athlete).filter(licenses__branch=sinav.branch,licenses__status='Onaylandı').filter(belts__branch=sinav.branch,belts__status='Onaylandı').distinct()
        elif user.groups.filter(name__in=['Yonetim', 'Admin']):

            modeldata = Athlete.objects.exclude(id__in=coa).distinct()

            total = modeldata.count()
            # print('elimizde olanlar', athletes)
            # kategori.athlete.exclude(
            # exclude(belts=None).exclude(licenses=None).exclude(beltexam__athletes__user__in = exam_athlete).filter(licenses__branch=sinav.branch,licenses__status='Onaylandı').filter(belts__branch=sinav.branch,belts__status='Onaylandı')
        #   .exclude(belts__definition__parent_id=None)    eklenmeli ama eklendigi zaman kuşaklarindan bir tanesi en üst olunca almıyor
    else:
        if search:
            if user.groups.filter(name='Federation'):

                federation = Federation.objects.get(user=request.user)
                modeldata = Athlete.objects.exclude(id__in=coa).filter(federation=federation).filter(
                    Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                        user__email__icontains=search)).distinct()

                total = modeldata.count()
                # .exclude(belts=None).exclude(licenses=None).exclude(beltexam__athletes__user__in = exam_athlete).filter(licenses__branch=sinav.branch,licenses__status='Onaylandı').filter(belts__branch=sinav.branch,belts__status='Onaylandı').distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                modeldata = Athlete.objects.exclude(id__in=coa).filter(
                    Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                        user__email__icontains=search)).distinct()
                total = modeldata.count()

        else:
            if user.groups.filter(name='Federation'):

                federation = Federation.objects.get(user=request.user)
                modeldata = Athlete.objects.exclude(id__in=coa).filter(federation=federation).distinct()[
                            start:start + length]
                total = Athlete.objects.exclude(id__in=coa).filter(federation=federation).distinct().count()
                # .exclude(belts=None).exclude(licenses=None).exclude(beltexam__athletes__user__in = exam_athlete).filter(licenses__branch=sinav.branch,licenses__status='Onaylandı').filter(belts__branch=sinav.branch,belts__status='Onaylandı').distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):

                modeldata = Athlete.objects.exclude(id__in=coa)[start:start + length]
                total = Athlete.objects.count()

    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        data = {
            'say': say,
            'pk': item.pk,
            'name': item.person.name + ' ' + item.person.surName,

        }
        beka.append(data)
        say += 1

    response = {
        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def musabaka_sanda_sporcu_ekle(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            compettion = Competition.objects.get(pk=request.POST.get('competition'))
            id = int(request.POST.get('id'))
            if request.POST.get('sanda'):
                if 0 == int(request.POST.get('sanda')):
                    sanda = 'Sanda'
                elif 1 == int(request.POST.get('sanda')):
                    sanda = 'Light Sanda'
                elif 2 == int(request.POST.get('sanda')):
                    sanda = 'Tuishou'

            if compettion.subBranch == EnumFields.SUBBRANCH.SANDA.value:
                if id == 1:
                    athlete = Athlete.objects.get(pk=request.POST.get('athleteId'))
                    athleteComps = SandaAthlete.objects.filter(athlete=athlete)
                    if TaoluAthlete.objects.filter(athlete=athlete):
                        if int(request.POST.get('sanda')) == 2:
                            sandaAthlete = SandaAthlete(
                                competition=compettion,
                                athlete=athlete,
                                competitiontype=sanda,
                                weight_category=SandaWeightCategory.objects.get(
                                    pk=int(request.POST.get('sandaWeight'))).categoryName
                            )
                            sandaAthlete.save()
                            mesaj = str(
                                compettion.name) + ' to the competition ' + sandaAthlete.athlete.person.name + ' ' + sandaAthlete.athlete.person.surName + 'added'
                            log = general_methods.logwrite(request, request.user, mesaj)
                            return JsonResponse({'status': 'Success', 'messages': 'Athlete Successfully Added'})
                        else:
                            return JsonResponse({'status': 'Warning',
                                                 'messages': 'Athletes registered in Taolu cannot be registered in Sanda.'})
                    else:
                        if athleteComps.count() > 1:
                            return JsonResponse(
                                {'status': 'Warning',
                                 'messages': 'It is not possible to register for more than two competitions.'})
                        elif athleteComps.count() == 1:
                            compCategory = SandaAthlete.objects.get(athlete=athlete).competitiontype
                            if (int(request.POST.get('sanda')) == 1 and compCategory == 'Tuishou') or (
                                    int(request.POST.get('sanda')) == 2 and compCategory == 'Light Sanda'):
                                sandaAthlete = SandaAthlete(
                                    competition=compettion,
                                    athlete=athlete,
                                    competitiontype=sanda,
                                    weight_category=SandaWeightCategory.objects.get(
                                        pk=int(request.POST.get('sandaWeight'))).categoryName
                                )
                                sandaAthlete.save()
                                mesaj = str(
                                    compettion.name) + ' to the competition ' + sandaAthlete.athlete.person.name + ' ' + sandaAthlete.athlete.person.surName + 'added'
                                log = general_methods.logwrite(request, request.user, mesaj)
                                return JsonResponse({'status': 'Success', 'messages': 'Athlete Successfully Added'})
                            else:
                                return JsonResponse(
                                    {'status': 'Warning',
                                     'messages': 'Registration is not possible in the selected category.'})

                        else:
                            sandaAthlete = SandaAthlete(
                                competition=compettion,
                                athlete=athlete,
                                competitiontype=sanda,
                                weight_category=SandaWeightCategory.objects.get(
                                    pk=int(request.POST.get('sandaWeight'))).categoryName
                            )
                            sandaAthlete.save()
                            mesaj = str(
                                compettion.name) + ' to the competition ' + sandaAthlete.athlete.person.name + ' ' + sandaAthlete.athlete.person.surName + 'added'
                            log = general_methods.logwrite(request, request.user, mesaj)
                            return JsonResponse({'status': 'Success', 'messages': 'Athlete Successfully Added'})
                elif id == 2:
                    coach = Coach.objects.get(pk=request.POST.get('coachId'))
                    if not SandaCoach.objects.filter(coach=coach):
                        sandaCoach = SandaCoach(
                            competition=compettion,
                            coach=coach,
                        )
                        sandaCoach.save()
                        mesaj = str(
                            compettion.name) + ' to the competition ' + sandaCoach.coach.person.name + ' ' + sandaCoach.coach.person.surName + 'added'
                        log = general_methods.logwrite(request, request.user, mesaj)
                        return JsonResponse({'status': 'Success', 'messages': 'Coach Successfully Added'})
                    else:
                        return JsonResponse({'status': 'Warning', 'messages': 'Coach already added.'})

                elif id == 3:

                    observer = Observer.objects.get(pk=request.POST.get('observerId'))
                    sandaObserver = SandaObserver(
                        competition=compettion,
                        observer=observer,
                    )
                    sandaObserver.save()
                    mesaj = str(
                        compettion.name) + ' to the competition ' + sandaObserver.observer.person.name + ' ' + sandaObserver.observer.person.surName + 'added'
                    log = general_methods.logwrite(request, request.user, mesaj)
                    return JsonResponse({'status': 'Success', 'messages': 'Observer Successfully Added'})
                elif id == 4:
                    officer = Officer.objects.get(pk=request.POST.get('officerId'))
                    if not SandaOfficer.objects.filter(officer=officer):

                        sandaOfficer = SandaOfficer(
                            competition=compettion,
                            officer=officer,
                        )
                        sandaOfficer.save()
                        mesaj = str(
                            compettion.name) + ' to the competition ' + sandaOfficer.officer.person.name + ' ' + sandaOfficer.officer.person.surName + 'added'
                        log = general_methods.logwrite(request, request.user, mesaj)
                        return JsonResponse({'status': 'Success', 'messages': 'Official Successfully Added'})
                    else:
                        return JsonResponse({'status': 'Warning', 'messages': 'Official already added.'})

                elif id == 5:
                    judge = Judge.objects.get(pk=request.POST.get('judgeId'))
                    if not SandaJudge.objects.filter(judge=judge):
                        if judge.category == 1 and SandaJudge.objects.filter(judge__federation__user=request.user).filter(
                                judge__category=1):
                            return JsonResponse({'status': 'Warning',
                                                 'messages': 'More than one referee cannot be registered.Please add a Candıdate judge'})
                        sandaJudge = SandaJudge(
                            competition=compettion,
                            judge=judge,
                        )
                        sandaJudge.save()
                        mesaj = str(
                            compettion.name) + ' to the competition ' + sandaJudge.judge.person.name + ' ' + sandaJudge.judge.person.surName + 'added'
                        log = general_methods.logwrite(request, request.user, mesaj)
                        return JsonResponse({'status': 'Success', 'messages': 'Referee Successfully Added'})
                    else:
                        return JsonResponse({'status': 'Warning', 'messages': 'Referee already added.'})

                elif id == 6:
                    federation = None
                    personId = int(request.POST.get('personId'))
                    name = request.POST.get('hotelRoom')
                    registerStartDate = request.POST.get('registerStartDate')
                    registerFinishDate = request.POST.get('registerFinishDate')
                    finishDate = datetime.strptime(registerFinishDate, "%Y-%m-%d").date()
                    startDate = datetime.strptime(registerStartDate, "%Y-%m-%d").date()
                    totalDay = finishDate - startDate
                    totalDay = totalDay.days
                    if name == 'SINGLE ROOM-81€':
                        price = totalDay * 81
                    else:
                        price = totalDay * 63
                    person = Person.objects.get(pk=personId)
                    if request.user.groups.filter(name='Admin'):
                        if Athlete.objects.filter(person=person):
                            federation = Athlete.objects.get(person=person).federation
                        elif Coach.objects.filter(person=person):
                            federation = Coach.objects.get(person=person).federation
                        elif Observer.objects.filter(person=person):
                            federation = Observer.objects.get(person=person).federation
                        elif Officer.objects.filter(person=person):
                            federation = Officer.objects.get(person=person).federation
                        elif Judge.objects.filter(person=person):
                            federation = Judge.objects.get(person=person).federation
                    elif request.user.groups.filter(name='Federation'):
                        federation = Federation.objects.get(user=request.user)

                    hotel = Hotel(
                        person=person, name=name, registerStartDate=registerStartDate,
                        registerFinishDate=registerFinishDate, federation=federation, totalDay=totalDay, price=price
                    )
                    hotel.save()

                    sandaHotel = SandaHotel(
                        hotel=hotel, competition=compettion
                    )
                    sandaHotel.save()

                    mesaj = ' Hotel registration has been made.'
                    log = general_methods.logwrite(request, request.user, mesaj)
                    return JsonResponse({'status': 'Success', 'messages': 'Hotel registration has been made.'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'The sub-category of the competition is not Sanda'})



        except Exception as e:

            traceback.print_exception()
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_sanda_weight_category(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    sandaWeightCategoryForm = SandaWeightCategoryForm()

    if request.method == 'POST':

        sandaWeightCategoryForm = SandaWeightCategoryForm(request.POST)
        if sandaWeightCategoryForm.is_valid():
            sandaWeightCategoryForm.save()
        else:
            messages.warning(request, 'Check Field')
    sandaWeightCategories = SandaWeightCategory.objects.all().order_by('-creationDate')
    return render(request, 'kategori/SandaWeightCategory.html',
                  {'sandaWeightCategoryForm': sandaWeightCategoryForm, 'sandaWeightCategories': sandaWeightCategories})


@login_required
def sanda_weight_category_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = SandaWeightCategory.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaWeightCategory.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def sanda_weight_category_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    weightCategory = SandaWeightCategory.objects.get(id=pk)
    sanda_weight_form = SandaWeightCategoryForm(request.POST or None, instance=weightCategory)
    if request.method == 'POST':
        if sanda_weight_form.is_valid():
            sanda_weight_form.save()

            messages.success(request, 'Successfully Update')
            return redirect('wushu:sanda-weight-category')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kategori/SandaWeightCategoryUpdate.html',
                  {'sanda_weight_form': sanda_weight_form})


@api_view(http_method_names=['POST'])
def get_weight_category(request):
    if request.POST:
        try:
            athleteId = request.POST.get('athleteId')
            sanda = int(request.POST.get('sanda'))
            athlete = Athlete.objects.get(pk=athleteId)
            ageGroup = ''
            if sanda == 2:
                if athlete.person.birthDate.year >= 1967 and athlete.person.birthDate.year <= 1981:
                    ageGroup = '41-55'
                elif athlete.person.birthDate.year >= 1982 and athlete.person.birthDate.year <= 2004:
                    ageGroup = '18-40'
                elif athlete.person.birthDate.year == 2005 or athlete.person.birthDate.year == 2006:
                    ageGroup = '16-17'
                elif athlete.person.birthDate.year == 2007 or athlete.person.birthDate.year == 2008:
                    ageGroup = '14-15'
                elif athlete.person.birthDate.year == 2009 or athlete.person.birthDate.year == 2010:
                    ageGroup = '12-13'
            else:
                if athlete.person.birthDate.year == 2015 or athlete.person.birthDate.year == 2016:
                    ageGroup = '6-7'
                elif athlete.person.birthDate.year == 2013 or athlete.person.birthDate.year == 2014:
                    ageGroup = '8-9'
                elif athlete.person.birthDate.year == 2011 or athlete.person.birthDate.year == 2012:
                    ageGroup = '10-11'
                elif athlete.person.birthDate.year == 2009 or athlete.person.birthDate.year == 2010:
                    ageGroup = '12-13'
                elif athlete.person.birthDate.year == 2008:
                    ageGroup = '14'
                elif athlete.person.birthDate.year == 2006 or athlete.person.birthDate.year == 2007:
                    ageGroup = '15-16'
                elif athlete.person.birthDate.year == 2004 or athlete.person.birthDate.year == 2005:
                    ageGroup = '17-18'
                elif athlete.person.birthDate.year >= 2001 and athlete.person.birthDate.year <= 2004:
                    ageGroup = '18-21'
                elif athlete.person.birthDate.year >= 1982 and athlete.person.birthDate.year <= 2000:
                    ageGroup = '22-40'

            gender = athlete.person.gender.lower()
            sandaWeightCategory = SandaWeightCategory.objects.filter(gender=gender).filter(ageGroup=ageGroup)

            dataSandaWeightCategory = SandaWeightCategorySerializer(sandaWeightCategory, many=True)
            responseData = dict()
            responseData['sandaWeightCategory'] = dataSandaWeightCategory.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
