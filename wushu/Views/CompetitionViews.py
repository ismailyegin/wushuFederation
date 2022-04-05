import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from wushu.Forms.CompetitionForm import CompetitionForm
from wushu.Forms.DisabledCompetitionForm import DisabledCompetitionForm
from wushu.Forms.competitonSearchForm import CompetitionSearchForm
from wushu.models import Competition, YearsSandaCategory, TaoluCategory, YearsTaoluCategory, Coach, Athlete, EnumFields, \
    TaoluAthlete, SandaAthlete
from wushu.services import general_methods


@login_required
def return_competitions(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    comquery = CompetitionSearchForm()
    competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                             registerFinishDate__gte=timezone.now())
    competitions = Competition.objects.none()

    if request.method == 'POST':
        comquery = CompetitionSearchForm(request.POST)
        name = request.POST.get('name')
        if name:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            competitions = Competition.objects.filter(query).order_by('-startDate').distinct()
        else:
            competitions = Competition.objects.all().order_by('-startDate')
    return render(request, 'musabaka/musabakalar.html', {'competitions': competitions,
                                                         'application': competition,
                                                         'query': comquery})


@login_required
def musabaka_sanda(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    categoryitemm = YearsSandaCategory.objects.all().order_by('-creationDate')
    return render(request, 'musabaka/musabaka-SandaSporcusec.html',
                  {'competition': musabaka, 'categoryitemm': categoryitemm})


@login_required
def musabaka_taolu(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    yearscategory = YearsTaoluCategory.objects.all()
    category = TaoluCategory.objects.all()

    return render(request, 'musabaka/musabaka-taolu-sporcu-sec.html',
                  {'competition': musabaka,
                   'yearscategory': yearscategory,
                   'category': category})


@login_required
def return_sporcu_sec_taolu(request):
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
        if user.groups.filter(name='Antrenor'):
            coach = Coach.objects.get(user=request.user)
            modeldata = Athlete.objects.exclude(id__in=coa).filter(coach=coach).distinct()
            for item in modeldata:
                print(item)
            total = modeldata.count()
        elif user.groups.filter(name__in=['Yonetim', 'Admin']):

            modeldata = Athlete.objects.exclude(id__in=coa).distinct()

            total = modeldata.count()
    else:
        if search:
            if user.groups.filter(name='Antrenor'):
                coach = Coach.objects.get(user=request.user)

                modeldata = Athlete.objects.exclude(id__in=coa).filter(coach=coach).filter(
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
            if user.groups.filter(name='Antrenor'):
                coach = Coach.objects.get(user=request.user)
                modeldata = Athlete.objects.exclude(id__in=coa).filter(coach=coach).distinct()[
                            start:start + length]
                total = Athlete.objects.exclude(id__in=coa).filter(coach=coach).distinct().count()
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
            'name': item.user.first_name + ' ' + item.user.last_name,

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
            category = TaoluCategory.objects.get(pk=request.POST.get('category'))
            athlete = Athlete.objects.get(pk=request.POST.get('athlete'))
            years = YearsTaoluCategory.objects.get(pk=request.POST.get('years'))
            # YearsTaoluCategory
            if compettion.subBranch == EnumFields.SUBBRANCH.TAOLU.value:
                taoluAthlete = TaoluAthlete(
                    competition=compettion,
                    category=category,
                    athlete=athlete,
                    years=years,
                )
                taoluAthlete.save()
                mesaj = str(
                    compettion.name) + ' müsabakasına ' + taoluAthlete.athlete.user.get_full_name() + '   eklendi'
                log = general_methods.logwrite(request, request.user, mesaj)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Müsabanın alt katagorisi Sanda degil'})



        except Exception as e:

            traceback.print_exception()
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_duzenle(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    categori = None
    athletes = None

    user = request.user
    if request.user.groups.filter(name='Antrenor'):
        competition_form = DisabledCompetitionForm(request.POST or None, instance=musabaka)
        coach = Coach.objects.get(user=request.user)

        if musabaka.subBranch == EnumFields.SANDA.value:
            athletes = SandaAthlete.objects.filter(athlete__coach=coach,
                                                   competition=musabaka.pk).distinct()
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            athletes = TaoluAthlete.objects.filter(athlete__coach=coach,
                                                   competition=musabaka).distinct()
    elif request.user.groups.filter(name__in=['Yonetim', 'Admin']):
        competition_form = CompetitionForm(request.POST or None, instance=musabaka)
        if musabaka.subBranch == EnumFields.SANDA.value:
            athletes = SandaAthlete.objects.filter(competition=musabaka)
        elif musabaka.subBranch == EnumFields.TAOLU.value:
            athletes = TaoluAthlete.objects.filter(competition=musabaka)

    if request.method == 'POST':
        if competition_form.is_valid():
            if request.user.groups.filter(name__in=['Yonetim', 'Admin']):
                competition = competition_form.save(commit=False)
                competition.save()
                mesaj = str(competition.name) + ' müsabaka güncellendi   '
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Müsabaka Başarıyla Güncellenmiştir.')
            return redirect('wushu:musabaka-duzenle', pk=pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-duzenle.html',
                  {'competition_form': competition_form, 'competition': musabaka, 'athletes': athletes,
                   'categori': categori})


@login_required
def musabaka_sporcu_sil_taolu(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = TaoluAthlete.objects.get(pk=pk)
            athlete.delete()
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
            athlete = SandaAthlete.objects.get(pk=pk)
            athlete.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_sporcu_sec_sanda(request):
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
        if user.groups.filter(name='Antrenor'):
            coach = Coach.objects.get(user=request.user)
            modeldata = Athlete.objects.exclude(id__in=coa).filter(coach=coach).distinct()
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
            if user.groups.filter(name='Antrenor'):

                coach = Coach.objects.get(user=request.user)
                modeldata = Athlete.objects.exclude(id__in=coa).filter(coach=coach).filter(
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
            if user.groups.filter(name='Antrenor'):

                coach = Coach.objects.get(user=request.user)
                modeldata = Athlete.objects.exclude(id__in=coa).filter(coach=coach).distinct()[
                            start:start + length]
                total = Athlete.objects.exclude(id__in=coa).filter(coach=coach).distinct().count()
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
            'name': item.user.first_name + ' ' + item.user.last_name,

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
            athlete = Athlete.objects.get(pk=request.POST.get('athlete'))
            if request.POST.get('sanda'):
                if 0 == int(request.POST.get('sanda')):
                    sanda = 'Sanda'
                elif 1 == int(request.POST.get('sanda')):
                    sanda = 'Light Sanda'
                elif 2 == int(request.POST.get('sanda')):
                    sanda = 'Tuishou'

            if compettion.subBranch == EnumFields.SUBBRANCH.SANDA.value:
                sandaAthlete = SandaAthlete(
                    competition=compettion,
                    athlete=athlete,
                    competitiontype=sanda,
                    athlete_yas_category=YearsSandaCategory.objects.get(pk=int(request.POST.get('yas'))).categoryYear
                )
                sandaAthlete.save()
                mesaj = str(compettion.name) + ' müsabakasına ' + sandaAthlete.athlete.user.get_full_name() + 'eklendi'
                log = general_methods.logwrite(request, request.user, mesaj)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Müsabanın alt katagorisi Sanda degil'})



        except Exception as e:

            traceback.print_exception()
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
