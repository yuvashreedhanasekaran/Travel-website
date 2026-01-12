from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Booking   # only model


# ---------- LANDING ----------
def landing(request):
    return render(request, 'landing.html')


# ---------- REGISTER ----------
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # 👈 auto login
            return redirect('/home/')     # 👈 direct URL (safe)
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# ---------- LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- HOME ----------
@login_required
def home(request):
    return render(request, 'home.html')


# ---------- BOOKING ----------
@login_required
def booking_form(request):
    if request.method == "POST":
        Booking.objects.create(
            user=request.user,
            name=request.POST["name"],
            age=request.POST["age"],
            from_place=request.POST["from_place"],
            to_place=request.POST["to_place"],
            duration=request.POST["duration"],
            budget=request.POST["budget"],
        )
        return render(request, "booking_success.html")

    return render(request, "form_page.html")

from django.shortcuts import get_object_or_404

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "booking_list.html", {"bookings": bookings})


@login_required
def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    booking.delete()
    return redirect("booking_list")

@login_required
def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)

    if request.method == "POST":
        booking.name = request.POST.get("name")
        booking.age = request.POST.get("age")
        booking.from_place = request.POST.get("from_place")
        booking.to_place = request.POST.get("to_place")
        booking.duration = request.POST.get("duration")
        booking.budget = request.POST.get("budget")
        booking.save()

        return redirect("booking_list")

    return render(request, "edit_booking.html", {"booking": booking})

