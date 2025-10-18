from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from orders.models import Order

@login_required
def submit_feedback(request, order_id=None):
    order = None
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.order = order
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback_history')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {
        'form': form,
        'order': order
    })

@login_required
def feedback_history(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'feedback/feedback_history.html', {'feedbacks': feedbacks})