
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method== 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        id = request.POST.get('id', None)
        password = request.POST.get('password', None)
  
    res_data = {}
    if not (id and password):
        res_data['error'] = '모든 값을 입력해야 합니다.'
        return render(request, 'login.html', res_data)
        
    else:
        user = User.objects.get(id = id)
        if check_password(password, user.password):
            request.session['user'] = user.id
            return redirect('home')
        else:
            res_data['error'] = '비밀번호가 틀렸습니다.'
    
            return render(request, 'login.html', res_data)
    
    if user is not None:
        self.request.session['nickname'] = nickname
        login(self.request, user)
        remember_session = self.request.POST.get('remember_session', False)
        if remember_session:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    return redirect("home")

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        
            id = request.POST['id']
            nickname = request.POST['nickname']
            name = request.POST['name']
            password = request.POST['password']
            passwordcheck = request.POST['passwordcheck']

            res_data = {} #응답 메시지를 담을 변수(딕셔너리)

            if not (id and password and passwordcheck and nickname and name):
                res_data['error'] = '모든 값을 입력해야 합니다.'
                return render(request, 'signup.html', res_data)
            elif password != passwordcheck:
                res_data['error'] = '비밀번호가 다릅니다'
                return render(request, 'signup.html', res_data)
            elif User.objects.filter(id = request.POST['id']).exists():
                res_data['error'] = '이미 존재하는 아이디입니다.'
                return render(request, 'signup.html', res_data)
            elif User.objects.filter(nickname = request.POST['nickname']).exists():
                res_data['error'] = '이미 존재하는 닉네임입니다.'
                return render(request, 'signup.html', res_data)
            else:
                user = User( # 모델에서 생성한 User 클래스를 가져와 객체 생성
                    id = id,
                    nickname = nickname,
                    name = name,
                    password = make_password(password),
                )

                user.save() #데이터베이스에 저장
                return render(request, 'signup_done.html', {'message': '회원가입을 완료하였습니다.'})
    return render(request, 'signup.html')

def post(request):

    return render(request, 'post.html')


def mypage(request):
    myposts = Post.objects
    search = request.GET.get('search')
    if search == 'true':
        writer = request.GET.get('writer')
        myposts = Post.objects.filter(author = writer)
    return render(request, 'mypage.html',{'myposts':myposts})


def each(request):
    return render(request, 'eachView.html')


def detail(request):
    post=request.GET['volunteerKinds']
    posts=[]
    posts.append(post)
    posts.append(request.GET['title'])
    posts.append(request.GET['author'])
    posts.append(request.GET['contentInput'])
    posts.append(request.GET['images'])
    posts.append(request.GET['place'])

    if post == '플로깅':
        return render(request, 'plogging.html',{'posts':posts})
    elif post =='채식':
        return render(request, 'vegetarian.html',{'posts':posts})
    elif post =='용기내':
        return render(request, 'container.html',{'posts':posts})
    elif post =='고고':
        return render(requset, 'gogo.html',{'posts':posts})
    else :
        return render(request, 'others.html',{'posts':posts})



def plogging(request,post):
    if post ==null:
        s = Plogging.objects.all()  
    return render(request, 'plogging.html')

def container(request):
    return render(request, 'container.html')

def gogo(request):
    return render(request, 'gogo.html')

def vegetarian(request):
    return render(request, 'vegetarian.html')

def others(request):
    return render(request,'others.html')

def logout(request):
    
    if request.session.get('user'):
        del(request.session['user'])
        
    return redirect('home')
