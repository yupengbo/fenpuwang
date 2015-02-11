from django.shortcuts import render

# Create your views here.

def order_detail(request):
    return render(request,"order/order.html")
