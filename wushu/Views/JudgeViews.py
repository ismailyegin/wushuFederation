from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

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

    if request.method == 'POST':
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

    return render(request, 'hakem/hakem-ekle.html', {'person_form': person_form, 'judge_form': judge_form, })


@login_required
def return_judges(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    judges = Judge.objects.none()

    if user.groups.filter(name='Federation'):
        judges = Judge.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        judges = Judge.objects.all()

    return render(request, 'hakem/hakemler.html',
                  {'judges': judges})


@login_required
def updatejudges(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    judge = Judge.objects.get(pk=pk)
    person = Person.objects.get(pk=judge.person.pk)

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    judge_form = JudgeForm(request.POST or None, request.FILES or None, instance=judge)
    say = 0

    if request.method == 'POST':

        if person_form.is_valid() and judge_form.is_valid():

            person_form.save()
            judge_form.save()
            messages.success(request, 'Judge Successfully Updated.')

            mesaj = 'The judge named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
            log = general_methods.logwrite(request, request.user, mesaj)

            return redirect('wushu:update-judges', pk=pk)

        else:

            messages.warning(request, 'Check Fields')

    return render(request, 'hakem/hakemDuzenle.html',
                  {'person_form': person_form, 'judge': judge, 'say': say, 'judge_form': judge_form, })
