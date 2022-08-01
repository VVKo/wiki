from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title",
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="Text", widget=forms.Textarea(attrs={'class': 'form-control'}))


class EditEntryForm(forms.Form):
    title = forms.CharField(label="Title",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    body = forms.CharField(label="Text", widget=forms.Textarea(attrs={'class': 'form-control'}))


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


def create(request):
    titles = util.list_entries()
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            TITLE = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            for title in titles:
                if TITLE.lower() == title.lower():
                    return render(request, "encyclopedia/new-entry.html", {
                        "form": form,
                        'alert': "Entry with current title already exist!!"
                    })

            util.save_entry(TITLE, body)
            return render(request, "encyclopedia/new-entry.html", {
                "form": NewEntryForm()
            })

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new-entry.html", {
                "form": form
            })
    return render(request, "encyclopedia/new-entry.html", {
        "form": NewEntryForm()
    })


def edit(request, TITLE):
    content = util.get_entry(TITLE)

    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = EditEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            TITLE = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            util.save_entry(TITLE, body)
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown2.markdown(util.get_entry(TITLE)),
                "title": TITLE
            })

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit-entry.html", {
                "form": form
            })

    return render(request, "encyclopedia/edit-entry.html", {
        "form": EditEntryForm(initial={'title': TITLE, 'body': content})
    })
