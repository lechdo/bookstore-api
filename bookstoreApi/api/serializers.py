from rest_framework import serializers
from .models import Category, Book, Chapter, SubChapter, BookImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'categories']


class ChapterSerialier(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['name', 'book']


class SubChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubChapter
        fields = ['name', 'content', 'chapter']


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ['name', 'path', 'book']
