from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from wushu.Forms.ObserverFederationForm import ObserverFederationForm
from wushu.Forms.PersonForm import PersonForm
from wushu.models import Federation, Person, Observer
from wushu.services import general_methods


@login_required
def return_add_observer(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    observer_federation_form = ObserverFederationForm()
    user = request.user

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            observer_federation_form = ObserverFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and observer_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = observer_federation_form.cleaned_data['federation']

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

        if user.groups.filter(name='Federation'):

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

    return render(request, 'gozlemci/gozlemci-ekle.html',
                  {'person_form': person_form, 'observer_federation_form': observer_federation_form, })


@login_required
def return_observers(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    observers = Observer.objects.none()
    person_form = PersonForm()
    observer_federation_form = ObserverFederationForm()
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            observer_federation_form = ObserverFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and observer_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                federation = observer_federation_form.cleaned_data['federation']

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

        if user.groups.filter(name='Federation'):

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

    if user.groups.filter(name='Federation'):
        observers = Observer.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        observers = Observer.objects.all()

    return render(request, 'gozlemci/gozlemciler.html',
                  {'observers': observers, 'person_form': person_form,
                   'observer_federation_form': observer_federation_form, })


@login_required
def updateobservers(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    observer = Observer.objects.get(pk=pk)
    person = Person.objects.get(pk=observer.person.pk)
    user = request.user

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    observer_federation_form = ObserverFederationForm(request.POST or None, request.FILES or None, instance=observer)
    say = 0

    if request.method == 'POST':

        if user.groups.filter(name__in=['Yonetim', 'Admin']):

            if person_form.is_valid() and observer_federation_form.is_valid():

                person_form.save()
                observer_federation_form.save()

                messages.success(request, 'Observer Successfully Updated.')

                mesaj = 'The observer named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-observers', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

        if user.groups.filter(name='Federation'):

            if person_form.is_valid():

                person_form.save()
                messages.success(request, 'Observer Successfully Updated.')

                mesaj = 'The observer named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-observers', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

    return render(request, 'gozlemci/gozlemciDuzenle.html',
                  {'person_form': person_form, 'observer': observer, 'say': say,
                   'observer_federation_form': observer_federation_form, })


@login_required
def delete_observer(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Observer.objects.get(pk=pk)
            log = 'The observer named ' + str(obj.person.name) + ' ' + str(obj.person.surName) + " has been deleted"
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except Observer.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
