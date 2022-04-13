from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from wushu.models import Competition, Coach, Observer, Officer, Judge
from wushu.models.Athlete import Athlete
from wushu.models.Federation import Federation
from wushu.services import general_methods

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
def return_federation_dashboard(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)

        return redirect('accounts:login')
    competitions = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                             registerFinishDate__gte=timezone.now())
    athletes = Athlete.objects.filter(federation__user=request.user)
    coaches = Coach.objects.filter(federation__user=request.user)
    observers = Observer.objects.filter(federation__user=request.user)
    officers = Officer.objects.filter(federation__user=request.user)
    judges = Judge.objects.filter(federation__user=request.user)
    return render(request, 'anasayfa/federasyon.html',
                  {'application': competitions, 'athletes': athletes, 'coaches': coaches,
                   'observers': observers, 'officers': officers, 'judges': judges, })


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')
    # son eklenen 8 sporcuyu ekledik
    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender='Erkek').count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender='Kadın').count()
    total_coachs = Coach.objects.all().count()

    competitions = Competition.objects.all().order_by('-startDate')
    return render(request, 'anasayfa/admin.html',
                  {
                      'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                      'total_athlete_gender_man': total_athlete_gender_man,
                      'total_athlete_gender_woman': total_athlete_gender_woman,
                      'application': competitions,
                  })
