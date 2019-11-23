from django.views.generic import TemplateView
from management.forms import VisitVisitorModelForm


class NewVisitAndVisitorView(TemplateView):
    template_name = 'new_visit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VisitVisitorModelForm()
        return context
