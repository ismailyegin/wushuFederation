from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render

from wushu.Forms.AthleteForm import AthleteForm
from wushu.Forms.JudgeForm import JudgeForm
from wushu.Forms.PersonForm import PersonForm
from wushu.models import Athlete, Person, Federation, Coach, Observer, Officer, Judge
from wushu.services import general_methods


def addFederationGroup(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    athlete_form = AthleteForm()
    judge_form = JudgeForm()

    if request.method == 'POST':
        if request.POST.get('submit') == 'athlete':
            person_form = PersonForm(request.POST, request.FILES)
            athlete_form = AthleteForm(request.POST, request.FILES)
            federation = Federation.objects.get(user=request.user)
            if person_form.is_valid() and athlete_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                ekgEeg = athlete_form.save(commit=False)

                athlete = Athlete(
                    person=person, federation=federation, eeg=ekgEeg.eeg, ekg=ekgEeg.ekg
                )
                athlete.save()

                mesaj = str(athlete.person.name) + ' ' + str(athlete.person.surName) + ' athlete registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Athlete Registered Successfully.')

                return redirect('wushu:sporcular')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if request.POST.get('submit') == 'coach':
            if request.method == 'POST':
                person_form = PersonForm(request.POST, request.FILES)
                federation = Federation.objects.get(user=request.user)
                if person_form.is_valid():

                    person = person_form.save(commit=False)
                    person.save()

                    coach = Coach(
                        person=person, federation=federation
                    )
                    coach.save()

                    mesaj = str(coach.person.name) + ' ' + str(coach.person.surName) + ' coach registered'
                    log = general_methods.logwrite(request, request.user, mesaj)

                    messages.success(request, 'Coach Registered Successfully.')

                    return redirect('wushu:coaches')

                else:
                    for x in person_form.errors.as_data():
                        messages.warning(request, person_form.errors[x][0])

        if request.POST.get('submit') == 'observer':
            person_form = PersonForm(request.POST, request.FILES)
            federation = Federation.objects.get(user=request.user)
            if person_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                observer = Observer(
                    person=person, federation=federation
                )
                observer.save()

                mesaj = str(observer.person.name) + ' ' + str(observer.person.surName) + ' observer registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Observer Registered Successfully.')

                return redirect('wushu:observers')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if request.POST.get('submit') == 'officer':
            person_form = PersonForm(request.POST, request.FILES)
            federation = Federation.objects.get(user=request.user)
            if person_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                officer = Officer(
                    person=person, federation=federation
                )
                officer.save()

                mesaj = str(officer.person.name) + ' ' + str(officer.person.surName) + ' officer registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Officer Registered Successfully.')

                return redirect('wushu:officers')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if request.POST.get('submit') == 'judge':
            person_form = PersonForm(request.POST, request.FILES)
            judge_form = JudgeForm(request.POST, request.FILES)
            federation = Federation.objects.get(user=request.user)
            if person_form.is_valid() and judge_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                judge_form = judge_form.save(commit=False)

                judge = Judge(
                    person=person, federation=federation, category=judge_form.category
                )
                judge.save()

                mesaj = str(judge.person.name) + ' ' + str(judge.person.surName) + ' judge registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Judge Registered Successfully.')

                return redirect('wushu:judges')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

    return render(request, 'federasyon/federasyon-grup-ekle.html',
                  {'person_form': person_form,
                   'athlete_form': athlete_form,
                   'judge_form': judge_form,
                   })
