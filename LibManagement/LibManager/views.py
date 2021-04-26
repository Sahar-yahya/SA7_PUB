from django.shortcuts import render , redirect
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



def search_member(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['roll_no','name','email'])

        members= Member.objects.filter(entry_query)

    return render(request,'BooksCatalog/member_list.html',locals())



    



@login_required
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    obj = Borrower.objects.get(id=pk)
    book_pk=obj.book.id
    member_pk=obj.member.id
    member = member.objects.get(id=member_pk)
    member.total_books_due=member.total_books_due-1
    member.save()

    book=Book.objects.get(id=book_pk)
    rating = Reviews(review="none", book=book,member=member,rating='2.5')
    rating.save()
    book.available_copies=book.available_copies+1
    book.save()
    obj.delete()
    return redirect('home')




@login_required
def RatingUpdate(request, pk):
    obj =Reviews.objects.get(id=pk)
    form = RatingForm(instance=obj)
    if request.method == 'POST':
        form = RatingForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('book-detail',pk=obj.book.id)
    return render(request, 'BooksCatalog/form.html', locals())


@login_required
def RatingDelete(request, pk):
    obj = get_object_or_404(Reviews, pk=pk)
    st=Member.objects.get(roll_no=request.user)
    if not st==obj.member:
        return redirect('home')
    pk = obj.book.id
    obj.delete()
    return redirect('book_detail',pk)




#######  BOOK VIES ############




@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('home')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(home)
    return render(request, 'BooksCatalog/form.html', locals())


@login_required
def BookUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=obj)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(home)
    return render(request, 'BooksCatalog/form.html', locals())


@login_required
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('home')




######## Members Views #########



@login_required
def Member_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu=Member.objects.get(roll_no=request.user)
    s = get_object_or_404(Member , roll_no=str(request.user))
    if s.total_books_due < 10:
        message = "book has been isuued, You can collect book from library"
        a = Borrower()
        a.member = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_books_due=stu.total_books_due+1
        stu.save()
        a.save()
    else:
        message = "you have exceeded limit."
    return render(request, 'BooksCatalog/result.html', locals())


@login_required
def MemberCreate(request):
    if not request.user.is_superuser:
        return redirect('home')
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            s=form.cleaned_data['roll_no']
            form.save()
            u=User.objects.get(username=s)
            s=Member.objects.get(roll_no=s)
            u.email=s.email
            u.save()
            return redirect(home)
    return render(request, 'BooksCatalog/form.html', locals())


@login_required
def MemberUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    obj = Member.objects.get(id=pk)
    form = MemberForm(instance=obj)
    if request.method == 'POST':
        form = MemberForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(home)
    return render(request, 'BooksCatalog/form.html', locals())


@login_required
def MemberDelete(request, pk):
    obj = get_object_or_404(Member, pk=pk)
    obj.delete()
    return redirect('home')

@login_required
def MemberList(request):
    members = Member.objects.all()
    return render(request, 'BooksCatalog/Member_list.html', locals())

@login_required
def MemberDetail(request, pk):
    member = get_object_or_404(Member, id=pk)
    books=Borrower.objects.filter(member=member)
    return render(request, 'BooksCatalog/Member_detail.html', locals())

