from django.views.generic import TemplateView
from management.forms import VisitVisitorModelForm, VisitorModelForm, VisitModelForm
from django.views.generic.edit import FormView


class NewVisitAndVisitorView(FormView):
    template_name = 'new_visit.html'
    form_class = VisitVisitorModelForm
    success_url = '/'

    def form_valid(self, form):
        visit_and_visitor_cleaned_data = form.cleaned_data

        visit_details = visit_and_visitor_cleaned_data['visit']
        visit_details['visitor'] = visit_and_visitor_cleaned_data['visitor']

        # Calling API
        return super(NewVisitAndVisitorView, self).form_valid(form)
