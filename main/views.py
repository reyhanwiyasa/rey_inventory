from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Reyhan Wiyasa P',
        'class': 'PBP A',
        'amount' : 100,
        'description' : 'Peppermint\'s storage'
    }

    return render(request, "main.html", context)

# Create your views here.
