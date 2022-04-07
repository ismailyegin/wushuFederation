from datetime import datetime

from wushu.models.Athlete import Athlete
from wushu.models.Federation import Federation
from wushu.models.Logs import Logs
from wushu.models.Menu import Menu
from wushu.models.MenuAdmin import MenuAdmin
from wushu.models.MenuAthlete import MenuAthlete
from wushu.models.MenuCoach import MenuCoach
from wushu.models.Person import Person


def getMenu(request):
    menus = Menu.objects.all()
    return {'menus': menus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all().order_by("sorting")
    return {'adminmenus': adminmenus}


def getAthleteMenu(request):
    athletemenus = MenuAthlete.objects.all()
    return {'athletemenus': athletemenus}


def getCoachMenu(request):
    coachmenus = MenuCoach.objects.all().order_by("sorting")
    return {'coachmenus': coachmenus}


def getProfileImage(request):
    if (request.user.id):
        current_user = request.user

        if current_user.groups.filter(name='Sporcu').exists():
            athlete = Athlete.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Federation').exists():
            athlete = Federation.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        # elif current_user.groups.filter(name='Hakem').exists():
        #     athlete = Judge.objects.get(user=current_user)
        #     person = Person.objects.get(id=athlete.person.id)
        #
        # elif current_user.groups.filter(name='Yonetim').exists():
        #     athlete = DirectoryMember.objects.get(user=current_user)
        #     person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"

        else:
            person = None

        return {'person': person}

    return {}


def control_access(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin":
        is_exist = True

    return is_exist


def control_access_antrenor(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin" or group.name=="Federation":
        is_exist = True

    return is_exist


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logwrite(request, user, log):
    try:
        logs = Logs(
            user=user,
            subject=log,
            ip=get_client_ip(request)
        )
        logs.save()

    except Exception as e:
        f = open("log.txt", "a")
        log = "[" + datetime.today().strftime('%d-%m-%Y %H:%M') + "]  lag kaydetme hata   \n "
        f.write(log)
        f.close()

    return log
