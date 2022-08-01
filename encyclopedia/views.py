from django.shortcuts import render
from django.http import Http404
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, TITLE):
    if TITLE not in util.list_entries():
        raise Http404
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(TITLE)),
        "title": TITLE
    })
