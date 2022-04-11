from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from wushu.Forms.OfficerFederationForm import OfficerFederationForm
from wushu.Forms.PersonForm import PersonForm
from wushu.models import Federation, Person, Officer
from wushu.services import general_methods


@login_required
def return_add_officer(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    officer_federation_form = OfficerFederationForm()
    user = request.user

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            officer_federation_form = OfficerFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and officer_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = officer_federation_form.cleaned_data['federation']

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

        if user.groups.filter(name='Federation'):
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

    return render(request, 'resmiGörevli/resmiGörevli-ekle.html',
                  {'person_form': person_form, 'officer_federation_form': officer_federation_form, })


@login_required
def return_officers(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    officers = Officer.objects.none()

    if user.groups.filter(name='Federation'):
        officers = Officer.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        officers = Officer.objects.all()

    return render(request, 'resmiGörevli/resmiGörevliler.html',
                  {'officers': officers})


@login_required
def updateofficers(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    officer = Officer.objects.get(pk=pk)
    person = Person.objects.get(pk=officer.person.pk)
    user = request.user

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    officer_federation_form = OfficerFederationForm(request.POST or None, request.FILES or None, instance=officer)
    say = 0

    if request.method == 'POST':

        if user.groups.filter(name__in=['Yonetim', 'Admin']):

            if person_form.is_valid() and officer_federation_form.is_valid():

                person_form.save()
                officer_federation_form.save()

                messages.success(request, 'Officer Successfully Updated.')

                mesaj = 'The officer named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-officers', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

        if user.groups.filter(name='Federation'):
            if person_form.is_valid():

                person_form.save()
                messages.success(request, 'Officer Successfully Updated.')

                mesaj = 'The officer named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-officers', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

    return render(request, 'resmiGörevli/resmiGörevliDuzenle.html',
                  {'person_form': person_form, 'officer': officer, 'say': say,
                   'officer_federation_form': officer_federation_form, })


@login_required
def delete_officer(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Officer.objects.get(pk=pk)
            log = 'The officer named ' + str(obj.person.name) + ' ' + str(obj.person.surName) + " has been deleted"
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except Officer.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
