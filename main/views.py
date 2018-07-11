#coding=utf-8
import sys,os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ObjectDoesNotExist
from pocscan.library.utils import get_poc_files
from users.models import User
from main.models import buglist,domain_ip,note,Result,Tasks_status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xlwt import *
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from web.lib.utils import check_status
from web.lib.task_control import Task_control
from dj2.settings import FLOWER_API
import requests as req
# Create your views here.


def results(request):
    try:
        page = (int(request.GET['page']) - 1) * 10
        try:
            results = Result.objects.all()[::-1]
            results = results[page:(page + 10)]
            return render(request, 'reslist.html', {"results": results})
        except Exception as e:
            pass
    except Exception as e:
        numOfResult = len(Result.objects.all())
        return render(request, 'results.html', {"num": numOfResult})


def scan(request):
    """
    :param request:
        domain: 127.0.0.1,erevus.me
        poc_name: struts;
        task_name: xxxx;
    :return:{
        status:1 目标都已有扫描结果或正在扫描
        status:200 可以去扫描
    """
    if request.method == 'POST':
        domains = str(request.POST.get('domains', "dhgate.com"))
        poc_name = request.POST.get('poc_name', "")
        task_name = request.POST.get('task_name', "")
        # mode = request.POST.get('mode', 1)

        targets = list(set(domains.split(',')))
        tmp_targets = list(set(domains.split(',')))
        # 已有数据或者在扫描的目标不进行扫描
        for target in tmp_targets:
            cannt_scan_target,status = check_status(target)
            if cannt_scan_target:
                targets.remove(cannt_scan_target)
        if targets:
            Task_control().launch(targets, poc_name, task_name)
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 1})
    if request.method == 'GET':
        return render(request,'scan.html')

def save_result(request):
    try:
        target = request.POST.get('target', None)
        poc_file = request.POST.get('poc_file', None)
        result = request.POST.get('result', None)
        #Result(domain=target, poc_file=poc_file, result=result).save()
        newBug = Result.objects.create(domain=target, poc_file=poc_file, result=result)
        newBug.save()
        print("保存成功")
        return JsonResponse({"status": 200, "result": result})
    except Exception as e:
        return JsonResponse({"status": e})
def scancheck(request):
    module = request.POST.get('module')
    if module == 'pocscan':
        domains = str(request.POST.get('domains', "dhgate.com"))
        targets = list(set(domains.split(',')))
        tmp_targets = list(set(domains.split(',')))
        for target in tmp_targets:
            cannt_scan_target, status = check_status(target)
            if cannt_scan_target:
                targets.remove(cannt_scan_target)
        if targets:
            Task_control().launch(targets, "", "")
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 1})
    elif module == 'sqlmap':
        print(1)
    else:
        return JsonResponse({'status': "error"})
    return JsonResponse({'status': "200"})




def poc_list(request):
    poc_list = get_poc_files('')
    return render(request, 'poc_list.html', {"poc_list": poc_list})


def index(request):
    return render(request, 'basemain.html')


def accounts_profile(request):
    if request.method == 'POST':
        a = json.loads(request.body.decode('utf-8'))
        print(a)
        b = User.objects.get(email=request.user.email)
        b.name = a["name"]
        b.age = a["age"]
        b.iphone = a["iphone"]
        b.job = a["job"]
        b.save()
    return render(request, 'accounts_profile.html')


def projectdetail(request):
    contact_list = buglist.objects.filter(is_del=0).order_by("-id")
    paginator = Paginator(contact_list, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'buglist.html', {'contacts': contacts})


def listing(request):
    contact_list = buglist.objects.all().order_by("-id")
    paginator = Paginator(contact_list, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'contacts': contacts})

@csrf_exempt
def delbug(request):
    '''
    删除bug
    :param request:
    :return:
    '''
    if not request.user.is_authenticated: #这个在新版本中是不带()
        return HttpResponse("0")
    if request.method == "POST":
        bug_id = int(request.POST['bug_id'])
        if bug_id == "":
            return HttpResponse("bug_id is null")
        else:
            try:
                bug = buglist.objects.get(id=bug_id)
                if bug.is_del == 1:
                    return HttpResponse("bug is delect")
                else:
                    bug.is_del = 1
                    bug.save()
                    return HttpResponse("1")
            except ObjectDoesNotExist as e:
                return HttpResponse("3")

    else:
        return HttpResponse("2")



@csrf_exempt
def addbug(request):
    '''
    新增bug
    :param request:
    :return:
    '''
    if request.user == "AnonymousUser":
        return HttpResponse("0")
    if request.method == "POST":
        try:
            # project = buglist.objects.get(id=int(project_id))
            try:
                print(request.POST)
                bug_name = request.POST['bug_name']
                bug_txt = request.POST['bug_content']
                # user = request.user
                newBug = buglist.objects.create(bugname=bug_name, bugtxt=bug_txt)
                newBug.save()
                print("保存成功")
                return HttpResponse("1")
            except Exception as e:
                raise Exception()
                return HttpResponse('3')
        except ObjectDoesNotExist as e:
            return HttpResponse("2")

    if request.method == "GET":
        # 查询出所有的漏洞模板
        return render(request,"addbug.html")

def projectdetailshow(request,project_id):
    '''
    漏洞详情
    :param request:
    :return:
    '''
    try:
        print(project_id)
        project = buglist.objects.get(id=project_id)
        if project.is_del != 1:
            print(project_id)
            bugs = buglist.objects.filter(id=project_id)
            return render(request, 'projectdetailshow.html',{"bugs":bugs})
    except ObjectDoesNotExist as e:
        return HttpResponse("4")



def assetlist(request):
    contact_list = domain_ip.objects.filter().order_by('-id')
    countd=domain_ip.objects.filter().order_by('id').count()
    print(countd)
    paginator = Paginator(contact_list, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'asset_list.html', {'contacts': contacts,'countd':countd})



def addasset(request):
    '''
    新增资产
    :param request:
    :return:
    '''
    if request.user == "AnonymousUser":
        return HttpResponse("0")
    if request.method == "POST":
        try:
            try:
                print(request.POST)
                asset_domain = request.POST['asset_domain']
                # user = request.user
                newasset = domain_ip.objects.get_or_create(subdomain=asset_domain)
                print("保存成功")
                return HttpResponse("1")
            except Exception as e:
                raise Exception()
        except ObjectDoesNotExist as e:
            return HttpResponse("2")

    if request.method == "GET":
        # 查询出所有的资产
        return render(request,"asset_add.html")


def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        print (file_obj)
        import os
        file_path = os.path.join('static', 'upload', file_obj.name)
        f = open(file_path, 'wb')

        for chunk in file_obj.chunks():
            f.write(chunk)
            #domain_ip.objects.create(subdomain=chunk)
        f.close()
        with open(file_path,encoding='utf-8') as fh:
            line = fh.readline()
            while line:
                domain_ip.objects.get_or_create(subdomain=line.strip())
                line = fh.readline()


        return HttpResponse('OK')
def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break
def excel_export(request):
    """
    导出excel表格
    """
    import os
    list_obj = domain_ip.objects.all()
    if list_obj:
        # 创建工作薄
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表")
        w.write(0, 0, "id")
        w.write(0, 1, u"域名")
        # 写入数据
        excel_row = 1
        for obj in list_obj:
            data_id = obj.id
            data_domain = obj.subdomain
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_domain)
            excel_row += 1
        # 检测文件是够存在
        # 方框中代码是保存本地文件使用，如不需要请删除该代码
        ###########################
        exist_file = os.path.exists("static/upload/test.xls")
        if exist_file:
            os.remove(r"static/upload/test.xls")
        ws.save("static/upload/test.xls")
        the_file_name = 'static/upload/test.xls'  # 显示在弹出对话框中的默认的下载文件名
        filename = 'static/upload/test.xls'  # 要下载的文件路径
        response = StreamingHttpResponse(readFile(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return response

    return render(request,'asset_list.html')


def savetodo(request):
    '''
    新增资产
    :param request:
    :return:
    '''
    if request.user == "AnonymousUser":
        return HttpResponse("0")
    if request.method == "POST":
        try:
            try:
                print(request.POST)
                todotxt = request.POST['todotxt']
                # user = request.user
                print(todotxt)
                newdata=note.objects.get(id=1)
                newdata.todolist=todotxt
                newdata.save()
                print("保存成功")
                return HttpResponse("1")
            except Exception as e:
                raise Exception()
        except ObjectDoesNotExist as e:
            return HttpResponse("2")

    if request.method == "GET":
        # 查询出所有的资产
        todo = note.objects.get(id=1)
        return render(request, 'todo.html', {"toto": todo})