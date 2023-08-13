from django.http import HttpResponse
from django.template import loader


def PSN(request):
    template = loader.get_template('platforms.html')
    return HttpResponse(template.render())
