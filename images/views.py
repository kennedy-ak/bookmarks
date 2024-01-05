from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
# Create your views here.


@login_required
def image_create(request):
    if request.method == 'POST':
        #form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            #if form is valid

            cd = form.cleaned_data
            # creating an instance but not saving it

            new_item = form.save(commit=False)

            #assign a user to the item
            new_item.user = request.user
            new_item.save()

            messages.success(request, 'Image added successfully')
            # redirect to the new created item detail view

            return redirect(new_item.get_absoulte_url())
        else:
            form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html',{'form':form})