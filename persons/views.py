from django.shortcuts import render,redirect,get_object_or_404
from persons.models import Home,Picture,State,City,Comment,Member
from django.template import loader,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import HomeForm,ImageForm,CommentForm
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.forms import inlineformset_factory


class SignUpView(CreateView):
    template_name = 'persons/signup.html'
    form_class = UserCreationForm





def validate_username(request):
    username = request.GET.get('username', None)
    print("############################")
    print(username)
    print("############################")
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'این نام کاربری قبلا ثبت نام کرده است.'
    return JsonResponse(data)



#-------------------------------------------------------------------#
@login_required
def addHome(request):
    current_user = request.user

    template_name='persons/add_home.html'
    state = request.POST.get("state" or None)
    city = request.POST.get("city" or None)
    form1 = HomeForm(request.POST or None, request.FILES or None)
    form2 = ImageForm(request.POST or None, request.FILES or None)
    if form1.is_valid():
        if form2.is_valid():
            _home=form1.save(commit=False)
            _image=form2.save(commit=False)
            _home.member_id= current_user.id
            _home.state= state
            _home.city= city
            _home.save()
            _image.homeid= _home
            _image.save()
            return redirect('persons:show_homes')
    states =  State.objects.all()  

    context ={
            "form1":form1,
            "form2":form2,
            "states":states,
                    }

    return render(request,template_name,context)

def select_citys(request):
    ostan_name = request.GET.get('ostan_name'or None)
    ostan_id = State.objects.get(name=ostan_name)
    citys = City.objects.filter(ostan=ostan_id)

    a={}
    for city in citys:
        a[city.name]=city.name

    return JsonResponse(a)


#-------------------------------------------------------------------#
@login_required
def yourHomes(request):
	current_user = request.user
	#f = User.objects.filter(pk=h.member_id)

	_yourHomes= Home.objects.filter(member_id=current_user.id) 
	template_name='persons/yourHomes.html'


	return render(request,template_name,{'yourHomes':_yourHomes})
	


#@login_required
def showHome(request):
    current_user = request.user
    template_name = 'home.html'
    homes = Home.objects.all().order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        homes = homes.filter(
            Q(name__icontains = query)|
            Q(state__icontains = query)|
            Q(member__first_name__icontains = query)|
            Q(member__last_name__icontains = query)|
            Q(member__username__icontains = query)|
            Q(city__icontains = query)
        ).distinct()
	
    return render(request,template_name,{'homes':homes,'user':current_user})

def base(request):
    template_name = 'base.html'
    
    return render(request,template_name,{})

def detail_home(request,home_id):
    h = Home.objects.get(pk=home_id)
    f = User.objects.get(pk=h.member_id)
    current_user = request.user

    im_of_this_house = Picture.objects.filter(homeid=home_id).order_by('-timestamp')
    comments = Comment.objects.filter(home=home_id).order_by('-timestamp')
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        _image=form.save(commit=False)
        _image.homeid=h
        _image.save()
    form2 = CommentForm(request.POST or None)
    if form2.is_valid():
        _comment=form2.save(commit=False)
        _comment.home=h
        _comment.writer=current_user
        _comment.save()

    # context ={
    #         "home":h
    #         "owner":f
    #         "pictures":im_of_this_house
    #         "form":form
    #         "form2":form2
    #                 }
    return render(request,'persons/detail_home.html',{'home':h,'owner':f,'pictures':im_of_this_house,'form':form,'form2':form2,'comments':comments})

def detail_user(request,user_id):
	user = User.objects.get(pk=user_id)
	return render(request,'persons/detail_user.html',{'u':user})

def home_delete(request,home_id = None):
    instance = get_object_or_404(Home,id=home_id)
    instance.delete()
    return redirect("persons:show_homes")

def home_update(request,home_id = None):
    instance = get_object_or_404(Home,id=home_id)
    form = HomeForm(request.POST or None,instance = instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())

    context = {
            "instance": instance,
            "form":form,
        }
    template_name = 'persons/home_update.html'
    return render(request, template_name, context)
def delete_image(request,img_id = None):
    img = get_object_or_404(Picture,id=img_id)
    p = img.homeid
    print(img.get_absolute_url())
    img.delete()
    return HttpResponseRedirect(img.get_absolute_url())

