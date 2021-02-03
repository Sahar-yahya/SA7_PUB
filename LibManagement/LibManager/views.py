from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import datetime
from django.shortcuts import get_object_or_404

import re

from django.db.models import Q

# Create your views here.

def home(request):
    return render(request,'home.html')



#book list 
def BookListView(request):
    book_list = Book.objects.all()
    return render(request, 'BooksCatalog/book_list.html', locals())



#Book List for each member 
@login_required
def MemberBookListView(request):
    member=Member.objects.get(roll_no=request.user)
    bor=Borrower.objects.filter(member=member)
    book_list=[]
    for b in bor:
        book_list.append(b.book)
    return render(request, 'BooksCatalog/book_list.html', locals())


#book details
def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews=Reviews.objects.filter(book=book).exclude(review="none")
    try:
        stu = Member.objects.get(roll_no=request.user)
        rr=Reviews.objects.get(review="none")
    except:
        pass
    return render(request, 'BooksCatalog/book_detail.html', locals())


def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'description','author'])

        book_list= Book.objects.filter(entry_query)

    return render(request,'BooksCatalog/book_list.html',locals() )





def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]






def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'description','author'])

        book_list= Book.objects.filter(entry_query)

    return render(request,'BooksCatalog/book_list.html',locals() )