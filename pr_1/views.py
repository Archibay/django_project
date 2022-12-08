from django.shortcuts import render


def detail_view(request):
    return render(request, 'detail.html', {})
