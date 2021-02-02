from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import datetime
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    return render(request,'home.html')