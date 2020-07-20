# Cognitive behavioral therapy

## Table of Contents
- [Introduction to the Problem](#intro)
- [Congnitive Behaviour therapy](#cbt)
- [Digital Solution](#solution)
- [Contributing](#contributing)
- [Live Demo](#demo)
<a name="intro"/>

## Introduction to the Problem

Depression is very common. 
### What is Depression?

Depression is a common and serious medical illness that negatively affects how you feel, the way you think and how you act. It can lead to a variety of emotional and physical problems and can decrease a person’s ability to function at work and at home.
Symptoms of Depression in women

* Depressed mood

* Loss of interest or pleasure in activities you used to enjoy

* Lack of energy and fatigue

* Feelings of guilt, hopelessness and worthlessness

* Appetite and weight changes

* Sleep changes (sleeping more or sleeping less)

* Difficulty concentrating

* Suicidal thoughts or recurrent thoughts of death

</a>
<a name="cbt"/>

### Cognitive Behavioral Therapy for Depression

CBT is based on two specific tasks: cognitive restructuring, in which the therapist and patient work together to change thinking patterns, and behavioral activation -- in which patients learn to overcome obstacles to participating in enjoyable activities.
</a>
<a name="solution"/>

## Digital Solution to the Problem

The objective of this project is to tackle depression in women by helping in diagnosis of depression and Cognitive Behavioral therapy for treating depression. The platform will be a Web application.
### Features of the Web application
#### Diagnosing Depression

A 3 minute Depression screening test which will give the level of depression. Results will be private.
#### Cognitive Behavioral therapy

* Cognitive restructuring : The website will provide a patient a 14-16 week therapy, which follows CBT. It finds a mental health professional/therapist near the patient who can be assigned to the patient for the next 14-16 weeks. The patient and therapist hold sessions together where they can discuss problems and work on negative thoughts of the patient. This is done via phone-calls or in-person.

* Behavioral activation : In Behavioral activation, Part of the process is looking at obstacles to taking part in that experience and deciding how to get past those obstacles by breaking the process down into smaller steps. This is achieved by a feature called Draw my life. In each week of the session, the patient will be assigned to draw something on the sketchpad (based on JavaScript) on the website. The difficulty will increase each week, making the process engaging and fun.

#### Locating Nearest Community Mental Health center

Enter location and find nearest mental health centers and specialist.
#### Other basic features include :

* User/Patient can login and logout

* Check their profile and see dashboard

* Search mental health centers
</a>
Check the repository and branch for local development
```
cd CBT-therapy
```
```
virtualenv cbt
```
```
source cbt/bin/activate
```

Install requirements
```
pip install --upgrade -r requirements.txt
```
```
python manage.py loaddata therapist.json
```
```
python manage.py loaddata drawing_challenges.json 
```
```
python manage.py runserver
```
</a>

* Access at http://localhost:8000/
"# MenTex" 
"# MenTex" 
