from django.shortcuts import render
from .models import MainContent


def home(request):
    items = MainContent.objects.all()
    main_content = {item.key: item.value for item in items}
    return render(request, 'main.html', {'main_content': main_content})
