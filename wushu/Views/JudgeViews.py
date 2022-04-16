from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from wushu.Forms.JudgeFederationForm import JudgeFederationForm
from wushu.Forms.JudgeForm import JudgeForm
from wushu.Forms.PersonForm import PersonForm
from wushu.models import Federation, Person, Judge
from wushu.services import general_methods


@login_required
def return_add_judge(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    person_form = PersonForm()
    judge_form = JudgeForm()
    judge_federation_form = JudgeFederationForm()
    user = request.user

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        judge_form = JudgeForm(request.POST, request.FILES)

        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            judge_federation_form = JudgeFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and judge_form.is_valid() and judge_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                category = judge_form.cleaned_data['category']

                federation = judge_federation_form.cleaned_data['federation']

                judge = Judge(
                    person=person, federation=federation, category=category
                )
                judge.save()

                mesaj = str(judge.person.name) + ' ' + str(judge.person.surName) + ' judge registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Referee Registered Successfully.')

                return redirect('wushu:judges')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if user.groups.filter(name='Federation'):
            federation = Federation.objects.get(user=request.user)
            if person_form.is_valid() and judge_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                category = judge_form.cleaned_data['category']

                judge = Judge(
                    person=person, federation=federation, category=category
                )
                judge.save()

                mesaj = str(judge.person.name) + ' ' + str(judge.person.surName) + ' judge registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Referee Registered Successfully.')

                return redirect('wushu:judges')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

    return render(request, 'hakem/hakem-ekle.html', {'person_form': person_form, 'judge_form': judge_form,
                                                     'judge_federation_form': judge_federation_form, })


@login_required
def return_judges(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    judges = Judge.objects.none()
    person_form = PersonForm()
    judge_form = JudgeForm()
    judge_federation_form = JudgeFederationForm()
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        judge_form = JudgeForm(request.POST, request.FILES)

        if user.groups.filter(name__in=['Yonetim', 'Admin']):
            judge_federation_form = JudgeFederationForm(request.POST, request.FILES)
            if person_form.is_valid() and judge_form.is_valid() and judge_federation_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                category = judge_form.cleaned_data['category']

                federation = judge_federation_form.cleaned_data['federation']

                judge = Judge(
                    person=person, federation=federation, category=category
                )
                judge.save()
                judge.weight = request.POST['weight']
                judge.height = request.POST['height']
                judge.pantSize = request.POST['pantSize']
                judge.shirtSize = request.POST['shirtSize']

                judge.save()

                mesaj = str(judge.person.name) + ' ' + str(judge.person.surName) + ' judge registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Referee Registered Successfully.')

                return redirect('wushu:judges')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

        if user.groups.filter(name='Federation'):
            federation = Federation.objects.get(user=request.user)
            if person_form.is_valid() and judge_form.is_valid():

                person = person_form.save(commit=False)
                person.save()

                category = judge_form.cleaned_data['category']

                judge = Judge(
                    person=person, federation=federation, category=category
                )
                judge.save()
                judge.weight = request.POST['weight']
                judge.height = request.POST['height']
                judge.pantSize = request.POST['pantSize']
                judge.shirtSize = request.POST['shirtSize']

                judge.save()

                mesaj = str(judge.person.name) + ' ' + str(judge.person.surName) + ' judge registered'
                log = general_methods.logwrite(request, request.user, mesaj)

                messages.success(request, 'Referee Registered Successfully.')

                return redirect('wushu:judges')

            else:
                for x in person_form.errors.as_data():
                    messages.warning(request, person_form.errors[x][0])

    if user.groups.filter(name='Federation'):
        judges = Judge.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        judges = Judge.objects.all()

    return render(request, 'hakem/hakemler.html',
                  {'judges': judges, 'person_form': person_form, 'judge_form': judge_form,
                   'judge_federation_form': judge_federation_form})


@login_required
def updatejudges(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    judge = Judge.objects.get(pk=pk)
    person = Person.objects.get(pk=judge.person.pk)
    user = request.user

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    judge_form = JudgeForm(request.POST or None, request.FILES or None, instance=judge)
    judge_federation_form = JudgeFederationForm(request.POST or None, request.FILES or None, instance=judge)

    say = 0

    if request.method == 'POST':
        if user.groups.filter(name__in=['Yonetim', 'Admin']):

            if person_form.is_valid() and judge_form.is_valid() and judge_federation_form.is_valid():

                person_form.save()
                judge_form.save()
                judge_federation_form.save()

                if judge_form.cleaned_data['category'] == 1:
                    judge.weight = request.POST['weight']
                    judge.height = request.POST['height']
                    judge.pantSize = request.POST['pantSize']
                    judge.shirtSize = request.POST['shirtSize']
                else:
                    judge.is_national = None
                    judge.weight = None
                    judge.height = None
                    judge.pantSize = None
                    judge.shirtSize = None
                judge.save()

                messages.success(request, 'Referee Successfully Updated.')

                mesaj = 'The judge named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-judges', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

        if user.groups.filter(name='Federation'):

            if person_form.is_valid() and judge_form.is_valid():

                person_form.save()
                judge_form.save()
                if judge_form.cleaned_data['category'] == 1:
                    judge.weight = request.POST['weight']
                    judge.height = request.POST['height']
                    judge.pantSize = request.POST['pantSize']
                    judge.shirtSize = request.POST['shirtSize']
                else:
                    judge.is_national = None
                    judge.weight = None
                    judge.height = None
                    judge.pantSize = None
                    judge.shirtSize = None
                judge.save()
                messages.success(request, 'Referee Successfully Updated.')

                mesaj = 'The judge named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
                log = general_methods.logwrite(request, request.user, mesaj)

                return redirect('wushu:update-judges', pk=pk)

            else:

                messages.warning(request, 'Check Fields')

    return render(request, 'hakem/hakemDuzenle.html',
                  {'person_form': person_form, 'judge': judge, 'say': say, 'judge_form': judge_form,
                   'judge_federation_form': judge_federation_form, })


@login_required
def delete_judge(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Judge.objects.get(pk=pk)
            log = 'The judge named ' + str(obj.person.name) + ' ' + str(obj.person.surName) + " has been deleted"
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except Judge.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
