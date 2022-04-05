from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

from wushu.models import Competition
from wushu.models.Athlete import Athlete
from wushu.models.Coach import Coach
from wushu.models.Level import Level
from wushu.services import general_methods
from wushu.models.EnumFields import EnumFields
from wushu.models.CategoryItem import CategoryItem

from datetime import date, datetime


@login_required
def return_athlete_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/sporcu.html')


@login_required
def return_referee_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/hakem.html')


@login_required
def return_coach_dashboard(request):
    perm = general_methods.control_access(request)
    #
    # if not perm:
    #     logout(request)
    #
    #     return redirect('accounts:login')
    competitions = Competition.objects.all().order_by('-startDate')
    athletes = Athlete.objects.filter(coach__user=request.user)
    return render(request, 'anasayfa/antrenor.html', {'application': competitions, 'athletes': athletes})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if not perm:
        logout(request)
        return redirect('accounts:login')
    # son eklenen 8 sporcuyu ekledik
    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender='Erkek').count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender='Kadın').count()
    total_athlate_last_month = Athlete.objects.exclude(user__date_joined__month=datetime.now().month).count()
    total_coachs = Coach.objects.all().count()
    total_brans_aikido = Athlete.objects.filter(licenses__branch='AIKIDO').count()
    total_brans_wushu = Athlete.objects.filter(licenses__branch='WUSHU').count()
    total_brans_wing_chun = Athlete.objects.filter(licenses__branch='WING CHUN').count()
    total_brans_budakadio = Athlete.objects.filter(licenses__branch='BUDAKADIO').count()
    total_brans_jeet_kune_do_kulelkavi = Athlete.objects.filter(licenses__branch='JEET KUNE DO KULELKAVIDO').count()
    competitions = Competition.objects.all().order_by('-startDate')
    return render(request, 'anasayfa/admin.html',
                  {
                      'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                      'total_athlete_gender_man': total_athlete_gender_man,
                      'total_athlete_gender_woman': total_athlete_gender_woman,
                      'total_athlate_last_month': total_athlate_last_month,
                      'total_brans_wushu': total_brans_wushu, 'total_brans_aikido': total_brans_aikido,
                      'total_brans_wing_chun': total_brans_wing_chun,
                      'total_brans_budakadio': total_brans_budakadio,
                      'total_brans_jeet_kune_do_kulelkavi': total_brans_jeet_kune_do_kulelkavi,
                      'application': competitions,
                  })


@login_required
def City_athlete_cout(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            athletecout = Athlete.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            coachcout = Coach.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()

            data = {
                'athlete': athletecout,
                'coach': coachcout,

            }
            return JsonResponse(data)
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})
#
#
