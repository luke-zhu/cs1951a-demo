from django.db import models

# Create your models here.

# Spotify Data

class Genre(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

class Artist(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    spotify_popularity = models.IntegerField()
    genres = models.ManyToManyField(Genre)

# Metacritic Data

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, primary_key=True)
    release_date = models.DateField(null=True)
    metacritic_score =  models.IntegerField()
    metacritic_url = models.URLField()

# Reddit Data

class RedditPost(models.Model):
    title = models.CharField(max_length=300)
    comments_url = models.URLField()
    datetime = models.DateTimeField(null=True)
    post_score = models.IntegerField()
    num_comments = models.IntegerField()

# Genius Data

class GeniusPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=200)
    comments_url = models.URLField()
    datetime = models.DateTimeField(null=True)
    post_score = models.IntegerField()
    num_comments = models.IntegerField()

# Chart Data

class AlbumChartRank(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE) 
    chart_name = models.CharField(max_length=100)
    week = models.DateField()
    rank = models.IntegerField()

class SongChartRank(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=200)
    chart_name = models.CharField(max_length=100)
    week = models.DateField()
    rank = models.IntegerField()
