import random

from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Board(models.Model):
    PROGRAMMING = 'Programming'
    DRAWING = 'Drawing'
    MUSIC = 'Music'

    CATEGORIES = (
        (PROGRAMMING, 'Programming'),
        (DRAWING, 'Drawing'),
        (MUSIC, 'Music'),
    )

    name = models.CharField(max_length=100, verbose_name="Board's name")
    type = models.CharField(max_length=15, choices=CATEGORIES, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, verbose_name="Board's token",
                             default=hash(str(name) + str(random.randint(1111111, 9999999))), unique=True)


class Column(models.Model):
    name = models.CharField(max_length=100, verbose_name="Column's name")
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Board's name")
    description = models.TextField(max_length=500)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(verbose_name="Task's image")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Mark(models.Model):
    name = models.CharField(max_length=100, verbose_name="Mark's name")
    colour = models.CharField(max_length=50, verbose_name="Mark's colour")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskParticipate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Teammate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
