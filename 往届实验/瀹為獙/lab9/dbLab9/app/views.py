import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import User, Role, Perm, Ur, Pr

# Create your views here.


@csrf_exempt
def add(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
    uname = request.POST.get('uname')
    age = request.POST.get('age')
    phone = request.POST.get('phone')
    city = request.POST.get('city')
    if uname is None or len(str(uname)) == 0 \
            or age is None or len(str(age)) == 0 \
            or phone is None or len(str(phone)) == 0 \
            or city is None or len(str(city)) == 0:
        return JsonResponse({'errno': 1002, 'msg': "输入不能为空"})
    if not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', str(phone)):
        return JsonResponse({'errno': 1003, 'msg': "电话格式错误"})
    User.objects.create(uname=uname, age=age, phone=phone, city=city)
    return JsonResponse({'errno': 0, 'msg': "新增用户成功"})


@csrf_exempt
def delete(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
    uid = request.POST.get('uid')
    if uid is None or len(str(uid)) == 0:
        return JsonResponse({'errno': 1002, 'msg': "输入不能为空"})
    user = User.objects.get(pk=uid)
    user.delete()
    return JsonResponse({'errno': 0, 'msg': "删除用户成功"})


@csrf_exempt
def alter(request):
    if not request.method == 'POST':
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
    uid = request.POST.get('uid')
    if uid is None or len(str(uid)) == 0:
        return JsonResponse({'errno': 1002, 'msg': "输入不能为空"})
    user = User.objects.get(pk=uid)
    uname = request.POST.get('uname')
    age = request.POST.get('age')
    phone = request.POST.get('phone')
    city = request.POST.get('city')
    if uname is None or len(str(uname)) == 0 \
            or age is None or len(str(age)) == 0 \
            or phone is None or len(str(phone)) == 0 \
            or city is None or len(str(city)) == 0:
        return JsonResponse({'errno': 1002, 'msg': "输入不能为空"})
    if not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', str(phone)):
        return JsonResponse({'errno': 1003, 'msg': "电话格式错误"})
    user.uname = uname
    user.age = age
    user.phone = phone
    user.city = city
    user.save()
    return JsonResponse({'errno': 0, 'msg': "修改用户成功"})


@csrf_exempt
def search(request):
    user = User.objects.all()
    user_re = []
    user_size = len(user)
    if user_size == 0:
        return JsonResponse({'errno': 1013, 'msg': "没有符合条件的视频"})
    for i in range(user_size):
        user_re.append(user[i].to_dic())
    return JsonResponse({'errno': 0, 'msg': "查找用户成功", 'cnt': user_size, 'info': user_re})
