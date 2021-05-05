# encoding:utf-8
from django.db import models
from abc import ABC, abstractmethod


def __repr_format(instance):
    """
    Generic format for Models objects.
    Return an assessable format of the object.

    :param instance:
    :return:
    """
    attrs = []
    for key in instance.__dict__:
        if key not in ["_state", "id"]:
            attrs.append(key)
    params_repr = ', '.join(["{}={}".format(key, repr(getattr(instance, key))) for key in attrs])
    return f"{type(instance).__name__}=({params_repr})"


def __str_format(instance):
    """
    generic format for Models Objects. Return the 'name' attribute. If it not exists, return the standard format of
    ModelBase class.

    :param instance:
    :return:
    """
    try:
        return instance.name
    except AttributeError:
        return instance.super().__str__()


# Monkey patching for avoiding multiple inheritances and meta class problems.
models.Model.__repr__ = __repr_format
models.Model.__str__ = __str_format


class Category(models.Model):
    """
    Catégorie du livre.
    """
    name = models.CharField(max_length=200)
    image = models.FilePathField()


class Book(models.Model):
    """
    Livre lui meme.
    """
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)


class Chapter(models.Model):
    """
    Chapitre d'un livre.
    """
    name = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    rank = models.IntegerField(null=True)


class SubChapter(models.Model):
    """
    Sous chapitre d'un chapitre d'un livre.
    """
    name = models.CharField(max_length=200)
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="sub_chapters")
    rank = models.IntegerField(null=True)


class BookImage(models.Model):
    """
    Image contenue par un livre
    """
    name = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")
    path = models.TextField()
