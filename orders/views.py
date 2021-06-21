from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from basket.basket import Basket
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['qty'])
            #order request email setup
            current_site = get_current_site(request)
            subject = 'Cokedama Order Request Confirmation'
            company_email = 'cokedama100@gmail.com'
            message = render_to_string('orders/order/email_template.html', {
                'order': order,
                'basket':basket,
                'domain': current_site.domain,
                'oid': urlsafe_base64_encode(force_bytes(order.pk)),
            })
            order.email_order(subject=subject, message=message, company_email=company_email)
            #return HttpResponse('Thank you for your order - Order Request Confirmation Sent!')
            # clear the basket
            basket.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'basket': basket, 'form': form})




