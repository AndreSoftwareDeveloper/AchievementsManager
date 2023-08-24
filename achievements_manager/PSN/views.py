from django.http import HttpResponse
from django.template import loader
from .playstation import PlayStation
from .forms import PsnSignInForm

def PSN(request):
    psn = PlayStation()
    template = loader.get_template('platforms.html')
    psn_form = PsnSignInForm()
    context = {
        'psn': psn,
        'PsnSignInForm' : PsnSignInForm
    }

    return HttpResponse(template.render(context, request))
