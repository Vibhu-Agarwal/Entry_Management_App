from api.permissions import IsHostOrLoggedOutMixin
from django.views.generic import TemplateView
from management.forms import VisitVisitorModelForm, VisitorModelForm, VisitModelForm
from django.views.generic.edit import FormView


class NewVisitAndVisitorView(IsHostOrLoggedOutMixin, FormView):
    template_name = 'new_visit.html'
    success_url = '/'

    def get_user(self):
        user = self.request.user
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
        return user

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return VisitModelForm
        else:
            return VisitVisitorModelForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            visit_data = form.cleaned_data
            visit_data['visitor'] = self.get_user()

            # Calling API
            print(visit_data)
        else:
            visit_and_visitor_cleaned_data = form.cleaned_data

            visit_details = visit_and_visitor_cleaned_data['visit']
            visit_details['visitor'] = visit_and_visitor_cleaned_data['visitor']

            # Calling API
            print(visit_details)

        return super(NewVisitAndVisitorView, self).form_valid(form)
