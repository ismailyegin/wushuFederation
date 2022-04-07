from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.shortcuts import redirect, render

from wushu.Forms.AthleteForm import AthleteForm
from wushu.Forms.CommunicationForm import CommunicationForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.UserForm import UserForm
from wushu.Forms.UserSearchForm import UserSearchForm
from wushu.models import Federation, Athlete, Person, Communication
from wushu.services import general_methods


@login_required
def return_add_athlete(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    athlete_form = AthleteForm()

    if request.method == 'POST':
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

    return render(request, 'sporcu/sporcu-ekle.html',
                  {'person_form': person_form,
                   'athlete_form': athlete_form,
                   })


@login_required
def return_athletes(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    athletes = Athlete.objects.none()

    if user.groups.filter(name='Federation'):
        athletes = Athlete.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        athletes = Athlete.objects.all()

    return render(request, 'sporcu/sporcular.html',
                  {'athletes': athletes})


@login_required
def updateathletes(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Athlete.objects.get(pk=pk)
    person = Person.objects.get(pk=athlete.person.pk)

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    athlete_form = AthleteForm(request.POST or None, request.FILES or None, instance=athlete)
    say = 0

    if request.method == 'POST':

        if person_form.is_valid() and athlete_form.is_valid():

            person_form.save()
            athlete_form.save(commit=False)
            athlete.eeg = athlete_form.cleaned_data['eeg']
            athlete.eeg = athlete_form.cleaned_data['ekg']
            athlete.save()
            messages.success(request, 'Athlete Successfully Updated.')

            mesaj = 'The athlete named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
            log = general_methods.logwrite(request, request.user, mesaj)

            return redirect('wushu:update-athletes', pk=pk)

        else:

            messages.warning(request, 'Check Fields')

    return render(request, 'sporcu/sporcuDuzenle.html',
                  {'person_form': person_form, 'athlete': athlete, 'say': say, 'athlete_form': athlete_form, })
