from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .forms import RegisterForm, ProfileForm, LeagueForm, ChallengeForm
from django.urls import reverse
from .models import Profile, League, Challenge
import random


class IndexView(TemplateView):
    template_name = "accounts/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.order_by('balance')[::-1][:25]
        context['profiles'] = profiles
        return context


class RegisterView(View):
    template_name = 'accounts/signup.html'
    def get(self, request):
        register_form = RegisterForm()
        profile_form = ProfileForm()
        args = {'profile_form': profile_form, 'register_form': register_form}
        return render(request, self.template_name, args)

    def post(self, request):
        profile_form = ProfileForm(request.POST)
        register_form = RegisterForm(request.POST)
        if register_form.is_valid() and profile_form.is_valid():
            print("hi")
            temp = register_form.save(commit=False)
            temp.profile = profile_form.save()
            temp.save()
            return redirect(reverse("index"))
        return render(request, "accounts/index.html")


class LeagueFormView(View):
    template_name = 'accounts/league_form.html'

    def get(self, request):
        league_form = LeagueForm
        args = {'league_form': league_form}
        return render(request, self.template_name, args)

    def post(self, request):
        league_form = LeagueForm(request.POST)
        if league_form.is_valid():
            league_form.save()
            return redirect(reverse("index"))
        return render(request, "accounts/index.html")


class LeagueView(TemplateView):
    template_name = 'accounts/league.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league_name = self.kwargs['name']
        league_participants = League.objects.get(name=league_name).participants.order_by('balance')[::-1]
        context['league'] = league_participants
        return context


class ChallengeFormView(View):
    template_name = 'accounts/challenge_form.html'

    def get(self, request):
        challenge_form = ChallengeForm
        args = {'challenge_form': challenge_form}
        return render(request, self.template_name, args)

    def post(self, request):
        challenge_form = ChallengeForm(request.POST)
        if challenge_form.is_valid():
            challenge_form.save()
            return redirect(reverse("index"))
        return render(request, "accounts/index.html")


class ChallengeSelectorView(View):
    template_name = 'accounts/challenge_selector.html'

    def get(self, request):
        challenge_form = ChallengeForm
        args = {'challenge_form': challenge_form}
        return render(request, self.template_name, args)

    def post(self, request):
        challenge_form = ChallengeForm(request.POST)
        challenge_type = challenge_form.data.get("challenge_type")
        possible_challenges = list(Challenge.objects.filter(challenge_type=challenge_type))
        challenge = random.choice(possible_challenges)
        user = self.request.user
        profile = user.profile
        profile.current_challenge = challenge
        profile.save()
        return redirect(reverse("profile"))

class ProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        user = self.request.user
        profile = user.profile
        leagues = League.objects.filter(participants__username=profile.username)
        args = {'profile': profile, 'leagues': leagues}
        return render(request, self.template_name, args)

    def post(self, request):
        challenge = request.POST.get("challenge")
        if challenge=="accept":
            user = self.request.user
            profile = user.profile
            profile.balance += profile.current_challenge.point_value
            profile.current_challenge = None
            profile.save()
        else:
            user = self.request.user
            profile = user.profile
            profile.current_challenge = None
            profile.save()
        return redirect(reverse("profile"))