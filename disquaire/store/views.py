from .models import Album, Artist, Contact, Booking
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ContactForm


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    # formatted_albums = ["<li>{}</li>".format(f"<a href=store/{album.id}>{album.title}</a>") for album in albums]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def listing(request):
    albums_list = Album.objects.filter(available=True).order_by('-created_at')

    paginator = Paginator(albums_list, 9)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
        'paginate': True
    }
    return render(request, 'store/listing.html', context)


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = album.artists.all()
    context = {
        'album_title': album.title,
        'artists': artists,
        'album_id': album.id,
        'thumbnail': album.picture,
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            contact = Contact.objects.filter(email=email)
            if not contact.exists():
                contact = Contact.objects.create(
                    email=email,
                    name=name
                )
                contact.save()
            album = get_object_or_404(Album, id=album_id)
            booking = Booking.objects.create(contact=contact, album=album)
            booking.save()
            album.available = False
            album.save()
            context = {
                'album_title': album.title,
            }
            return render(request, 'store/merci.html', context)
        else:
            context['errors'] = form.errors.items()
    form = ContactForm()
    context['form'] = form
    return render(request, 'store/detail.html', context)


def artist(request, artist_id):
    albums = Album.objects.filter(artists=artist_id)
    artist = get_object_or_404(Artist, pk=artist_id)
    title = f'Tous les disques de {artist.name}'
    # formatted_albums = ["<li>{}</li>".format(f"<a href=../{album.id}>{album.title}</a>") for album in albums]
    # message = f"{artist.name}"
    if not albums:
        albums = [f"No album for {artist.name} yet"]
    context = {
        'albums': albums,
        'artist': artist.name,
        'title': title
    }
    return render(request, 'store/artist.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)

    # if not albums.exists():
    #     message = "Misère de misère, nous n'avons trouvé aucun résultat !"

    if query:
        title = f"Résultats pour la requête {query}"
    else:
        title = "Tous les albums"
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)
