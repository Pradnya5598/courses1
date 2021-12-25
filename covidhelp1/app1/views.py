from django.http.response import HttpResponse
from django.shortcuts import render

from app1.models import Hospital, Facility, State, City, Availability
from django.views import generic 

class HospitalDetailView(generic.DetailView):
    model=Hospital


def home(request):
    Selected_state_id = request.GET.get('state') 
    Selected_city_id = request.GET.get('city') 
    Selected_facility_id = request.GET.get('facility') 
    facilities = Facility.objects.all().order_by('title')
    if Selected_state_id:
      cities = City.objects.filter(state=Selected_state_id)
    else:
      cities =City.objects.all()
    states = State.objects.all()
    hospitals = Hospital.objects.all()

    if Selected_city_id: 
       hospitals = hospitals.filter(city=City(pk=Selected_city_id))


    if Selected_facility_id: 
        availibilities = Availability.objects.all()
        if Selected_city_id: 
          availibilities = availibilities.filter(hospital__city=City(pk=Selected_city_id))
           
        availibilities = availibilities.filter(facility=Facility(pk=Selected_facility_id) ,available__gt=0)
        
        hospitals = []
        for avl in  availibilities:
           hospitals.append(avl.hospital)

        print("Hospitals" , hospitals)

    context = {
        'facilities' : facilities,
        'cities' : cities,
        'states' : states,
        'hospitals' : hospitals,
        'selected_state_id' : Selected_state_id,
        'selected_city_id'  : Selected_city_id,
        'selected_facility_id' : Selected_facility_id,
    }
    return render(request , template_name='app1/index.html', context=context)