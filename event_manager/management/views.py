from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from management.forms import VisitVisitorModelForm, VisitorModelForm, VisitModelForm
from django.views.generic.edit import FormView
from django.forms.utils import ErrorDict


class NewVisitAndVisitorView(FormView):
    template_name = 'new_visit.html'
    form_class = VisitVisitorModelForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        visit_and_visitor_raw_data = dict(form.data)

        map_field_name = {
            'email': 'visitor-email',
            'first_name': 'visitor-first_name',
            'last_name': 'visitor-last_name',
            'phone_number': 'visitor-phone_number',
            'in_time': 'visit-in_time',
            'purpose': 'visit-purpose',
            'host': 'visit-host'
        }

        visitor_email = visit_and_visitor_raw_data['visitor-email'][0]
        visitor_first_name = visit_and_visitor_raw_data['visitor-first_name'][0]
        visitor_last_name = visit_and_visitor_raw_data['visitor-last_name'][0]
        visitor_phone_number = visit_and_visitor_raw_data['visitor-phone_number'][0]
        visit_in_time = visit_and_visitor_raw_data['visit-in_time'][0]
        visit_purpose = visit_and_visitor_raw_data['visit-purpose'][0]
        visit_host = visit_and_visitor_raw_data['visit-host'][0]

        visitor_data = {
            'email': visitor_email,
            'first_name': visitor_first_name,
            'last_name': visitor_last_name,
            'phone_number': visitor_phone_number,
        }

        form_errors = {}
        visitor_form = VisitorModelForm(data=visitor_data)
        if not visitor_form.is_valid():
            for field, field_error in visitor_form.errors.items():
                form_errors[map_field_name[field]] = field_error
        else:
            visitor = visitor_form.save()
            visit_details = {
                'in_time': visit_in_time,
                'purpose': visit_purpose,
                'host': visit_host,
            }
            return HttpResponseRedirect(self.get_success_url())

        form_errors = ErrorDict(form_errors)
        form._errors = form_errors

        return self.form_invalid(form)
