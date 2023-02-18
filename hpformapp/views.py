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
    new_obj = request.POST.get('new')
    site_url_obj = request.POST.get('site_url')
    company_name_obj = request.POST.get('company_name')
    manager_name_obj = request.POST.get('manager_name')
    phone_obj = request.POST.get('phone')
    post_obj = request.POST.get('post')
    address_obj = request.POST.get('address')
    company_overview_obj = request.POST.get('company_overview')
    hope_domain_obj = request.POST.get('hope_domain')
    site_image_obj = request.POST.get('site_image')
    site_image_text_obj = request.POST.get('site_image_text')
    color_obj = request.POST.get('color')
    color_text_obj = request.POST.get('color_text')
    business_obj = request.POST.get('business')
    menu_obj = request.POST.get('menu')
    strength_obj = request.POST.get('strength')
    keyword_obj = request.POST.get('keyword')
    image_data_obj = request.POST.get('image_data')
    hp_plan_obj = request.POST.get('hp_plan')

    user_obj = User.objects.create_user(email,password)
    user_hp_profile = Hp_profile(
      user=user_obj,
      email=user_obj.email,
      new=new_obj,
      site_url=site_url_obj,
      company_name=company_name_obj,
      manager_name=manager_name_obj,
      phone=phone_obj,
      post=post_obj,
      address=address_obj,
      company_overview=company_overview_obj,
      hope_domain=hope_domain_obj,
      site_image=site_image_obj,
      site_image_text=site_image_text_obj,
      color=color_obj,
      color_text=color_text_obj,
      business=business_obj,
      menu=menu_obj,
      strength=strength_obj,
      keyword=keyword_obj,
      image_data=image_data_obj,
      hp_plan=hp_plan_obj
      )
    user_hp_profile.save()

    payjp_token = request.POST.get("payjp-token")
    customer = payjp.Customer.create(card=payjp_token)
    Subscription =payjp.Subscription.create(
      customer= customer.id,
      plan=user_hp_profile.hp_plan
    )

    card_obj =Card(
      user =user_obj,
      card_token=payjp_token,
      customer_id=customer.id,
      email =user_obj.email,
      sub_id=Subscription.id
    )
    card_obj.save()

    return render(request, 'thanks.html', {'message':'ユーザー登録が完了しました'})
  return render(request, 'hp_form.html')