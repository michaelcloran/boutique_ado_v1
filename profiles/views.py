from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from .forms import UpdateUserForm

from checkout.models import Order

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            message.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        form = UserProfileForm(instance=profile)
        
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'user_form': user_form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)