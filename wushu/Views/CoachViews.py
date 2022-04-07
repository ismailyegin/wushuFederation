from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

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

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        coach = Federation.objects.get(user=request.user)
        if person_form.is_valid():

            person = person_form.save(commit=False)
            person.save()

            coach = Coach(
                person=person, federation=coach
            )
            coach.save()

            mesaj = str(coach.person.name) + ' ' + str(coach.person.surName) + ' coach registered'
            log = general_methods.logwrite(request, request.user, mesaj)

            messages.success(request, 'Coach Registered Successfully.')

            return redirect('wushu:coaches')

        else:
            for x in person_form.errors.as_data():
                messages.warning(request, person_form.errors[x][0])

    return render(request, 'antrenor/antrenor-ekle.html', {'person_form': person_form, })


@login_required
def return_coaches(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coaches = Coach.objects.none()

    if user.groups.filter(name='Federation'):
        coaches = Coach.objects.filter(federation__user=request.user)

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        coaches = Coach.objects.all()

    return render(request, 'antrenor/antrenorler.html',
                  {'coaches': coaches})


@login_required
def updatecoaches(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = Coach.objects.get(pk=pk)
    person = Person.objects.get(pk=coach.person.pk)

    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    say = 0

    if request.method == 'POST':

        if person_form.is_valid():

            person_form.save()
            messages.success(request, 'Coach Successfully Updated.')

            mesaj = 'The coach named ' + str(person.name) + ' ' + str(person.surName) + ' has been updated'
            log = general_methods.logwrite(request, request.user, mesaj)

            return redirect('wushu:update-coaches', pk=pk)

        else:

            messages.warning(request, 'Check Fields')

    return render(request, 'antrenor/antrenorDuzenle.html',
                  {'person_form': person_form, 'coach': coach, 'say': say, })