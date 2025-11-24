from django.shortcuts import render
from .models import Track, Profile
from .forms import TrackForm, ProfileForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login

#chatbot
from django.http import JsonResponse
from .chatbot import chatbot
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def track_list(request):
    tracks = Track.objects.filter(user=request.user).all().order_by('-date')
    context = {'tracks': tracks}
    return render(request, 'track_list.html', context)

@login_required
def track_create(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.user = request.user
            track.save()
            return redirect('track_list')
    else:
        form = TrackForm()
    return render(request, 'track_form.html', {'form': form})

@login_required
def track_edit(request, pk):
    track = get_object_or_404(Track, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
            form.save()
            return redirect('track_list')
    else:
        form = TrackForm(instance=track)
    return render(request, 'track_form.html', {'form': form})

@login_required
def track_delete(request, pk):
    track=get_object_or_404(Track,pk=pk,user=request.user)
    if request.method=='POST':
        track.delete()
        return redirect('track_list')
    return render(request,'track_confirm_delete.html',{'track':track})

@login_required
def profile_view(request):
    try:
        profile=Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('profile_create')
    return render(request,'profile_view.html',{'profile':profile})

@login_required
def profile_create(request):
    if request.method=='POST':
        form=ProfileForm(request.POST)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('profile_view')
    else:
        form=ProfileForm()
    return render(request,'profile_form.html',{'form':form})

@login_required
def profile_edit(request):
    profile=Profile.objects.get(user=request.user,pk=request.user.profile.pk)
    if request.method =='POST':
        form=ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
            form.save()
            return redirect('profile_view')
    else:
        form=ProfileForm(instance=profile)
    return render(request,'profile_form.html',{'form':form})

@login_required
def profile_delete(request):
    profile=get_object_or_404(Profile,user=request.user,pk=request.user.profile.pk)
    if request.method=='POST':
        profile.delete()
        return redirect('index')
    return render(request,'profile_confirm_delete.html',{'profile':profile})

def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('index')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})



@login_required
def charts_view(request):
    user = request.user

    logs = Track.objects.filter(user=user).order_by("date")

    # Scatter plot: (x: day count, y: weight)
    scatter_points = []
    for i, log in enumerate(logs, start=1):
        scatter_points.append({"x": i, "y": log.weight})

    # Radar chart data
    muscle_groups = {}
    for key, label in Track.MUSCLE_GROUP_CHOICES:
        muscle_groups[label] = logs.filter(muscle_group=key).count()

    context = {
        "scatter": scatter_points,
        "muscle_labels": list(muscle_groups.keys()),
        "muscle_counts": list(muscle_groups.values()),
    }
    return render(request, "charts.html", context)

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    user_message = data.get("message")

    if not user_message:
        return JsonResponse({"error": "Message is required"}, status=400)

    response = chatbot.invoke(
        {"question": user_message},
        config={"configurable": {"session_id": "user123"}}
    )

    return JsonResponse({"reply": response})

def chatbot_page(request):
    return render(request, "chat_page.html")