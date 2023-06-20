from django.shortcuts import render

def index(request):
    return render(request, 'catalog/index.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name}, {phone}: {message}")
    return render(request, 'catalog/contacts.html')
