from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .serializers import ChapterSerialier, BookSerializer
from .models import Book, Chapter, Category
from rest_framework import status
import json
from django.core import serializers


@api_view(["GET"])
@csrf_exempt
def welcome(request):
    content = {"message": "Welcome to the BookStore!"}
    return JsonResponse(content)


@api_view(["GET"])
@csrf_exempt
def get_books(request):
    books = Book.objects.all()
    return JsonResponse({"books": [
        {"id": book.id,
         "name": book.name,
         "categories": [cat.id for cat in book.categories.all()],
         } for book in books
    ]}, content_type='JSON')


@api_view(["GET"])
@csrf_exempt
def get_book(request, book_id):
    book = Book.objects.get(id=book_id)

    chapters = Chapter.objects.filter(book=book).order_by("rank")
    data = [{"id": chap.id, 'name': chap.name, 'rank': chap.rank} for chap in chapters]

    return JsonResponse({'id': book.id,
                         'name': book.name,
                         'chapters': data,
                         }, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_page(request, book_id, chapter_id, subchapter_id):
    try:
        book = Book.objects.get(id=book_id)
        # chapter = book.chapters.all().order_by("rank")[chapter_id - 1]
        chapter = book.chapters.get(id=chapter_id)
        # subchapters = chapter.sub_chapters.all()
        subchapter = chapter.sub_chapters.get(id=subchapter_id)
        # subchapter = subchapters.order_by("rank")[subchapter_id - 1]
        return JsonResponse({
            'book_id': book.id,
            'book_name': book.name,
            'chapter_id': chapter.id,
            'chapter_name': chapter.name,
            'subchapter_id': subchapter.id,
            'subchapter_name': subchapter.name,
            'subchapter_content': subchapter.content,
            'subchapters_len': len(subchapters)
        }, safe=False, status=status.HTTP_200_OK)
    except IndexError as e:
        return HttpResponseNotFound("Cette page n'existe pas: {}".format(e))


@api_view(["POST"])
@csrf_exempt
def input_book(request):
    book = Book()
    book.name = request.data['name']
    if request.data['categories']:
        [book.categories.add(Category.objects.get(id=id)) for id in request.data['categories']]
    book.save()

    return JsonResponse({'id': book.id,
                         'name': book.name,
                         'categories': [cat.id for cat in book.categories.all()],
                         }, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_categories(request):
    categories = Category.objects.all()
    return JsonResponse([
        {
            'id': cat.id,
            'name': cat.name,
            'image': cat.image,
        } for cat in categories
    ], safe=False)


@api_view(["POST"])
@csrf_exempt
def add_category(request):
    category = Category()
    category.name = request.data['name']
    category.image = request.data['image']
    category.save()
    return JsonResponse([
        {
            'id': category.id,
            'name': category.name,
            'image': category.image,
        }
    ], safe=False)
