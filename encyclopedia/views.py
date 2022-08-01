from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
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


def search(request):
    titles = util.list_entries()
    if request.method == "POST":
        TITLE = request.POST['q']
        for title in titles:
            if TITLE.lower() == title.lower():
                return HttpResponseRedirect(reverse("entry", kwargs={'TITLE': title}))

        results = []
        for title in titles:
            if TITLE.lower() in title.lower():
                results.append(title)

        if len(results) > 0:
            return render(request, "encyclopedia/search.html", {
                "results": results,
                "is_match": True,
            })

    return render(request, "encyclopedia/search.html", {
        "results": titles,
        "is_match": False,
    })
