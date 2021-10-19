from django.http import HttpResponse
# from .models import ALBUMS
from .models import Album, Artist, Contact, Booking


def artist(request, artist_id):
    albums = Album.objects.filter(artists=artist_id)
    artist = Artist.objects.get(pk=artist_id)
    formatted_albums = ["<li>{}</li>".format(f"<a href=../{album.id}>{album.title}</a>") for album in albums]
    # message = f"{artist.name}"
    if formatted_albums:
        message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    else:
        message = f"No album for {artist.name} yet"
    return HttpResponse(message)


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    formatted_albums = ["<li>{}</li>".format(f"<a href=store/{album.id}>{album.title}</a>") for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    return HttpResponse(message)


def listing(request):
    albums = ["<li>{}</li>".format(album['name']) for album in Album.objects.all()]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)


def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join([f"<a href=artist/{artist.id}>{artist.name}</a>" for artist in album.artists.all()])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album.title, artists)
    return HttpResponse(message)


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)

    if not albums.exists():
        message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    else:
        albums = ["<li>{}</li>".format(album.title) for album in albums]
        message = """
            Nous avons trouvé les albums correspondant à votre requête ! Les voici :
            <ul>{}</ul>
        """.format("</li><li>".join(albums))

    return HttpResponse(message)
