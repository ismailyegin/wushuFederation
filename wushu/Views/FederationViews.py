from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from wushu.Forms.AthleteForm import AthleteForm
from wushu.Forms.JudgeForm import JudgeForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.UserForm import UserForm
from wushu.models import Athlete, Person, Federation, Coach, Observer, Officer, Judge, Competition, SandaAthlete, \
    TaoluAthlete, SandaCoach, SandaObserver, SandaOfficer, SandaJudge, TaoluCoach, TaoluObserver, TaoluOfficer, \
    TaoluJudge
from wushu.services import general_methods


@login_required
def return_add_federation(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    user_form = UserForm()

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        user_form = UserForm(request.POST, request.FILES)

        if person_form.is_valid() and user_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            password = User.objects.make_random_password()
            user.set_password(password)
            user.is_active = user_form.cleaned_data['is_active']
            user.save()

            person = person_form.save(commit=False)
            person.name = user.first_name
            person.surName = user.last_name
            person.save()

            federasyon = Federation(
                person=person, user=user
            )
            federasyon.save()

            mesaj = str(federasyon.person.name) + ' ' + str(federasyon.person.surName) + ' athlete registered'
            log = general_methods.logwrite(request, request.user, mesaj)

            messages.success(request, 'Federation Registered Successfully.')

            return redirect('wushu:federations')

        else:
            for x in person_form.errors.as_data():
                messages.warning(request, person_form.errors[x][0])

    return render(request, 'federasyon/federasyon-ekle.html', {'person_form': person_form, 'user_form': user_form, })


@login_required
def return_federations(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    user_form = UserForm()
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        user_form = UserForm(request.POST, request.FILES)

        if person_form.is_valid() and user_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            password = User.objects.make_random_password()
            user.set_password(password)
            # user.is_active = user_form.cleaned_data['is_active']
            user.save()

            person = person_form.save(commit=False)
            person.name = user.first_name
            person.surName = user.last_name
            person.save()

            federasyon = Federation(
                person=person, user=user
            )
            federasyon.save()

            mesaj = str(federasyon.person.name) + ' ' + str(federasyon.person.surName) + ' athlete registered'
            log = general_methods.logwrite(request, request.user, mesaj)

            messages.success(request, 'Federation Registered Successfully.')

            return redirect('wushu:federations')

        else:
            for x in person_form.errors.as_data():
                messages.warning(request, person_form.errors[x][0])

    federations = Federation.objects.all()

    return render(request, 'federasyon/federasyonlar.html',
                  {'federations': federations, 'person_form': person_form, 'user_form': user_form, })


@login_required
def update_federation(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    federation = Federation.objects.get(pk=pk)
    person = Person.objects.get(pk=federation.person.pk)
    user = User.objects.get(pk=federation.user.pk)

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    user_form = UserForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':

        if person_form.is_valid() and user_form.is_valid():

            person_form.save()
            userUpdate = user_form.save(commit=False)
            userUpdate.username = user_form.cleaned_data['email']
            userUpdate.first_name = user_form.cleaned_data['first_name']
            userUpdate.last_name = user_form.cleaned_data['last_name']
            userUpdate.email = userUpdate.username
            # userUpdate.is_active = user_form.cleaned_data['is_active']
            userUpdate.save()

            messages.success(request, 'Federation Successfully Updated.')

            mesaj = 'The federation named ' + str(user.first_name) + ' ' + str(user.last_name) + ' has been updated'
            log = general_methods.logwrite(request, request.user, mesaj)

            return redirect('wushu:update-federations', pk=pk)

        else:

            messages.warning(request, 'Check Fields')

    return render(request, 'federasyon/federasyonDuzenle.html',
                  {'person_form': person_form, 'user_form': user_form, })


@login_required
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


@login_required
def delete_federation(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            federation = Federation.objects.get(pk=pk)
            if Athlete.objects.filter(federation=federation):
                for athlete in Athlete.objects.filter(federation=federation):
                    athlete.delete()
            if Coach.objects.filter(federation=federation):
                for coach in Coach.objects.filter(federation=federation):
                    coach.delete()
            if Observer.objects.filter(federation=federation):
                for observer in Observer.objects.filter(federation=federation):
                    observer.delete()
            if Officer.objects.filter(federation=federation):
                for officer in Officer.objects.filter(federation=federation):
                    officer.delete()
            if Judge.objects.filter(federation=federation):
                for judge in Judge.objects.filter(federation=federation):
                    judge.delete()
            user = federation.user
            user.delete()

            federation.delete()

            log = 'The federation named ' + str(federation.user.first_name) + ' ' + str(
                federation.user.last_name) + " has been deleted"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except Federation.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def registration_list(request):
    perm = general_methods.control_access_antrenor(request)
    user = request.user
    if not perm:
        logout(request)
        return redirect('accounts:login')

    athletes = None
    coaches = None
    observers = None
    officers = None
    judges = None
    sandaAthlete = SandaAthlete.objects.all()
    sandaCoach = SandaCoach.objects.all()
    sandaObserver = SandaObserver.objects.all()
    sandaOfficer = SandaOfficer.objects.all()
    sandaJudge = SandaJudge.objects.all()

    taoluAthlete = TaoluAthlete.objects.all()
    taoluCoach = TaoluCoach.objects.all()
    taoluObserver = TaoluObserver.objects.all()
    taoluOfficer = TaoluOfficer.objects.all()
    taoluJudge = TaoluJudge.objects.all()

    countSandaCoach = sandaAthlete.all().count()


    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        athletes = Athlete.objects.all()
        coaches = Coach.objects.all()
        observers = Observer.objects.all()
        officers = Officer.objects.all()
        judges = Judge.objects.all()

    elif user.groups.filter(name='Federation'):
        athletes = Athlete.objects.filter(federation__user=request.user)
        coaches = Coach.objects.filter(federation__user=request.user)
        observers = Observer.objects.filter(federation__user=request.user)
        officers = Officer.objects.filter(federation__user=request.user)
        judges = Judge.objects.filter(federation__user=request.user)

    return render(request, 'federasyon/kayit-listele.html',
                  {'athletes': athletes, 'coaches': coaches, 'observers': observers, 'officers': officers,
                   'judges': judges, 'sandaAthlete': sandaAthlete, 'sandaCoach': sandaCoach,
                   'sandaObserver': sandaObserver, 'sandaOfficer': sandaOfficer, 'sandaJudge': sandaJudge,
                   'taoluAthlete': taoluAthlete, 'taoluCoach': taoluCoach, 'taoluObserver': taoluObserver,
                   'taoluOfficer': taoluOfficer, 'taoluJudge': taoluJudge, 'countSandaCoach': countSandaCoach, })
