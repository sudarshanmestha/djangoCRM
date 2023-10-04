from typing import Any
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent, Category
from .forms import ( LeadModelForm, CustomUserCreationForm, 
AssignAgentModelForm, LeadCategoryUpdateModelForm, FollowUpModelForm) #LeadForm
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin



class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")
    
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    # queryset = Lead.objects.all()
    context_object_name = 'leads'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:               #If the user is an organizer, the queryset will be filtered to show only leads associated with their organization.
            queryset = Lead.objects.filter(organisation= user.userprofile, agent__isnull=False)
        else:                               #If the user is an agent, the queryset will be further filtered to only show leads assigned to that agent.
            queryset = Lead.objects.filter(organisation= user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset  
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context  
    


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = 'lead'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation= user.userprofile)
        else:    
            queryset = Lead.objects.filter(organisation= user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset  

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        lead = form.save(commit = False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
                  subject="A lead has been created", 
                  message="Go to the site to see the new lead", 
                  from_email="test@test.com", 
                  recipient_list=["test2@test.com"]
                  )
        return super(LeadCreateView,self).form_valid(form)
    
class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation= user.userprofile) 
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    

class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
        
    
class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView): 
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentModelForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request" : self.request
        }) 
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]        #grab the selected agent data
        lead = Lead.objects.get(id=self.kwargs["pk"]) #grabs pk of lead id
        lead.agent = agent                ## assign the selected agent to the lead      
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    
    
class CategoryListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html' 
    context_object_name = 'category_list'
    

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_organisor:               #If the user is an organizer, the queryset will be filtered to show only leads associated with their organization.
            queryset = Lead.objects.filter(
                organisation= user.userprofile, 
                )
        else:                               #If the user is an agent, the queryset will be further filtered to only show leads assigned to that agent.
            queryset = Lead.objects.filter(
                organisation= user.agent.organisation, 
                )
            
        context.update({
            "unassigned_lead_count" : queryset.filter(category__isnull = True).count()
            
        })
        return context
    
    
     
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:               #If the user is an organizer, the queryset will be filtered to show only leads associated with their organization.
            queryset = Category.objects.filter(
                organisation= user.userprofile, 
                )
        else:                               #If the user is an agent, the queryset will be further filtered to only show leads assigned to that agent.
            queryset = Category.objects.filter(
                organisation= user.agent.organisation, 
                )
        return queryset       
    
    
class CategoryDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html' 
    context_object_name = 'category'
    

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:               #If the user is an organizer, the queryset will be filtered to show only leads associated with their organization.
            queryset = Category.objects.filter(
                organisation= user.userprofile, 
                )
        else:                               #If the user is an agent, the queryset will be further filtered to only show leads assigned to that agent.
            queryset = Category.objects.filter(
                organisation= user.agent.organisation, 
                )
        return queryset       
        
    
class LeadCategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView): 
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateModelForm
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation= user.userprofile)
        else:    
            queryset = Lead.objects.filter(organisation= user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset  
    
    def get_success_url(self):
        return reverse("leads:lead-detail" ,kwargs={"pk": self.get_object().id })   
    
    
class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)
