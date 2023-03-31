# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView


def homePageView(request):
    return render(request, 'home.html', {
        'yearsEducationOption': [12,13,14,15,16, 'More than 16'],
        'mynumbers': [1, 2, 3, 4, 5, 6, ],
        'firstName': 'Simron',
        'lastName': 'Adiwal'})


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')


def simronPageView(request):
    # return request object and specify page.
    return render(request, 'simron.html')


from django.http import HttpResponseRedirect
from django.urls import reverse


def homePost(request):
    # Use request object to extract choice.

    choice = 1 # -999
    gmat = 1 #-999

    try:
        # Extract value from request object by control name.
        # currentChoice = request.POST['choice']
        # gmatStr = request.POST['gmat']
        educStr = request.POST['education']
        unemploymentStr = request.POST['unemployment']
        distStr = request.POST['distance']
        tuitionStr = request.POST['tuition']

        # Crude debugging effort.
        # print(educStr, unemploymentStr, distStr, tuitionStr)
        # choice = int(currentChoice)
        # gmat = float(gmatStr)
        educ = float(educStr)
        unemployment = float(unemploymentStr)
        dist = float(distStr)
        tuition = float(tuitionStr)
        print("*** Years of education: " + str(educ))
        print("*** Unemployment rate: " + str(unemployment))
        print("*** Distance from campus: " + str(dist))
        print("*** Tuition cost: " + str(tuition))

    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'educ': educ, 'unemployment':
            unemployment, 'dist': dist, 'tuition': tuition}))
        # return HttpResponseRedirect(reverse('results', kwargs={'choice': choice, 'gmat': gmat}, ))



import pickle
# import sklearn # You must perform a pip install.
import pandas as pd

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def results(request, educ, unemployment, dist, tuition):
    print("*** Inside results()")

    # Check if input values are valid
    educ = float(educ)
    unemployment = float(unemployment)
    dist = float(dist) / 10
    tuition = float(tuition) / 10000
    #
    # if not (0 <= unemployment <= 100):
    #     return render(request, 'error.html', {'message': 'Invalid unemployment rate'})
    # if not (0 <= educ <= 20):
    #     return render(request, 'error.html', {'message': 'Invalid education level'})
    # # Add more checks for other input values as needed

    # Load saved model
    with open('/Users/simro1/Desktop/4949/A2/A2 Django /linear_regression_model_1.pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSample = np.array([[educ, unemployment, dist, tuition]])
    print('singleSample', singleSample)

    # Standardize input data
    # scaler = StandardScaler()
    # singleSample = scaler.fit_transform(singleSample)

    print('singleSample after standardizing', singleSample)


    singlePrediction = loadedModel.predict(singleSample)
    finalTestScorePrediction = round(singlePrediction[0], 2)
    print("finalTestScorePrediction", finalTestScorePrediction)
    # singlePrediction = round(singlePrediction, 2)

    print("Single prediction: " + str(singlePrediction))

    # change the units back to scale that the user inputted in (had to scale down to match model)
    dist = float(dist) * 10
    tuition = float(tuition) * 10000

    return render(request, 'results.html', {'educ': educ, 'unemployment': unemployment,
                                            'dist': dist, 'tuition': tuition,
                                            'prediction': finalTestScorePrediction})


from pages.models import Item, ToDoList
def todos(request):
    print("*** Inside todos()")
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    return render(request, 'ToDoItems.html', 
                {'ToDoItemDetail': itemErrandDetail})



from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            # return redirect("../") # Go to home page
            return HttpResponseRedirect(reverse('message', kwargs={'msg': "Your are registered.", 'title': "Success!"}, ))

    # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})


def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title })




def secretArea(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('message',
               kwargs={'msg': "Please login to access this page.", 
                       'title': "Login required."}, ))
    return render(request, 'secret.html', {'useremail': request.user.email })
