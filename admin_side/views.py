from django.shortcuts import render,redirect
from authentication.models import CustomUser
from datetime import datetime, timedelta
import random
from admin_side.models import Fixtures
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

# Admin Home View
def admin_home(request):
    # Get the currently logged-in admin user
    admin=request.user
    # Fetch and order non-superuser teams by points
    teams = CustomUser.objects.filter(is_superuser=False).order_by('-points')
    # Render the admin home page with admin user and teams data
    return render(request,'admin_home.html',{'admin':admin,'teams':teams})

# Round 1 View
def round_1(request):
    user=request.user
    total_team=CustomUser.objects.count()
    fixture_count=Fixtures.objects.count()
    fixture_all=Fixtures.objects.filter(round='Round 1').order_by('id')
    # Check if there are enough teams to start fixtures
    if total_team < 11:
        count=False
    else:
        count=True
    # Check if fixtures for Round 1 have been created
    if fixture_count != 0:
        display=True
    else:
        display=False
    venues=['Kerala','Kolkata','Goa','Bangaluru','Mumbai']
    if request.method == 'POST':
        # Retrieve starting date to schedule the Round 1 fixture
        date_str=request.POST['date']
        date=datetime.strptime(date_str,'%Y-%m-%d')
        print('selected_date',date_str)
        teams=list(CustomUser.objects.filter(is_superuser=False))
        # Dividing the whole teams into 2 groups
        group1=teams[:5]
        group2=teams[5:10]
        # Set 'win' field to False for all teams
        CustomUser.objects.all().update(win=False)
        for i in range(len(group1)):
            for j in range(i+1,len(group1)):

                selected_venue = random.choice(venues)
                # Creating fixture for group1
                fixture1=Fixtures(venue=selected_venue,date=date.strftime('%Y-%m-%d'),team1=group1[i],result1=0,result2=0,team2=group1[j],group=1)
                fixture1.save()
                date += timedelta(days=1)

                selected_venue = random.choice(venues)
                # Creating fixture for group1
                fixture2=Fixtures(venue=selected_venue,date=date.strftime('%Y-%m-%d'),team1=group2[i],result1=0,result2=0,team2=group2[j],group=2)
                fixture2.save()
                date += timedelta(days=1)
        return redirect('round_1')
    return render(request,'round1.html',{'count':count,'display':display,'fixture_all':fixture_all,'user':user})

# Update Match View
def update_match(request, id):
    win_point=5
    loose_point=0
    draw_point=2
    fixture = get_object_or_404(Fixtures, id=id)
    team1=CustomUser.objects.get(username=fixture.team1)
    team2=CustomUser.objects.get(username=fixture.team2)
    if request.method == 'POST':
        result1=request.POST['result1']
        result2=request.POST['result2']

        # Update fixture results
        fixture.result1=result1
        fixture.result2=result2
        fixture.save()

        # Update team goals
        team1.goals+=int(result1)
        team1.save()
        team2.goals+=int(result2)
        team2.save()
        if result1<result2:
            # Updating teams points and also only updating win in semifinals and finals
            if fixture.round == 'Semi-Finals' or 'Finals':
                team1.win=False
            team1.points+=loose_point
            team1.save()
            if fixture.round == 'Semi-Finals' or 'Finals':
                team2.win=True
            team2.points+=win_point
            team2.save()
        elif result1 == result2:
            team1.points+=draw_point
            team1.save()
            team2.points+=draw_point
            team2.save()
        else:
            if fixture.round == 'Semi-Finals' or 'Finals':
                team1.win=True
            team1.points+=win_point
            team1.save()
            if fixture.round == 'Semi-Finals' or 'Finals':
                team2.win=False
            team2.points+=loose_point
            team2.save()
        fixture.updated=True
        fixture.save()
        print('result1',result1,'result2',result2)
        # Redirect to the appropriate view based on the round
        if fixture.round == 'Semi-Finals':
            return redirect('semifinals')
        if fixture.round == 'Finals':
            return redirect('finals')
        return redirect('round_1')
    return render(request, 'round1.html', {'fixture': fixture})

# Semi-Finals View
def semifinals(request):
    venues = ['Kerala', 'Kolkata', 'Goa', 'Bangaluru', 'Mumbai']
    semifinal_fixtures=Fixtures.objects.filter(round='Semi-Finals').order_by('date')
    round1_matches_completed=Fixtures.objects.filter(round='Round 1',updated=True).count()
    print('round1_matches_completed',round1_matches_completed)
     # Check if Semi-Finals fixtures have been created
    if not semifinal_fixtures:
        # Checking all the matches in Round 1 has completed
        if round1_matches_completed >19:
            last_day_of_round1=Fixtures.objects.filter(round='Round 1').last()
            date_str = last_day_of_round1.date
            date_obj = datetime.strptime(date_str,'%Y-%m-%d')
            date = date_obj+timedelta(days=3)

            team_semi = list(CustomUser.objects.filter(is_superuser = False).order_by('-points')[:4])
            bottom_teams = CustomUser.objects.filter(is_superuser=False).order_by('-points')[4:10]

            fourth_position_points=team_semi[3].points
            print('Team @ 4th position',team_semi[3],':',team_semi[3].points)
            
            fourth_position = CustomUser.objects.filter(points=fourth_position_points)
            bottom_teams_with_same_points = [team for team in bottom_teams if team.points == fourth_position_points]
            # Handle tie-breaker logic if multiple teams have the same points and goals
            print('teams that have same points as the team in 4th position',bottom_teams_with_same_points)

            if len(bottom_teams_with_same_points) > 1:
                max_goals_team = None
                max_goals = 0

                for team in bottom_teams_with_same_points:
                    if team.goals > max_goals:
                        max_goals = team.goals
                        max_goals_team = team
                team_semi[3]=max_goals_team
            print('right team for the 4th position is:',team_semi[3])
            
            CustomUser.objects.all().update(win=False)
            selected_venue = random.choice(venues)
             # Create Semi-Finals fixture 1
            fixture1 = Fixtures(
                venue=selected_venue,
                date=date.strftime('%Y-%m-%d'),
                team1=team_semi[0].username,
                result1=0,
                result2=0,
                team2=team_semi[1].username,
                group=1,
                updated=False,
                round='Semi-Finals'
            )
            fixture1.save()
            date += timedelta(days=1)

            selected_venue = random.choice(venues)
             # Create Semi-Finals fixture 2
            fixture2 = Fixtures(
                venue=selected_venue,
                date=date.strftime('%Y-%m-%d'),
                team1=team_semi[2].username,
                result1=0,
                result2=0,
                team2=team_semi[3].username,
                group=2,
                updated=False,
                round='Semi-Finals'
            )
            fixture2.save()
            return redirect('semifinals')
        else:
            return render(request,'semifinals.html',{'semifinal_fixtures':semifinal_fixtures})

    else:
        return render(request,'semifinals.html',{'semifinal_fixtures':semifinal_fixtures})

# Finals View
def finals(request):
    venue = 'Kerala'
    winner=None
    final_fixtures = Fixtures.objects.filter(round='Finals')
    # Check if Finals fixture exists
    if final_fixtures:
        print('final_fixtures')
        for i in final_fixtures:
            team1=i.team1
            team2=i.team2
            update=i.updated
        if update:
            # Check which team has won in the final
            team1_won = CustomUser.objects.filter(username=team1, win=True).exists()
            team2_won = CustomUser.objects.filter(username=team2, win=True).exists()
            print('team1_won:',team1_won,'team2_won:',team2_won,'update:',update)
            if team1_won:
                winner = team1
            elif team2_won:
                winner = team2
            print('the winner is:',winner)
        
    semifinal_matches_completed = Fixtures.objects.filter(round = 'Semi-Finals',updated=True).count()
    print('semifinal_matches_completed',semifinal_matches_completed)
    # Checking if Finals fixture needs to be created
    if not final_fixtures:
        if semifinal_matches_completed >1:

            last_day_of_semifinals=Fixtures.objects.filter(round='Semi-Finals').last()
            date_str = last_day_of_semifinals.date
            date_obj = datetime.strptime(date_str,'%Y-%m-%d')
            date = date_obj+timedelta(days=3)
            print('this is where final fixtere created-----------------------')
            team_final=list(CustomUser.objects.filter(is_superuser = False,win=True))
            print('team_final',team_final)
            fixture1 = Fixtures(
                venue=venue,
                date=date.strftime('%Y-%m-%d'),
                team1=team_final[0].username,
                result1=0,
                result2=0,
                team2=team_final[1].username,
                group=1,
                updated=False,
                round='Finals'
            )
            fixture1.save()
            return redirect('finals')
        else:
            return render(request,'finals.html',{'final_fixtures':final_fixtures})
    else:
        return render(request,'finals.html',{'final_fixtures':final_fixtures,'winner':winner})