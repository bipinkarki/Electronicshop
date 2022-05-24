from email.policy import default
from sqlite3 import Timestamp
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.

def index(request):
    product = Product.objects.all()
    # n = len(product)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # #Placing the items cateogry wise :
    allProds=[]
    catprods=Product.objects.values('category', 'id')
    # print(catprods)
    cats={item["category"] for item in catprods}
    # print(cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        # print(prod)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': product}
    # allProds = [
    #     [product, range(1, nSlides), nSlides],
    #     [product, range(1, nSlides), nSlides]
    # ]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def tracker(request):
    if(request.method=='POST'):        
        orderId=request.POST.get('orderId', '')
        email=request.POST.get('email','')
        try:
            order=Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                response=json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')

        except Exception as e:
            return HttpResponse('{}')
            
    return render(request, 'shop/tracker.html')
   

    


def search(request):
    return render(request, 'shop/search.html' )


def productView(request, myid):
    product=Product.objects.filter(id=myid)
    params={'product':product[0]}
    return render(request, 'shop/prodView.html', params )


def checkout(request):
    if(request.method=='POST'):
        items_json=request.POST.get('items_Json','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address1', '')+request.POST.get('address2','')
        city=request.POST.get('city', '')
        zip_code=request.POST.get('zip_code','')
        state=request.POST.get('state','')

        order=Orders(items_json=items_json, name=name, email=email, phone=phone, address=address, city=city, zip_code=zip_code, state=state)
        order.save()
        update=OrderUpdate(order_id=order.order_id, update_desc='Your order has been saved here.')
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html' )
