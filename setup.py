import setuptools
from os import environ, curdir, path
from importlib import reload
import bookstoreApi as application

try:
    version = environ["CI_COMMIT_TAG"]
except KeyError:
    version = 'test-mode'

def overload_version():
    with open(f"{curdir()/application.__name__}/__init__.py", 'r', encoding='utf-8') as file:
        content = file.read()
    content.replace(f"__version__ = {repr(application.__version__)}", f"__version__ = {repr(version)}")
    with open(f"{path.abspath(curdir())}/{application.__name__}/__init__.py", 'w', encoding='utf-8') as file:
        file.write(content)
    reload(application)

overload_version()

setuptools.setup(
    name="bookstoreApi",
    version=version,
    author="Julien Vince",
    author_email="julien.vince@gmail.com",
    description="API pour la lecture de livres",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
