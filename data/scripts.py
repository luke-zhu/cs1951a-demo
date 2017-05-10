# Run these in python3 manage.py shell

import json
import spotipy

from visualizations.models import *

def transform_artists_and_genres():
    artists = set()
    with open('data/billboard_albums.json') as f1:
        data = json.load(f1)
        artists.update([d['artist'] for d in data])

    with open('data/billboard_songs.json') as f2:
        data = json.load(f2)
        artists.update([d['artist'] for d in data])

    with open('data/metacritic_albums.json') as f3:
        data = json.load(f3)
        artists.update([d['artist'] for d in data])


    artists = [a.lower() for a in artists if 'featuring' not in a.lower()]

    sp = spotipy.Spotify()

    # print(sp.search('artist:three 6 mafia', type='artist')['artists']['items'][0])

    django_artists = []
    django_genres = set()
    added_artists = set()

    for artist in artists:
        results = sp.search(q='artist:{}'.format(artist), type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            django_genres.update(items[0]['genres'])
            if items[0]['name'] not in added_artists:
                added_artists.add(items[0]['name'])
                django_artists.append({
                    'name': items[0]['name'],
                    'spotify_popularity': items[0]['popularity'],
                    'genres': items[0]['genres'],
                })
            print('Already added: {}'.format(artist))
        else:
            print('Not Found: {}'.format(artist))

    with open('data/django_artists.json', 'w') as outfile:
        json.dump(django_artists, outfile)

    with open('data/django_genres.json', 'w') as outfile:
        json.dump(list(django_genres), outfile)

def add_artists():
    with open('data/django_artists.json') as f:
        artists = json.load(f)

    for artist in artists:
        a = Artist(name=artist['name'],
            spotify_popularity=artist['spotify_popularity'])
        a.save()
        for genre in artist['genres']:
            g = Genre.objects.get(name=genre)
            a.genres.add(g)

def add_albums():
    with open('data/metacritic_albums.json') as f:
        albums = json.load(f)

    sp = spotipy.Spotify()

    for album in albums[883:]:
        results = sp.search(q='artist:{}'.format(album['artist']), type='artist')
        items = results['artists']['items']

        if len(items) > 0:
            spotify_name = items[0]['name']
            try:
                a = Album(name=album['album'],
                    artist=Artist.objects.get(name=spotify_name),
                    metacritic_score=album['score'],
                    metacritic_url=album['url'])
                a.save()
            except: #!!!!!
                print(spotify_name)
        else:
            print(album['artist'])

def add_reddit_posts():
    with open('data/reddit_top_posts.json') as f:
        posts = json.load(f)

    for post in posts:
        p = RedditPost(title=post['title'],
            comments_url=post['comments_url'],
            post_datetime=post['datetime'],
            post_score=post['score'],
            num_comments=post['num_comments'])
        p.save()

def add_genius_posts():
    posts = []
    for i in range(1, 7):
        with open('data/genius-{}.json'.format(i)) as f:
            posts += json.load(f)

    for post in posts:
        p = GeniusPost(title=post['title'],
            comments_url=post['url'],
            num_comments=post['num_comments'],
            last_comment_datetime=post['datetime'],
            post_score=post['score'],
            excerpt=post['excerpt'])
        p.save()

def add_album_chart_ranks():
    with open('data/billboard_albums.json') as f1:
        album_ranks = json.load(f1)

    sp = spotipy.Spotify()

    artists = set()
    for rank in album_ranks:
        artists.add(rank['artist'])

    artist_dict = {}
    for artist in artists:
        results = sp.search(q='artist:{}'.format(artist), type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist_dict[artist] = items[0]['name']

    bad_entries=set()

    for rank in album_ranks:
        try:
            a = AlbumChartRank(
                album=Album.objects.get(name=rank['title']),
                chart_name='r-b-hip-hop-albums',
                week=rank['week'],
                rank=rank['rank'],
                artist=Artist.objects.get(name=artist_dict[rank['artist']]))
            a.save()
        except:
            bad_entries.add((rank['title'], rank['artist']))

    with open('data/bad_entries.json', 'w') as outfile:
        json.dump(list(bad_entries), outfile)

def add_song_chart_ranks():
    with open('data/billboard_songs.json') as f2:
        song_ranks = json.load(f2)

    sp = spotipy.Spotify()

    artists = set()
    for rank in song_ranks:
        if 'Featuring' not in rank['artist']:
            artists.add(rank['artist'])

    artist_dict = {}
    for artist in artists:
        results = sp.search(q='artist:{}'.format(artist), type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            # print(artist_dict)
            artist_dict[artist] = items[0]['name']

    for rank in song_ranks:
        try:
            s = SongChartRank(
                song_name=rank['title'],
                chart_name='r-b-hip-hop-songs',
                week=rank['week'],
                rank=rank['rank'],
                artist=Artist.objects.get(name=artist_dict[rank['artist']]))
        except:
            print(rank['title'])
        s.save()

def main():
    add_albums()

if __name__ == '__main__':
    main()