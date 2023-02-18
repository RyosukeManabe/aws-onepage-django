from django.shortcuts import render
import os
import payjp
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from account.models import User,Hp_profile,Insta_profile,Card


@csrf_exempt
def formfunc(request):
  payjp.api_key = getattr(settings, "PAYJP_SECRETKEY", None)
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    agency_id_obj = request.POST.get('agency_id')
    name_obj = request.POST.get('name')
    name_ruby_obj = request.POST.get('name_ruby')
    phone_obj = request.POST.get('phone')
    post_obj = request.POST.get('post')
    prefectures_obj = request.POST.get('prefectures')
    address_obj = request.POST.get('address')
    insta_id_obj = request.POST.get('insta_id')
    insta_pass_obj = request.POST.get('insta_pass')
    insta_plan_obj = request.POST.get('insta_plan')

    user_obj = User.objects.create_user(email,password)
    user_insta_profile =Insta_profile(
      user=user_obj,
      email=user_obj.email,
      agency_id=agency_id_obj,
      name=name_obj,
      name_ruby=name_ruby_obj,
      phone=phone_obj,
      post=post_obj,
      prefectures=prefectures_obj,
      address=address_obj,
      insta_id=insta_id_obj,
      insta_pass=insta_pass_obj,
      insta_plan=insta_plan_obj
      )
    user_insta_profile.save()

    payjp_token = request.POST.get("payjp-token")
    customer = payjp.Customer.create(card=payjp_token)
    Subscription =payjp.Subscription.create(
      customer= customer.id,
      plan=user_insta_profile.insta_plan
    )

    card_obj =Card(
      user =user_obj,
      card_token=payjp_token,
      customer_id=customer.id,
      email =user_obj.email,
      sub_id=Subscription.id
    )
    card_obj.save()

    return render(request, 'thanks.html', {'message':'定期課金登録'})
  return render(request, 'insta_form.html')

def termsfunc(request):
  return render(request, 'terms.html')

def privacypolicyfunc(request):
  return render(request, 'privacy-policy.html')

def rootfunc(request):
  return render(request, 'root.html')