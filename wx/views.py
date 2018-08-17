import hashlib

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic

def index(request):

    try:
        if len(request.POST) == 0:
            return HttpResponse("hello, this is handle view")
        signature = request.POST['signature']
        timestamp = request.POST['timestamp']
        nonce = request.POST['nonce']
        echostr = request.POST['echostr']
        token = "zhoukuniyc"  # 请按照公众平台官网\基本配置中信息填写

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("")
    except Exception as Argument:
        return HttpResponse(Argument)

class IndexView(generic.ListView):
    template_name = 'wx/index.html'
    context_object_name = 'hello world'


    def get_queryset(self):
        """Return the last five published questions."""
        return self.context_object_name;

