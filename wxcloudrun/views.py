import json
import logging
import hashlib

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt

from wechat_reply import ReplyFactory, Article

logger = logging.getLogger('log')

# Handle the wechat request
# @csrf_exempt  # This decorator is used to exempt this view from CSRF protection
def wechat(request, _):
    # Check if the request method is POST
    if request.method == 'POST' or request.method == 'post':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Log the received message (similar to console.log in Node.js)
            print('消息推送', data)
            
            # Check if the action is "CheckContainerPath"
            if data.get('action') == 'CheckContainerPath':
                # Return a simple "success" response with status 200
                return HttpResponse('success', status=200)
            
            if data.get('MsgType') == 'text':
                content = data.get('Content', '')
                from_user = data.get('FromUserName')
                to_user = data.get('ToUserName')
                
                # Create a text reply message
                reply = ReplyFactory.create_text_reply(to_user, from_user, content)
                
                # Return the reply message as a JSON response
                return HttpResponse(json.dumps(reply.to_dict()), content_type='application/json')
            
            # If the message type is not text, return an empty response
            return HttpResponse('success', status=200)
        
        except json.JSONDecodeError:
            # If there's an error in parsing JSON, we still return "success"
            # because the WeChat server only expects to see "success" or an empty response
            return HttpResponse('success', status=200)
    
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
