from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from wushu.Forms.competitonSearchForm import CompetitionSearchForm
from wushu.models import Competition
from wushu.services import general_methods


@login_required
def return_competitions(request):
    perm = general_methods.control_access_antrenor(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    comquery = CompetitionSearchForm()
    competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                             registerFinishDate__gte=timezone.now())
    competitions = Competition.objects.none()

    if request.method == 'POST':
        comquery = CompetitionSearchForm(request.POST)
        name = request.POST.get('name')
        if name:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            competitions = Competition.objects.filter(query).order_by('-startDate').distinct()
        else:
            competitions = Competition.objects.all().order_by('-startDate')
    return render(request, 'musabaka/musabakalar.html', {'competitions': competitions,
                                                         'application': competition,
                                                         'query': comquery})
