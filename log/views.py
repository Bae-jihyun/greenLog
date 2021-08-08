from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import Post,Photo
from django.db.models import Count
from django.contrib import messages


def home(request):
    return render(request,'home.html')

def login(request):
    if request.method== 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        nickname = request.POST.get('nickname', None)
        password = request.POST.get('password', None)
  
    res_data = {}
    if not (nickname and password):
        res_data['error'] = '모든 값을 입력해야 합니다.'
        return render(request, 'login.html', res_data)
    else:
        try: 
            user = User.objects.get(nickname = nickname)
            if check_password(password, user.password):
                request.session['user'] = user.nickname
                return redirect('home')
            else:
                res_data['error'] = '아이디와 비밀번호를 다시 확인해주세요.'
                return render(request, 'login.html', res_data)
        except: 
            res_data['error'] = '아이디와 비밀번호를 다시 확인해주세요.'
            return render(request, 'login.html', res_data)

    if user is not None:
        self.request.session['nickname'] = nickname
        login(self.request, user)
        remember_session = self.request.POST.get('remember_session', False)
        if remember_session:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    return redirect("home")

def signup(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        name = request.POST['name']
        password = request.POST['password']
        passwordcheck = request.POST['passwordcheck']
        profile = request.FILES['profile']
        
        res_data = {} #응답 메시지를 담을 변수(딕셔너리)
        if not (password and passwordcheck and nickname and name and profile):
            res_data['error'] = '모든 값을 입력해야 합니다.'
            return render(request, 'signup.html', res_data)
        elif password != passwordcheck:
            res_data['error'] = '비밀번호가 다릅니다'
            return render(request, 'signup.html', res_data)
        elif User.objects.filter(nickname = request.POST['nickname']).exists():
            res_data['error'] = '이미 존재하는 닉네임입니다.'
            return render(request, 'signup.html', res_data)
        else:
            user = User( # 모델에서 생성한 User 클래스를 가져와 객체 생성
                nickname = nickname,
                name = name,
                password = make_password(password),
                profile = profile,
            )
            user.save() #데이터베이스에 저장
            return render(request, 'signup_done.html', {'message': '회원가입을 완료하였습니다.'})
    return render(request, 'signup.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('home')

def mypage(request):
    myposts = Post.objects.order_by('-date')
    search = request.GET.get('search')
    if search == 'true':
        author = request.GET.get('author')
        myposts = Post.objects.filter(writer = author)
        my_postcount = Post.objects.filter(writer = author).count()#게시물 개수 세기
        #회원 멤버쉽 저장 -> 수정******
        my_membership = User.objects.get(nickname = author)
        if my_postcount >= 0 and my_postcount < 15:
            my_membership.Member = "Bronze"
        elif my_postcount >= 15 and my_postcount < 30:
            my_membership.Member = "Silver"
        elif my_postcount >= 30 and my_postcount < 45:
            my_membership.Member = "Gold"
        elif my_postcount >= 45 and my_postcount < 60:
            my_membership.Member = "Platinum"
        elif my_postcount >= 60 and my_postcount < 75:
            my_membership.Member = "Diamond"
        elif my_postcount >= 75:
            my_membership.Member = "Ruby"      
        my_membership.save()
        
        myposts_list = []#image url 추출하기
        date = []# 잔디밭 구현을 위한(월,일 담을) 리스트
        loop_counter = []#carousel row가 2개로 나오기 때문에 for반복문 횟수 미리 정함.
        id = []# 내가 쓴 게시물로 이동을 위해 id를 담은 리스트
        
        #사진 업로드 여러개 가능 -> 이에 대해서 각 해당 포스트의 image 리스트에서 첫 번째 사진을 대표로 썸네일로 정함.
        for mypost in myposts:
            for index, photo in enumerate(mypost.photo_set.all()):
                if index == 0:
                    image_url = str(photo.image.url)
                else:
                    break
            ids = mypost.id
            id.append(ids)
            myposts_list.append(image_url)

        for mypost in myposts:
            date.append(mypost.date.strftime("%m"))
            date.append(mypost.date.strftime("%d"))
        if my_postcount % 2 == 0:#짝수일때
            for i in range(0,my_postcount//2):
                loop_counter.append(0)
            
        else:
            for i in range(0,my_postcount//2+1):
                loop_counter.append(0)
    
    myposts_list = list(myposts_list)
    return render(request, 'mypage.html',{'membership':my_membership,'dates':date,'count':my_postcount,'myposts_list':myposts_list,'loop_counter':loop_counter,'id':id})


def each(request, post_id): 
    MyPost = get_object_or_404(Post, pk = post_id)
    Image=Photo.objects.filter(post=MyPost.id)
    Writer= User.objects.get(pk=MyPost.writer)
    like="false"
    
    if request.method == "POST":
        try:
            user=request.session['user']
            users_list=MyPost.like_users.all()
            for users in users_list:
                if(users.nickname == user):
                    MyPost.like_users.remove(user)
                    MyPost.like-=1
                    MyPost.save()
                    return render(request, 'eachNomal.html',{'MyPost':MyPost,'Writer':Writer,'Image':Image,'like':like})
            like="true"
            MyPost.like_users.add(user)
            MyPost.like+=1
            MyPost.save()
        except:
            messages.warning(request, '로그인이 필요합니다.')
            return redirect('login')
    return render(request, 'eachNomal.html',{'MyPost':MyPost,'Writer':Writer,'Image':Image,'like':like})

def post(request):
    return render(request, 'post.html')

def create(request):
    new_post = Post()
    new_post.kinds=request.POST['volunteerKinds']
    new_post.title=request.POST['title']
    new_post.writer=request.session['user']
    new_post.content=request.POST['contentInput']
    place1 = request.POST["h_area1"]
    place2 = request.POST["h_area2"]
    new_post.firstPlace= place2
    new_post.like=0
    new_post.date= timezone.datetime.now()
    new_post.save()
    if request.FILES.getlist('images'):
        for img in request.FILES.getlist('images'):
            photo = Photo()
            photo.post = new_post
            photo.image = img
            photo.save()
    else :
        new_post.image= "../static/images/noPhoto.png"
    return redirect('home')

def plogging(request):
    place =  request.GET.get("h_area2")
    posts = Post.objects.filter(kinds='플로깅',firstPlace = place).distinct()
    if 'h_area2' in request.POST:
        posts = Post.objects.filter(firstPlace = place).distinct()
    All=[]
    for post in posts:
        One=[]
        One.append(post.id)
        One.append(Photo.objects.filter(post=post.id).first().image.url)
        All.append(One)
    return render(request, 'plogging.html',{'place':place, 'posts':posts, 'All':All })

def container(request):
    posts=Post.objects.all().filter(kinds='용기내').distinct()
    All=[]
    for post in posts:
        One=[]
        One.append(post.id)
        One.append(Photo.objects.filter(post=post.id).first().image.url)
        All.append(One)
    return render(request, 'container.html',{'All':All})

def gogo(request):
    posts=Post.objects.all().filter(kinds='고고').distinct()
    All=[]
    for post in posts:
        One=[]
        One.append(post.id)
        One.append(Photo.objects.filter(post=post.id).first().image.url)
        All.append(One)
    return render(request, 'gogo.html',{'All':All})

def vegetarian(request):
    posts=Post.objects.all().filter(kinds='채식').distinct()
    All=[]
    for post in posts:
        One=[]
        One.append(post.id)
        One.append(Photo.objects.filter(post=post.id).first().image.url)
        All.append(One)
    return render(request, 'vegetarian.html',{'All':All})

def others(request):
    posts=Post.objects.all().filter(kinds='기타').distinct()
    All=[]
    for post in posts:
        One=[]
        One.append(post.id)
        One.append(Photo.objects.filter(post=post.id).first().image.url)
        All.append(One)
    return render(request, 'others.html',{'All':All})

def edit_profile(request,user):
    user_profile = User.objects.get(nickname=user)
    user_profile.profile = request.FILES['profile']
    user_profile.save()
    return redirect('/mypage/?search=true&author=' + str(user_profile.nickname))
