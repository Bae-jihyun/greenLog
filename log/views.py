from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def post(request):
    return render(request, 'post.html')

def mypage(request):
    return render(request, 'mypage.html')


def each(request):
    return render(request, 'eachView.html')

def others(request):
    return render(request,'others.html')

def plogging(request):
    return render(request, 'plogging.html')

def container(request):
    return render(request, 'container.html')

def GoGo(request):
    return render(request, 'GoGo.html')

def vegetarian(request):
    return render(request, 'vegetarian.html')

def container(request):
    return render(request, 'container.html')

>>>>>>> Stashed changes
