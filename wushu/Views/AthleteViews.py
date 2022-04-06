from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.shortcuts import redirect, render

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
    user_form = UserForm()
    person_form = PersonForm()

    communication_form = CommunicationForm()
    # lisan ekleme son alani bu alanlar sadece form bileselerinin sisteme gidebilmesi icin post ile gelen veride gene ayni şekilde  karşılama ve kaydetme islemi yapilacak

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        coach = Federation.objects.get(user=request.user)
        if person_form.is_valid() and communication_form.is_valid() and user_form:
            user = User()
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user.username = email
            user.email = email

            group = Group.objects.get(name='Sporcu')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.is_active = False
            user.save()

            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            athlete = Athlete(
                user=user, person=person, communication=communication, coach=coach,
            )
            athlete.save()


            # subject, from_email, to = 'WUSHU - Sporcu Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'ik@oxityazilim.com', user.email
            # text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            # html_content = '<p> <strong>Site adresi: </strong> <a href="https://www.twf.gov.tr/"></a>https://www.twf.gov.tr/</p>'
            # html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            # html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            mesaj = str(user.get_full_name()) + ' Sporcusunu kaydetti'
            log = general_methods.logwrite(request, request.user, mesaj)

            messages.success(request, 'Sporcu Başarıyla Kayıt Edilmiştir.')

            return redirect('wushu:sporcular')

        else:
            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'sporcu/sporcu-ekle.html',
                  {'user_form': user_form, 'person_form': person_form,
                   'communication_form': communication_form

                   })


@login_required
def return_athletes(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    user_form = UserSearchForm()

    athletes = Athlete.objects.none()

    if user.groups.filter(name='Antrenor'):

        athletes = Athlete.objects.filter(coach__user=request.user)

    if request.method == 'POST':

        user_form = UserSearchForm(request.POST)
        if user_form.is_valid():
            firstName = user_form.cleaned_data.get('first_name')
            lastName = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')
            if not (firstName or lastName or email):

                if user.groups.filter(name='Antrenor'):
                    athletes = Athlete.objects.filter(coach__user=request.user).distinct()
                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    athletes = Athlete.objects.all()
            elif firstName or lastName or email:
                query = Q()

                if firstName:
                    query &= Q(user__first_name__icontains=firstName)
                if lastName:
                    query &= Q(user__last_name__icontains=lastName)
                if email:
                    query &= Q(user__email__icontains=email)
                if user.groups.filter(name='Antrenor'):
                    athletes = Athlete.objects.filter(coach__user=request.user).filter(query).distinct()

                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    athletes = Athlete.objects.filter(query).distinct()

    return render(request, 'sporcu/sporcular.html',
                  {'athletes': athletes, 'user_form': user_form})


@login_required
def updateathletes(request, pk):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Athlete.objects.get(pk=pk)
    user = User.objects.get(pk=athlete.user.pk)
    person = Person.objects.get(pk=athlete.person.pk)
    communication = Communication.objects.get(pk=athlete.communication.pk)

    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)
    say = 0

    if request.method == 'POST':

        if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()
            person_form.save()
            communication_form.save()

            messages.success(request, 'Sporcu Başarıyla Güncellenmiştir.')

            mesaj = str(user.get_full_name()) + ' Sporcu güncellendi'
            log = general_methods.logwrite(request, request.user, mesaj)

            return redirect('wushu:update-athletes', pk=pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/sporcuDuzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'athlete': athlete, 'say': say})
