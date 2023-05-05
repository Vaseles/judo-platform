from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404

from ..models import Tournament, Logos, WeightCategory, Sponsors, Weight
from ..forms import TournamentForm, WeightCategoryForm
from ..utils import slug_generator, checking_slug, generate_slug
from ..services import get_tournaments, get_all_weight_category, get_user_profile
from ..filters import TournamentFilter


def show_tournaments(request):
   tournaments = get_tournaments()
   
   filter = TournamentFilter(request.GET, queryset=tournaments)
   tournaments = filter.qs
   
   context = {
      'filter': filter,
      'tournaments': tournaments,     
   }
   return render(request, 'base/tournaments/show_tournaments.html', context)
   
def tournamet_show(request, slug):
   tournament = get_object_or_404(Tournament, slug=slug)
   person_count = 0
   
   for tournamen in tournament.weight_categories.all():
      person_count += tournamen.participants.count()
   
   context = {
      'tournament': tournament,
      
      'person_count': person_count
   }
   return render(request, 'base/tournaments/show_tournament.html', context)

@csrf_exempt
@login_required(login_url= 'base:login')
def create_tournamets(request):
   page_type = 'create_tournament__part__one'
   
   if (request.user.profile.userType == 'Админ' or request.user.profile.userType == 'Секретарь' or request.user.is_superuser):
      form = TournamentForm()
                     
      if request.method == 'POST':
         form = TournamentForm(request.POST, request.FILES)
         
         if form.is_valid():
            slug = checking_slug(slug_generator(form.cleaned_data.get('title')))
            
            article = form.save(commit=False)
            
            article.user = request.user
            article.slug = slug
            
            article.save()
            return redirect('base:create_tournamets__images', article.slug)
   
      context = {
         'form': form,
         'page_type': page_type
      }
      return render(request, 'base/tournaments/create_tournament.html', context)
   else:
      messages.error(request, "You don't have permission to create tournament ;)")
      return redirect('base:show_tournaments')
   
@csrf_exempt
@login_required(login_url= 'base:login')
def create_tournamets__images(request, slug):
   page_type = 'create_tournament__part__two'   
   
   if (request.user.profile.userType == 'Админ' or request.user.is_superuser or request.user.profile.userType == 'Секретарь'):
      tournire = get_object_or_404(Tournament, slug=slug)
      weight_categories_all = WeightCategory.objects.all()
      
      if request.method == 'POST':
         logotips = request.FILES.getlist('files')
         sponsors_logotips = request.FILES.getlist('sponsors-logotips')
         weight_categoriees = request.POST.getlist('weight-categories')
         
         # Weight Categories
         if (len(weight_categoriees) > 0):
            for weight_category in weight_categoriees:
               tournire.weight_categories.add(weight_category)
         
          # Add Logotips and Photos
         if (len(logotips) > 0):
            for logo in logotips:
               new_file = Logos(image = logo)
               
               new_file.save()  
               tournire.logos.add(new_file)
            
         # Add Sponsor Emblems
         if (len(sponsors_logotips) > 0):
            for logo in sponsors_logotips:
               new_file = Sponsors(image = logo)
               
               new_file.save()
               tournire.sponsors.add(new_file)
               
         tournire.save()   
         return redirect('base:tournamets_admin_update_info', tournire.slug)
   
      context = {
         'page_type': page_type,
         
         'tournire': tournire,
         'weight_categories_all': weight_categories_all
      }
      return render(request, 'base/tournaments/create_tournament.html', context)
   else:
      messages.error(request, "You don't have permission to create tournament ;)")
      return redirect('base:show_tournaments')

# Weight Category
@login_required(login_url='base:login')
def weight_categories(request):
   # get data and form
   weight_categories = get_all_weight_category()
   form = WeightCategoryForm()
   
   # get data from form
   if request.method == 'POST':
      form = WeightCategoryForm(request.POST)
      
      # validation checking
      if form.is_valid():
         category = form.save()
         
         return redirect('base:weight_category_weight', category.id)
         
   context = {
      'weight_categories': weight_categories,
      'form': form
   }
   return render(request, 'base/tournaments/weight_categories.html', context)
      
@login_required(login_url='base:login')
def weight_category_weight(request, id):
   weight_category = WeightCategory.objects.get(id=id)
   
   if request.method == 'POST':
      weight = request.POST.get('weight')
      
      if weight is not None and len(weight) > 1 and len(weight) < 3:
         weight_type = Weight.objects.create(
            name=weight
         )
         
         weight_type.save()

         weight_category.weight.add(weight_type.id)
         weight_category.save()
         return redirect('base:weight_category_weight', weight_category.id)
      else:
         messages.error(request, 'Error creating weight category')
         
      # return redirect('base:weight_categories')
   
   context = {
      'weight_category': weight_category
   }
   return render(request, 'base/tournaments/weight_add.html', context)

@login_required(login_url='base:login')
def weight_category_weight_delete(request,id, weight_id):
   weight_category = WeightCategory.objects.get(id=id)
   weight = Weight.objects.get(id=weight_id)
   
   if weight:
      weight.delete()
      
      messages.success(request,'Weight category deleted successfully')
      return redirect('base:weight_category_weight', weight_category.id)
   else:
      messages.error(request,'Weight category not found')
      return redirect('base:weight_category_weight', weight_category.id)

#Weight Categories Delete
@login_required(login_url='base:login')
def weight_categories_delete(request, pk):
   weight_category = get_object_or_404(WeightCategory, id=pk)
   
   # Delete weight category
   weight_category.delete()
   return redirect('base:weight_categories')

@login_required(login_url='base:sign-in')
def registration_on_tournament(request, slug):
   tournament = get_object_or_404(Tournament, slug=slug)
   
   user = request.user
   profile = get_user_profile(user)
   
   participants = Participant.objects.filter(user=user) 
   
   context = {
      'tournament': tournament,
      'user': user,
      'profile': profile,
      
      'participants': participants
   }
   return render(request, 'base/tournaments/athlete_registration.html', context)