from django.db import models

# Create your models here.
class buglist(models.Model):

    bugname=models.CharField(u'标题',max_length=256)
    bugtxt=models.TextField(u'内容')
    pub_time=models.DateTimeField(u'发布时间',auto_now_add=True,editable=True)
    update_time=models.DateTimeField(u'更新时间',auto_now=True,null=True)
    is_del = models.BooleanField(default=0)  # 1是删除，0是未删除

    def __str__(self):
        return 'bug {}'.format(self.bugname)


class domain_ip(models.Model):
    subdomain=models.CharField(U'域名',max_length=100)
    id_del=models.BooleanField(default=0)

    def __str__(self):
        return 'domain {}'.format(self.subdomain)

class note(models.Model):
    todolist=models.TextField(u'待办事项')

    def __str__(self):
        return self.todolist
class Result(models.Model):
    domain = models.TextField()
    poc_file = models.TextField(default='', null=True)
    result = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    is_fixed = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.result

class Tasks_status(models.Model):
    domains = models.TextField()
    task_name = models.TextField()
    status = models.NullBooleanField (default=False)

    def __unicode__(self):
         return self.domains

class Req_list(models.Model):
    method = models.CharField('METHOD', max_length=5, )
    host = models.CharField('HOST', max_length=40, )
    uri = models.CharField('FILE', max_length=100, default='/', )
    url = models.TextField('URL', )
    ua = models.TextField('User-agent', )
    referer = models.TextField('REFERER', null=True)
    data = models.TextField('REQUEST BODY', null=True)
    cookie = models.TextField('COOKIE', default='', )


    class Meta:
        unique_together = (('method', 'host', 'uri',))


    def __self__(self):
        return self.url

