from django.http import HttpResponse
from django.template import loader
from .playstation import PlayStation
from .forms import PsnSignInForm

def PSN(request):
    psn = PlayStation()
    template = loader.get_template('platforms.html')
    psn_form = PsnSignInForm(request.POST)
    psn_form.fields['npsso'].error_messages = {'required': ''}

    if psn_form.is_valid():
        npsso = psn_form.cleaned_data['npsso']
        context = {
             'psn': psn,
             'psn_form': psn_form,
             'npsso': npsso
        }
    else:
        context = {
          'psn': psn,
          'psn_form' : psn_form
        }

    return HttpResponse(template.render(context, request))
