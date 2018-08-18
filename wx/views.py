import hashlib

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic

def index(request):

    try:
        if len(request.GET) == 0:
            return HttpResponse("hello, this is handle view")
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        token = "zhoukuniyc"  # 请按照公众平台官网\基本配置中信息填写

        list = [token, timestamp, nonce]
        list.sort()
        list = ''.join(list)
        hashcode = hashlib.sha1(list.encode()).hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('check err')
    except Exception as Argument:
        return HttpResponse(Argument)

class IndexView(generic.ListView):
    template_name = 'wx/index.html'
    context_object_name = 'hello world'


    def get_queryset(self):
        """Return the last five published questions."""
        return self.context_object_name;

