from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LostItemForm, FoundItemForm
from .models import FoundItem, LostItem, ClaimAttempt

# ---- LOGIN/LOGOUT ----
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'items/login.html')

from django.contrib.auth.models import User

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    return render(request, 'items/signup.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

# ---- HOME ----
def home(request):
    found_items = FoundItem.objects.all().order_by('-date_posted')
    lost_items = LostItem.objects.all().order_by('-date_posted')
    return render(request, 'items/home.html', {
        'found_items': found_items,
        'lost_items': lost_items,
    })

# ---- POST LOST ITEM ----
@login_required
def post_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.user = request.user
            lost_item.save()
            messages.success(request, "Lost item posted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LostItemForm()
    return render(request, 'items/post_lost_item.html', {'form': form})

# ---- POST FOUND ITEM ----
@login_required
def post_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.user = request.user
            found_item.save()
            messages.success(request, "Found item posted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FoundItemForm()
    return render(request, 'items/post_found_item.html', {'form': form})

# ---- CLAIM ITEM ----
@login_required
def claim_item(request, item_id):
    found_item = get_object_or_404(FoundItem, id=item_id)
    if request.method == 'POST':
        answer1 = request.POST.get('answer1', '').strip()
        answer2 = request.POST.get('answer2', '').strip()
        answer3 = request.POST.get('answer3', '').strip()

        claim = ClaimAttempt.objects.create(
            found_item=found_item,
            claimant=request.user,
            answer1=answer1,
            answer2=answer2,
            answer3=answer3,
        )

        claim.check_answers()
        claim.save()

        if claim.approved:
            messages.success(request, "✅ Claim approved! You answered correctly.")
        else:
            messages.error(request, "❌ Claim denied. Answers didn’t match.")

        return redirect('home')
    return render(request, 'items/claim_item.html', {'found_item': found_item})

# ---- GET QUESTIONS FOR STAFF ----
@staff_member_required
def get_questions(request, found_item_id):
    try:
        found_item = FoundItem.objects.get(id=found_item_id)
        questions = list(found_item.questions.values_list('question_text', flat=True))
        return JsonResponse({'questions': questions})
    except FoundItem.DoesNotExist:
        return JsonResponse({'questions': []})
