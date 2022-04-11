from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from wushu.Forms.CoachFederationForm import CoachFederationForm
from wushu.Forms.PersonForm import PersonForm
from wushu.models import Federation, Coach, Person
from wushu.services import general_methods


@login_required
def return_add_coach(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    coach_federation_form = CoachFederationForm()
    user = request.user

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            coach_federation_form = CoachFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and coach_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = coach_federation_form.cleaned_data['federation']

                coach = Coach(
                    person=person, federation=federation
                )
                coach.save()

                mesaj = str(coach.person.name) + ' ' + str(coach.person.surName) + ' coach registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Coach Registered Successfully.')

                return redirect('wushu:add-coach')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if user.groups.filter(name='Federation'):

            if person_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = Federation.objects.get(user=request.user)

                coach = Coach(
                    person=person, federation=federation
                )
                coach.save()

                mesaj = str(coach.person.name) + ' ' + str(coach.person.surName) + ' coach registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Coach Registered Successfully.')

                return redirect('wushu:add-coach')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

    return render(request, 'antrenor/antrenor-ekle.html', {'person_form': person_form, 'coach_federation_form': coach_federation_form})


@login_required
def return_coaches(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coaches = Coach.objects.none()
    person_form = PersonForm()
    coach_federation_form = CoachFederationForm()
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            coach_federation_form = CoachFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and coach_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = coach_federation_form.cleaned_data['federation']

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

        if user.groups.filter(name='Federation'):

            if person_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = Federation.objects.get(user=request.user)

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

    if user.groups.filter(name='Federation'):
        coaches = Coach.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        coaches = Coach.objects.all()

    return render(request, 'antrenor/antrenorler.html',
                  {'coaches': coaches,'person_form': person_form, 'coach_federation_form': coach_federation_form})


@login_required
def updatecoaches(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = Coach.objects.get(pk=pk)
    person = Person.objects.get(pk=coach.person.pk)
    user = request.user

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    coach_federation_form = CoachFederationForm(request.POST or None, request.FILES or None, instance=coach)
    say = 0

    if request.method == 'POST':

        if user.groups.filter(name__in=['Yonetim', 'Admin']):

            if person_form.is_valid() and coach_federation_form.is_valid():

                person_form.save()
                coach_federation_form.save()

                messages.success(request, 'Coach Successfully Updated.')

                mesaj = 'The coach named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-coaches', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

        if user.groups.filter(name='Federation'):
            if person_form.is_valid():

                person_form.save()

                messages.success(request, 'Coach Successfully Updated.')

                mesaj = 'The coach named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-coaches', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

    return render(request, 'antrenor/antrenorDuzenle.html',
                  {'person_form': person_form, 'coach': coach, 'say': say, 'coach_federation_form': coach_federation_form, })


@login_required
def delete_coach(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Coach.objects.get(pk=pk)
            log = 'The coach named ' + str(obj.person.name) + ' ' + str(obj.person.surName) + " has been deleted"
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
