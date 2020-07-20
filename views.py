from django.shortcuts import render,redirect
from django.http import HttpResponse
import random
# for login and logout
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Forms
from .forms import UserForm,UserProfileForm,CBT_therapyForm,RegisterCBTForm
#Models
from .models import Therapist,CBT_therapy,User,UserProfile,Challenge,WeeklySession
from datetime import datetime, timedelta

import pandas as pd
from sklearn.model_selection import train_test_split



from random import randint

# Create your views here.
def index(request):
    return render(request,'home.html',{})

def techniques(request):
    return render(request,'techniques.html',{})


def screen_test(request):
    return render(request,'screen_test.html',{})

def anxiety(request):
    return render(request,'anxiety.html')
def stress(request):
    return render(request,'stress.html',{})


def createDataset(request):
    columnList=['How was your sleep over last few weeks?','How is your appetite?','How often do you feel low?','How interested are you on doing things that you used to do before?','How often are you tired and it takes effort to do small things?','Do you take everything as negative purpose?','Do you think depression hinders your ability to work with people?']
    rowValues=[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    ansList = []
    for i in range(0,2):
        temp = []
        for k in rowValues:
            randomNumber=randint(0,4)
            temp.append(k[randomNumber])
        ansList.append(temp)
    print(ansList)


def trainModel(request):
    
    list1=request.GET.get('test')
    print(list1)
    df=pd.read_csv('test2c.csv',)
    
    
    # for i in df.columns:
    #     df[i]=df[i]/max(df[i])
    
    X=df.iloc[:,:-1].values
    y=df.iloc[:,-1].values
    
    X_train,X_test,Y_train,Y_test=train_test_split(X,y,test_size=0.30,random_state=0)
    print(X_train)
    print(Y_train.shape)

    from sklearn.naive_bayes import GaussianNB    
    model = GaussianNB()
    # import pickle
    # model = pickle.loads(model)
    # print(model)
    # Train the model using the training sets
    model.fit(X_train,Y_train)
  
    # model.predict(X_test)
    y_pred=model.predict(X_test)
    # print(y_pred)
    # print(Y_test)
   
    from sklearn.metrics import confusion_matrix
    print(confusion_matrix(Y_test, y_pred))
    # for i in range(0,7):
    #     list1[i]=random.randint(1,4)
        
    # print(list1)    
    anxiety=model.predict([[1,2,3,1,3,1,4]])
    if anxiety==1:
       print('low')
    elif anxiety==2:
       print('medium')  
    else:
        print('high')     
    # return render(request,'register.html')
        
    # import pickle 
    
    # Save the trained model as a pickle string. 
    # model = pickle.dumps(model) 
    
    # Load the pickled model 
    # knn_from_pickle = pickle.loads(saved_model) 
  
# Use the loaded pickled model to make predictions 
# knn_from_pickle.predict(X_test) 
    
    # Use the loaded model to make predictions 
    # knn_from_joblib.predict(X_test) "hi"
    return HttpResponse(anxiety)


def register(request):

    registered=False
    if request.method =='POST':
        user_form=UserForm(request.POST or None)
        profile_form=UserProfileForm(request.POST or None,request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user_form.cleaned_data.get('password'))
            username=user_form.cleaned_data.get('username')
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
           # Update our variable to tell the template registration was successful.
            registered=True
            login(request,user)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()

    return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def locate(request):
    return render(request,'map.html',{})

def registerCBT(request):
    if request.method == 'POST':
        register_form = RegisterCBTForm(request.POST or None)
        if register_form.is_valid():
            start_date=register_form.cleaned_data['start_date']
            session_time=register_form.cleaned_data['session_time']
            user=request.user
            username=UserProfile.objects.get(user=user)
            region=username.get_region()
            try:
                therapist_name=Therapist.objects.get(region=region)
            except : 
                therapist_name=Therapist.objects.get(region='online')
            cbt=CBT_therapy(
                user=user,
                start_date=start_date,
                session_time=session_time,
                therapist=therapist_name
                )
            cbt.save()
            session_date=start_date
            for challenge in Challenge.objects.all():
                session_date = session_date + timedelta(days=7)
                w=WeeklySession(
                     session_time =session_time,
                     session_date =session_date,
                     week_no=challenge.pk,
                     challenge=challenge.title,
                     therapy=cbt
                    )
                w.save()
            return render(request,'home.html',{})
    else:
        register_form = RegisterCBTForm()
    return render(request,'register_for_cbt.html',{'register_form':register_form})



def viewCBT(request):
    registered=False
    if request.user.is_authenticated():
        user=request.user
        try:
            temp=CBT_therapy.objects.filter(user=user)
            registered=True
            print(registered)
        except:
            registered=False
    return render(request,'cbt.html',{registered:registered})

@login_required
def dashboard(request):
    user=request.user
    username=UserProfile.objects.get(user=user)
    try:
        cbt=CBT_therapy.objects.get(user=user)
        therapy=WeeklySession.objects.select_related().filter(therapy=cbt)
    except:
        therapy=False
        cbt=False
    return render(request,'dashboard.html',{'user':username,'therapy':therapy,'cbt':cbt})

@login_required
def session(request,pk):
    user=request.user
    username=UserProfile.objects.get(user=user)
    cbt=CBT_therapy.objects.get(user=user)
    therapy=WeeklySession.objects.select_related().get(pk=pk)
    attended=WeeklySession.objects.select_related().filter(therapy=cbt)
    session_active=therapy.start_session()
    # therapist=Therapist.objects.get(name=cbt.therapist)
    return render(request,'session.html',{'session_active':session_active,'therapy':therapy,'cbt':cbt,'attended':attended})

@login_required
def draw(request,pk):
    week=WeeklySession.objects.get(pk=pk)
    challenge=week.challenge
    return render(request,'draw.html',{'challenge':challenge})

def sampleDraw(request,pk):
    challenge=Challenge.objects.get(pk=pk)
    return render(request,'draw.html',{'challenge':challenge.title})