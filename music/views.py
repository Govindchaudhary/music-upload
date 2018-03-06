from django.views import generic
from .models import Album,Song
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.views.generic import View
from.forms import UserForm,LoginForm
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.db.models import Q


 


def index(request):
    if not request.user.is_authenticated():
        return redirect( 'music:login')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()  #Returns a new QuerySet that uses SELECT DISTINCT in its SQL query. This eliminates duplicate rows from the query results.
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})

class DetailView(generic.DetailView):
      model = Album
      template_name = 'music/detail.html'
      

class AlbumUpdate(UpdateView):
      model = Album
      fields = ['artist','album_title','genre','album_logo']


class AlbumCreate(CreateView):
      model = Album
      fields = ['artist','album_title','genre','album_logo']


class AlbumDelete(DeleteView):
      model = Album
      success_url = reverse_lazy('music:index')


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})

class UserFormView(View):
       form_class = UserForm
       template_name = 'music/registration_form.html'

       # display blank form
       def get(self,request):
            form = self.form_class(None)
            return render(request,self.template_name,{'form':form})

       # process form data
       def post(self,request):
             form = self.form_class(request.POST)
             
             if form.is_valid():
                user = form.save(commit=False)

                # cleaned (normalized) data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                
                return redirect('music:index')

               
                   
             return render(request,self.template_name,{'form':form})
           


def login_user(request):
  
      
    form = LoginForm(request.POST)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
       
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
       return render(request,'music/login_form.html', {'form':form}) 


def user_logout(request):
    logout(request)
    return redirect('music:login') 


class SongCreate(CreateView):
      model = Song
      fields = ['song_title','audio_file']
     # You need to provide the user a way to input the 'file_type' or 'song_title'
     # fields in the HTML form though,  as view requires them for form validation to pass. 
     
      def form_valid(self, form):
            #form.instance.album  is like saying song.album
            form.instance.album = Album.objects.get(pk=self.kwargs['pk'])
            return super(SongCreate, self).form_valid(form)

   
def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return redirect('music:detail',song.album.slug)


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return redirect('music:index')


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login_form.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,


            
        })








