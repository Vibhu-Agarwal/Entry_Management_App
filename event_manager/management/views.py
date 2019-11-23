from django.views.generic import TemplateView
from management.forms import VisitVisitorModelForm
from django.views.generic.edit import FormView


class NewVisitAndVisitorView(FormView):
    template_name = 'new_visit.html'
    form_class = VisitVisitorModelForm
    success_url = '/'

    def form_valid(self, form):
        import pdb; pdb.set_trace()
        return super(NewVisitAndVisitorView, self).form_valid(form)
