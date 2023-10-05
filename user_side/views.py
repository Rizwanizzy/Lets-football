from django.shortcuts import render,redirect
from .models import TeamMembers

# Create your views here.
def home(request):
    user=request.user
    role_choices = TeamMembers.ROLE_CHOICES
    members=TeamMembers.objects.filter(user=user)
    if request.method == 'POST':
        name=request.POST['name']
        number=request.POST['number']
        role=request.POST['role']
        team_members=TeamMembers(name=name,number=number,role=role,user=user)
        team_members.save()
        return redirect('home')
    context={
        'user':user,
        'role_choices':role_choices,
        'members':members
        }
    return render(request,'home.html',context)

def squad(request):
    user = request.user
    team_members = TeamMembers.objects.filter(user=user)
    positions = [
        {'position': 'pos1', 'margin': '5px 17px'},
        {'position': 'pos2', 'margin': '65px 40px'},
        {'position': 'pos3', 'margin': '65px 117px'},
        {'position': 'pos4', 'margin': '65px 194px'},
        {'position': 'pos5', 'margin': '65px 271px'},
        {'position': 'pos6', 'margin': '114px 76px'},
        {'position': 'pos7', 'margin': '114px 156px'},
        {'position': 'pos8', 'margin': '114px 238px'},
        {'position': 'pos9', 'margin': '165px 110px'},
        {'position': 'pos10', 'margin': '165px 202px'},
        {'position': 'pos11', 'margin': '195px 156px'},

    ]
    squad_data = list(zip(team_members, positions))
    return render(request,'squad.html',{'squad_data':squad_data})