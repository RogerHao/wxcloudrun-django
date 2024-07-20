import json
import logging
import hashlib

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger('log')

# Handle the wechat request
@csrf_exempt  # This decorator is used to exempt this view from CSRF protection
def wechat(request):
    # Check if the request method is POST
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Log the received message (similar to console.log in Node.js)
            print('消息推送', data)
            
            # Check if the action is "CheckContainerPath"
            if data.get('action') == 'CheckContainerPath':
                # If it is, return a JSON response with success message and 200 status
                return JsonResponse({'message': 'success'}, status=200)
            
            # For any other case, just return a simple "success" response
            return HttpResponse('success')
        
        except json.JSONDecodeError:
            # If there's an error in parsing JSON, return an error response
            return HttpResponse('Invalid JSON', status=400)
    
    # If the request method is not POST, return a method not allowed response
    return HttpResponse('Method not allowed', status=405)


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 10
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
