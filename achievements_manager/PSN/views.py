from django.http import HttpResponse
from django.template import loader
from .playstation import PlayStation


def PSN(request):
    psn_achievements = PlayStation()
    template = loader.get_template('platforms.html')
    context = {
        'psn_achievements': psn_achievements
    }

    return HttpResponse(template.render(context, request))
