# encoding: utf-8
from keyword import iskeyword
from json import loads, dumps
from os import path
from collections import MutableSequence, Mapping
from api.models import Book, Chapter, SubChapter


class FrozenJson:
    """
    Class for making object-like read only json.
    Very useful to state every dict key like an object attribute.
    """

    def __new__(cls, arg):
        if isinstance(arg, Mapping):
            return super().__new__(cls)
        elif isinstance(arg, MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self._components = {}
        for key, value in mapping.items():
            # checking if the key is a keyword.
            if iskeyword(key):
                key += '_'
            # checking if the key can be an attribute: this does not handle specials characters, only numbers.
            if not key.isidentifier():
                key = 'v_' + key
            self._components[key] = value


    def __getitem__(self, item):
        if hasattr(self._components, item):
            return getattr(self, item)
        else:
            return FrozenJson(self._components[item])

    def __repr__(self):
        return self._components

    def __str__(self):
        return self.__repr__()

    def __call__(self):
        return self._components

    def __iter__(self):
        if isinstance(self._components, MutableSequence):
            return self._components
        elif isinstance(self._components, Mapping):
            return self._components
        else:
            raise TypeError("Cet élément n'est pas une liste ou un dictionnaire.")

    def __len__(self):
        if isinstance(self._components, MutableSequence) or isinstance(self._components, Mapping):
            return len(self._components)
        else:
            raise TypeError("Cet élément n'est pas une liste ou un dictionnaire.")


def summary(dir):
    """
    Get the summary data from the directory book. Return an object-like read only json.
    :param dir:
    :return:
    """
    with open(dir + "\\summary.json", 'r', encoding="utf-8") as file:
        data = loads(file.read())
        return FrozenJson(data)


def get_book_structure(dir):
    """
    Get the chapters names and theirs ranks from the book's manifest.
    Return an object-like read only json.

    :param dir:
    :return:
    """
    sum = summary(dir)
    book = {}
    for chapter, i in sum.chapters, range(len(sum.chapters)):
        book[chapter] = {
            "name": chapter,
            "rank": i,
            "sub_chapters": get_sub_chapters(dir, chapter, sum.sub_chapters.chapter)
        }
    return FrozenJson(book)


def get_sub_chapters(dir, chapter, subchapters):
    """
    Get the subchapters names and theirs ranks from the book's manifest.
    Return an object-like read only json.

    :param dir:
    :param chapter:
    :param subchapters:
    :return:
    """
    data = {}
    for subchap, i in subchapters, range(len(subchapters)):
        with open(dir + "\\chapters\\{}\\{}".format(chapter, subchap.replace("?", "")), 'r', encoding="utf-8") as file:
            content = file.read()
        data[subchap] = {
            "name": subchap,
            "rank": i,
            "content": content
        }
    return FrozenJson(data)


def get_book(dir):
    """
    Beta version.
    Persist the book data (except the pictures) with the manifest informations.

    :param dir:
    :return:
    """
    data = get_book_structure(dir)
    book = Book(name=path.split(dir)[-1])
    book.save()

    for chapter, _ in data:
        new_chapter = Chapter(name=chapter,
                              book=book)
        new_chapter.save()
        book.chapters.add(new_chapter)
        for subchapter in getattr(data, chapter).sub_chapters.keys():
            cur_chapter = getattr(data, chapter)
            cur_subchapter = getattr(cur_chapter.sub_chapters, subchapter)
            new_subchapter = SubChapter(name=cur_subchapter.name,
                                        chapter=new_chapter,
                                        rank=cur_subchapter.rank,
                                        content=cur_subchapter.content)
            new_subchapter.save()
            new_chapter.sub_chapters.add(new_subchapter)
            new_chapter.save()
    book.save()
