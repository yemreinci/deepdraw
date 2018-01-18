from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import exceptions
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from learning.helpers import b64_to_np_array, predict
from web.models import Image
import numpy as np
import json
import base64


def index(request):
    return render(request, 'web/index.html')


@login_required(redirect_field_name='next', login_url='login')
@csrf_exempt
def train(request, label='-'):
    if request.method == 'GET':
        images = Image.objects.filter(user=request.user, label=label)

        return render(request, 'web/train.html', {'images': images, 'label': label})
    elif request.method == 'POST':
        if label == '-':
            return HttpResponse(status=404)

        image = Image()

        image.data = json.loads(request.body.decode('utf-8')).get('data')
        image.user = request.user
        image.label = label

        image.save()

        return render(request, 'web/image.html', {'id': image.id})


@csrf_exempt
def test(request):
    if request.method == 'GET':
        return render(request, 'web/test.html')
    elif request.method == 'POST':
        b64data = json.loads(request.body.decode('utf-8')).get('data')

        prediction = predict(b64_to_np_array(b64data))

        return HttpResponse(str(prediction))


def image_data(request, id):
    image = get_object_or_404(Image, id=id)

    return HttpResponse(content_type='image/jpeg', content=base64.b64decode(image.data))


def image(request, id):
    image = get_object_or_404(Image, id=id)

    return render(request, 'web/image_view.html', {'image': image})


@login_required(redirect_field_name='next', login_url='login')
def image_delete(request, id):
    image = get_object_or_404(Image, id=id)

    if image.user != request.user:
        raise exceptions.PermissionDenied()

    label = image.label
    image.delete()

    return redirect('train', label=label)


@login_required(redirect_field_name='next', login_url='login')
def stats(request):
    if not request.user.is_staff:
        raise exceptions.PermissionDenied()

    images = Image.objects.all()
    users = User.objects.all()

    user_to_ind = dict()
    for user in users:
        user_to_ind[user.id] = len(user_to_ind)

    n_users = len(user_to_ind)
    cnt = np.zeros((10, n_users+1), dtype=np.int32)

    for image in images:
        if image.label != '-':
            cnt[int(image.label), user_to_ind[image.user.id]] += 1
            cnt[int(image.label), n_users] += 1

    return render(request, 'web/stats.html', {'count': cnt, 'users': users})


class Login(View):
    def get(self, request):
        return render(request, 'web/login.html')

    def post(self, request):
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        if user is None:
            return redirect('login')
        else:
            login(request, user)

            return redirect(request.GET.get('next') or 'index')