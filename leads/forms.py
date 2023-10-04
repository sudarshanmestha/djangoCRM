from django import forms
from .models import Lead, FollowUp
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from leads.models import Agent


User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'category',
            'description',
            'phone_number',
            'email',
        )
 
 
class AssignAgentModelForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentModelForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents
        
        
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
           


class LeadCategoryUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
        
class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file'
        )
            
# class LeadForm(forms.Form):
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#     age = forms.IntegerField(min_value=0)