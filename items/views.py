from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LostItemForm
from .models import FoundItem, LostItem

def home(request):
    found_items = FoundItem.objects.all().order_by('-date_posted')
    lost_items = LostItem.objects.all().order_by('-date_posted')
    return render(request, 'items/home.html', {
        'found_items': found_items,
        'lost_items': lost_items,
    })


@login_required
def post_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.user = request.user  # Save the user who posted it
            lost_item.save()
            messages.success(request, "Lost item posted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LostItemForm()

    return render(request, 'items/post_lost_item.html', {'form': form})

from .forms import FoundItemForm  # make sure this import exists at the top

@login_required
def post_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.user = request.user  # Save the user who posted it
            found_item.save()
            messages.success(request, "Found item posted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FoundItemForm()

    return render(request, 'items/post_found_item.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoundItem, ClaimAttempt


@login_required
def claim_item(request, item_id):
    """
    Handles the process when a user claims a found item.
    The verification questions are displayed automatically from the FoundItem,
    and the claimant's answers are checked for correctness.
    """
    found_item = get_object_or_404(FoundItem, id=item_id)

    if request.method == 'POST':
        # Get answers directly from the form textareas
        answer1 = request.POST.get('answer1', '').strip()
        answer2 = request.POST.get('answer2', '').strip()
        answer3 = request.POST.get('answer3', '').strip()

        # Create a new claim attempt
        claim = ClaimAttempt.objects.create(
            found_item=found_item,
            claimant=request.user,
            answer1=answer1,
            answer2=answer2,
            answer3=answer3,
        )

        # Automatically check answers and update approval status
        claim.check_answers()
        claim.save()

        # Feedback message to user
        if claim.approved:
            messages.success(request, "✅ Claim approved! You answered correctly.")
        else:
            messages.error(request, "❌ Claim denied. Answers didn’t match.")

        return redirect('home')

    # GET request: show the form
    return render(request, 'items/claim_item.html', {'found_item': found_item})

from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import FoundItem

@staff_member_required
def get_questions(request, found_item_id):
    try:
        found_item = FoundItem.objects.get(id=found_item_id)
        questions = list(found_item.questions.values_list('question_text', flat=True))
        return JsonResponse({'questions': questions})
    except FoundItem.DoesNotExist:
        return JsonResponse({'questions': []})
