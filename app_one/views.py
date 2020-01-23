import bcrypt
from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render

from app_one.models import Trip, User

# from app_one.models import Author, Book, Review, User

# Create your views here.
def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    if request.session['logged_in'] == True:
        return redirect('/dashboard')
    return render(request, "index.html")

def create_user(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    if request.session['logged_in'] == True:
        return redirect('/dashboard')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        name = request.POST['f_name']
        alias = request.POST['l_name']
        email = request.POST['email']
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(f_name=name, l_name=alias,email=email, password=password)
        request.session['logged_in'] = True
        request.session['user_id'] = newUser.id
        return redirect('/dashboard')

    return redirect('/dashboard')

def log_in(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    if request.session['logged_in'] == True:
        return redirect('/dashboard')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        print("Not good!")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    request.session['logged_in'] = True
    request.session['user_id'] = User.objects.get(email=request.POST['email']).id 
    print(request.session['user_id'])
    return redirect('/dashboard')

def dashboard(request):
    if not logVal_user(request):
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    user_trips = current_user.trips_made.all()
    user_joined = current_user.trips_joined.all()
    all_trips = Trip.objects.all()
    filtered_trips = filter(lambda i: i not in user_trips, all_trips)
    filter_2 = filter(lambda i : i not in user_joined, filtered_trips)

    context = {
        'user_joined':user_joined,
        'other_trips':filter_2,
        'current_user':current_user,
        'all_trips': all_trips,
    }
    return render(request,"dashboard.html", context)

def log_out(request):
    request.session.flush()
    return redirect('/')

def new_trip(request):
    if not logVal_user(request):
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])

    context = {
        'user':current_user
    }
    return render(request, "new_trip.html", context)

def create_trip(request):
    if not logVal_user(request):
        return redirect('/')
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        print("trip not made!")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    dest = request.POST['dest']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    plan = request.POST['plan']
    made_by = User.objects.get(id=request.session['user_id'])
    print("trip made!")
    newTrip = Trip.objects.create(dest=dest, start_date=start_date, end_date=end_date, plan=plan, made_by=made_by)
    return redirect('/dashboard')

def edit_trip(request, trip_id):
    if not logVal_user(request):
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    current_user = User.objects.get(id=request.session['user_id'])
    start_date = trip.start_date.strftime("%Y-%m-%d")
    end_date = trip.end_date.strftime("%Y-%m-%d")
    
    context = {
        'start_date':start_date,
        'end_date':end_date,
        'trip':trip,
        'user':current_user,
    }
    return render(request, 'edit_trip.html', context)

def make_changes(request, trip_id):
    if not logVal_user(request):
        return redirect('/')
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        print("trip not editted!")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/edit/'+str(trip_id))
    dest = request.POST['dest']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    plan = request.POST['plan']
    made_by = User.objects.get(id=request.session['user_id'])
    print("trip changed!")
    trip = Trip.objects.get(id=trip_id)
    trip.dest = dest
    trip.start_date = start_date
    trip.end_date = end_date
    trip.plan = plan
    trip.save()
    return redirect('/dashboard')

def trip_page(request, trip_id):
    if not logVal_user(request):
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)

    context = {
        'user':current_user,
        'trip':trip,


    }
    return render(request, "trip_page.html", context)

def delete_trip(request, trip_id):
    if not logVal_user(request):
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    if trip.made_by.id != user.id:
        return redirect('/log_out')
    trip.delete()
    return redirect('/dashboard')

def join_trip(request, trip_id):
    if not logVal_user(request):
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    user.trips_joined.add(trip)

    return redirect('/dashboard')

def leave_trip(request, trip_id):
    if not logVal_user(request):
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    user.trips_joined.remove(trip)
    return redirect('/dashboard')
















#################HELPER FUNCTIONS

def logVal_user(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    if request.session['logged_in'] == False:
        return(False)
    return(True)
