from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from wushu.services import general_methods


def login(request):
    if request.user.is_authenticated is True:
        return redirect('wushu:admin')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            log = general_methods.logwrite(request, request.user, " Giris yapti")
            if user.groups.all():
                if user.groups.all()[0].name == 'Admin':
                    return redirect('wushu:admin')

                elif user.groups.all()[0].name == 'Federation':
                    return redirect('wushu:federasyon')

                else:
                    return redirect('accounts:logout')
            else:
                messages.add_message(request, messages.SUCCESS, 'Grup Bilgisi Bulunmamaktadır.')
                return render(request, 'registration/login.html')

        else:
            messages.add_message(request, messages.SUCCESS, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')

def pagelogout(request):
    log = general_methods.logwrite(request, request.user, " Çıkış yapti")
    logout(request)
    return redirect('accounts:login')


