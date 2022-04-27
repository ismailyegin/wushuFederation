import os
import shutil
from itertools import chain
from pathlib import Path

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from oxiterp.settings.base import BASE_DIR
from wushu.models import SandaAthlete, SandaCoach, SandaObserver, SandaOfficer, SandaJudge, TaoluAthlete, TaoluCoach, \
    TaoluObserver, TaoluOfficer, TaoluJudge, Person
from wushu.services import general_methods


@login_required
def profile_image(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if not (os.path.isdir('media/profile_image')):
        os.makedirs(os.path.join('media','profile_image'))

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/profile_image')
    try:
        for item in Person.objects.all()[:5]:
            if item.profileImage:
                extension='.'+item.profileImage.name.split('.')[1]
                dst = os.path.join(BASE_DIR, 'media/profile_image/' + item.pasaport+extension)
                if not Path(dst).is_file():
                    shutil.copyfile(item.profileImage.path, dst)
        zip_file=None
        is_file=Path(os.path.join(BASE_DIR, 'media/profile_image.zip'))
        if not is_file.is_file():
            zip_file=shutil.make_archive(MEDIA_ROOT, 'zip', MEDIA_ROOT)
        else:
            zip_file=os.path.join(BASE_DIR, 'media/profile_image.zip')
        # file=os.path.join(BASE_DIR, 'media/profile_image.zip')
        # html='<a href="/media/profile_image.zip" download>Download the file by clicking here</a>'
        if Path(zip_file).is_file():
            html='You can download profile pictures of registered people by<a href="/media/profile_image.zip" download> clicking here</a>'
        else:
            html='file could not be created'

        return render(request, 'anasayfa/download.html', {'html': html})
    except Exception as e:
        print(e)
        html = "<html><body>file could not be created</body></html>"
        return HttpResponse(html)
