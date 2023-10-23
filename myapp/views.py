from django.shortcuts import render, redirect
from .models import Food, Consume
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

def index(request):
    foods = None
    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        User = get_user_model()
        if isinstance(request.user, User):
            try:
                consume = Food.objects.get(name=food_consumed)
                Consume.objects.create(user=request.user, food_consumed=consume)
            except Food.DoesNotExist:
                pass

        foods = Food.objects.all()
    User = get_user_model()
    if isinstance(request.user, User):
        consumed_food = Consume.objects.filter(user=request.user)
    else:
        consumed_food = None 

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        if consumed_food.user == request.user:
            consumed_food.delete()
            return redirect('/')
        else:
            return HttpResponseForbidden("You don't have permission to delete this item.")
    return render(request, 'myapp/delete.html')
