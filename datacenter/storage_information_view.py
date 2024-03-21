from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    # Программируем здесь

    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        non_closed_visits.append({
                'who_entered': visit.passcard,
                'entered_at': visit.entered_at,
                'duration': visit.get_duration(),
            })
        
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
