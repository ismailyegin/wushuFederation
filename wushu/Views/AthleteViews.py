from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from wushu.Forms.AthleteFederationForm import AthleteFederationForm
from wushu.Forms.AthleteForm import AthleteForm
from wushu.Forms.CommunicationForm import CommunicationForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.SandaYearsCategoryForm import SandaYearsCategoryForm
from wushu.Forms.TaoluCategoryForm import TaoluCategoryForm
from wushu.Forms.UserForm import UserForm
from wushu.Forms.UserSearchForm import UserSearchForm
from wushu.Forms.YearsTaoluCategoryForm import YearsTaoluCategoryForm
from wushu.models import Federation, Athlete, Person, Communication, TaoluCategory, CategoryItem, YearsTaoluCategory, \
    YearsSandaCategory
from wushu.services import general_methods


@login_required
def return_add_athlete(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    athlete_form = AthleteForm()
    athlete_federation_form = AthleteFederationForm()
    user = request.user

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        athlete_form = AthleteForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            athlete_federation_form = AthleteFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and athlete_form.is_valid() and athlete_federation_form.is_valid():

                person = person_form.save()

                athlete = Athlete(
                    person=person, federation=athlete_federation_form.cleaned_data['federation'],
                    eeg=athlete_form.cleaned_data['eeg'].name, ekg=athlete_form.cleaned_data['ekg'].name
                )
                athlete.save()

                mesaj = str(athlete.person.name) + ' ' + str(athlete.person.surName) + ' athlete registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Athlete Registered Successfully.')

                return redirect('wushu:sporcular')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if user.groups.filter(name='Federation'):

            if person_form.is_valid() and athlete_form.is_valid():

                person = person_form.save(commit=False)
                person.save()
                federation = Federation.objects.get(user=request.user)

                athlete = athlete_form.save(commit=False)

                athlete = Athlete(
                    person=person, federation=federation, eeg=athlete.eeg, ekg=athlete.ekg
                )
                athlete.save()

                mesaj = str(athlete.person.name) + ' ' + str(athlete.person.surName) + ' athlete registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Athlete Registered Successfully.')

                return redirect('wushu:sporcular')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

    return render(request, 'sporcu/sporcu-ekle.html', {'person_form': person_form, 'athlete_form': athlete_form,
                                                       'athlete_federation_form': athlete_federation_form, })


@login_required
def return_athletes(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    athletes = Athlete.objects.none()
    person_form = PersonForm()
    athlete_form = AthleteForm()
    athlete_federation_form = AthleteFederationForm()
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        athlete_form = AthleteForm(request.POST, request.FILES)
        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            athlete_federation_form = AthleteFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and athlete_form.is_valid() and athlete_federation_form.is_valid():

                person = person_form.save()

                athlete = Athlete(
                    person=person, federation=athlete_federation_form.cleaned_data['federation'],
                    eeg=athlete_form.cleaned_data['eeg'].name, ekg=athlete_form.cleaned_data['ekg'].name
                )
                athlete.save()

                mesaj = str(athlete.person.name) + ' ' + str(athlete.person.surName) + ' athlete registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Athlete Registered Successfully.')

                return redirect('wushu:sporcular')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if user.groups.filter(name='Federation'):

            if person_form.is_valid() and athlete_form.is_valid():

                person = person_form.save(commit=False)
                person.save()
                federation = Federation.objects.get(user=request.user)

                athlete = athlete_form.save(commit=False)

                athlete = Athlete(
                    person=person, federation=federation, eeg=athlete.eeg, ekg=athlete.ekg
                )
                athlete.save()

                mesaj = str(athlete.person.name) + ' ' + str(athlete.person.surName) + ' athlete registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Athlete Registered Successfully.')

                return redirect('wushu:sporcular')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])
    if user.groups.filter(name='Federation'):
        athletes = Athlete.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        athletes = Athlete.objects.all()

    return render(request, 'sporcu/sporcular.html',
                  {'athletes': athletes,'person_form': person_form, 'athlete_form': athlete_form,
                                                       'athlete_federation_form': athlete_federation_form,})


@login_required
def updateathletes(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Athlete.objects.get(pk=pk)
    person = Person.objects.get(pk=athlete.person.pk)
    user = request.user

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    athlete_form = AthleteForm(request.POST or None, request.FILES or None, instance=athlete)
    athlete_federation_form = AthleteFederationForm(request.POST or None, request.FILES or None, instance=athlete)
    say = 0

    if request.method == 'POST':

        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            athlete_federation_form = AthleteFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and athlete_form.is_valid() and athlete_federation_form.is_valid():

                person_form.save()
                athlete.ekg = athlete_form.cleaned_data['ekg'].name
                athlete.eeg = athlete_form.cleaned_data['eeg'].name
                athlete.federation = athlete_federation_form.cleaned_data['federation']
                athlete.save()

                messages.success(request, 'Athlete Successfully Updated.')

                mesaj = 'The athlete named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-athletes', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

        if user.groups.filter(name='Federation'):

            if person_form.is_valid() and athlete_form.is_valid():

                person_form.save()
                athlete_form.save()

                messages.success(request, 'Athlete Successfully Updated.')

                mesaj = 'The athlete named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-athletes', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

    return render(request, 'sporcu/sporcuDuzenle.html',
                  {'person_form': person_form, 'athlete': athlete, 'say': say, 'athlete_form': athlete_form,
                   'athlete_federation_form': athlete_federation_form, })


@login_required
def delete_athlete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Athlete.objects.get(pk=pk)
            log = 'The athlete named ' + str(obj.person.name) + ' ' + str(obj.person.surName) + " has been deleted"
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except Athlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_taolu(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    taolu_form = TaoluCategoryForm()

    if request.method == 'POST':

        taolu_form = TaoluCategoryForm(request.POST)
        if taolu_form.is_valid():
            taolu_form.save()
        else:
            messages.warning(request, 'You Checked the Fields')
    categoryitem = TaoluCategory.objects.all().order_by('-creationDate')
    return render(request, 'kategori/TaoluCategori.html',
                  {'taolu_form': taolu_form, 'categoryitem': categoryitem})


@login_required
def categoryTaoluDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = TaoluCategory.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def categoryTaoluUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    taolu = TaoluCategory.objects.get(id=pk)
    taolu_form = TaoluCategoryForm(request.POST or None, instance=taolu)
    if request.method == 'POST':
        if taolu_form.is_valid():
            taolu_form.save()

            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('wushu:taolu-katagori')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kategori/TaoluKategoriDüzenle.html',
                  {'taolu_form': taolu_form})


@login_required
def return_taolu_years(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    taoluyears_form = YearsTaoluCategoryForm()

    if request.method == 'POST':
        taoluyears_form = YearsTaoluCategoryForm(request.POST)
        if taoluyears_form.is_valid():
            taoluyears_form.save()
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitemm = YearsTaoluCategory.objects.all().order_by('-creationDate')
    return render(request, 'kategori/YearsTaoluCategory.html',
                  {'taoluyears_form': taoluyears_form, 'categoryitemm': categoryitemm})


@login_required
def categoryTaoluyearsDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = YearsTaoluCategory.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def categoryTaoluyearsUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    taoluyears = YearsTaoluCategory.objects.get(id=pk)
    taoluyears_form = YearsTaoluCategoryForm(request.POST or None, instance=taoluyears)
    if request.method == 'POST':
        if taoluyears_form.is_valid():
            taoluyears_form.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('wushu:yas-taolu-katagori')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kategori/YearsTaoluCategoryDüzenle.html',
                  {'taoluyears_form': taoluyears_form})


@login_required
def return_sanda_years(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    sandayears_form = SandaYearsCategoryForm()
    if request.method == 'POST':
        sandayears_form = SandaYearsCategoryForm(request.POST)
        if sandayears_form.is_valid():
            sandayears_form.save()
            messages.success(request, 'Başarıyla Kayıt Edildi.')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitemm = YearsSandaCategory.objects.all().order_by('-creationDate')
    return render(request, 'kategori/sandaYearsCategory.html',
                  {'sandayears_form': sandayears_form, 'categoryitemm': categoryitemm})


@login_required
def categorySandayearsDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = YearsSandaCategory.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def categorySandayearsUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    sandayears = YearsSandaCategory.objects.get(id=pk)
    sandayears_form = SandaYearsCategoryForm(request.POST or None, instance=sandayears)
    if request.method == 'POST':
        if sandayears_form.is_valid():
            sandayears_form.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('wushu:return_sanda_years')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kategori/yearsSandaCategoryDuzenle.html',
                  {'sandayears_form': sandayears_form})
