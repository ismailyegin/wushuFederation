from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.shortcuts import redirect, render

from wushu.Forms.CommunicationForm import CommunicationForm
from wushu.Forms.LicenseForm import LicenseForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.UserForm import UserForm
from wushu.Forms.UserSearchForm import UserSearchForm
from wushu.models import Coach, Athlete
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

    license_form = LicenseForm(request.POST, request.FILES or None)

    # lisan ekleme son alani bu alanlar sadece form bileselerinin sisteme gidebilmesi icin post ile gelen veride gene ayni şekilde  karşılama ve kaydetme islemi yapilacak

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        license_form = LicenseForm(request.POST, request.FILES or None)
        coach = Coach.objects.get(user=request.user)
        if person_form.is_valid() and license_form.is_valid() and communication_form.is_valid():
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

            # lisans kaydedildi  kakydetmeden id degeri alamayacagi icin önce kaydedip sonra ekleme islemi yaptık
            license = license_form.save()
            athlete.save()
            athlete.licenses.add(license)


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
                  {'user_form': user_form, 'person_form': person_form, 'license_form': license_form,
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
        brans = request.POST.get('branch')

        if user_form.is_valid():
            firstName = user_form.cleaned_data.get('first_name')
            lastName = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')
            if not (firstName or lastName or email or brans):

                if user.groups.filter(name='Antrenor'):
                    athletes = Athlete.objects.filter(coach__user=request.user).distinct()
                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    athletes = Athlete.objects.all()
            elif firstName or lastName or email or brans:
                query = Q()

                if firstName:
                    query &= Q(user__first_name__icontains=firstName)
                if lastName:
                    query &= Q(user__last_name__icontains=lastName)
                if email:
                    query &= Q(user__email__icontains=email)
                if brans:
                    query &= Q(licenses__branch=brans, licenses__status='Onaylandı')

                if user.groups.filter(name='Antrenor'):
                    athletes = Athlete.objects.filter(coach__user=request.user).filter(query).distinct()

                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    athletes = Athlete.objects.filter(query).distinct()

    return render(request, 'sporcu/sporcular.html',
                  {'athletes': athletes, 'user_form': user_form})
