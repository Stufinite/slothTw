from django.http import JsonResponse
from djangoApiDec.djangoApiDec import queryString_required
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from slothTw.models import *
from django.db.models import F
import json, requests, itertools
from infernoWeb.models import User
from infernoWeb.view.inferno import user_verify
from ngram import NGram
courseNgram = NGram((i['name'] for i in Course.objects.values('name')))
teacherNgram = NGram((i['teacher'] for i in Course.objects.values('teacher')))

AMOUNT_NUM = 10
SEARCH_NUM = 20
# Create your views here.
@queryString_required(['school', 'start'])
def clist(request):
    start = int(request.GET['start']) -1
    ctype = request.GET['ctype'] if 'ctype' in request.GET else '通識'

    querySet = Course.objects.filter(school=request.GET['school'], ctype=ctype)
    length = len(querySet) // AMOUNT_NUM +1
    querySet = querySet[start:start+AMOUNT_NUM]
    result = json.loads(serializers.serialize('json', list(querySet), fields=('name', 'ctype', 'avatar', 'teacher', 'school', 'feedback_amount')))
    for r, q in zip(result, querySet):
        r['fields']['avatar'] = q.avatar.url
    return JsonResponse([{'TotalPage':length, 'school':request.GET['school'], 'ctype':ctype}] + result, safe=False)

@queryString_required(['id'])
def cvalue(request):
    try:
        result = model_to_dict(Course.objects.get(id=request.GET['id']), exclude='attendee')
        result['avatar'] = result['avatar'].url if result['avatar'] else None
        return JsonResponse(result, safe=False)
    except Exception as e:
        raise

@queryString_required(['school', 'keyword'])
def search(request):
    keyword = courseNgram.find(request.GET['keyword'])
    teacher = '' if 'teacher' not in request.GET else teacherNgram.find(request.GET['teacher'])
    try:
        target = [Course.objects.get(teacher=teacher, name=keyword)]
    except Exception as e:
        if teacher:
            target = [(i, teacherNgram.compare(teacher, i.teacher)) for i in Course.objects.filter(name=keyword)]
            target = [i[0] for i in sorted(target, key=lambda x:-x[1])]
        else:
            target = Course.objects.filter(name=keyword)
    result = json.loads(serializers.serialize('json', target, fields=('name', 'ctype', 'avatar', 'teacher', 'school', 'feedback_amount')))
    for r, t in zip(result, target):
        r['fields']['avatar'] = t.avatar.url
    return JsonResponse(result, safe=False)

# 顯示特定一門課程的留言評論
@queryString_required(['id', 'start'])
def comment(request):
    try:
        start = int(request.GET['start']) - 1
        c = Course.objects.prefetch_related('comment_set').get(id=request.GET['id'])
        comments = c.comment_set.all()[start:start+AMOUNT_NUM]

        result = []
        for i, j in zip(json.loads(serializers.serialize('json', comments, use_natural_foreign_keys=True, use_natural_primary_keys=True)), comments):
            i['fields']['likesfromuser'] = list(map(lambda x:x.author.facebookid, j.likesfromuser_set.all()))
            result.append(i)

        return JsonResponse(result, safe=False)
    except Exception as e:
        raise


@queryString_required(['id'])
@user_verify
def like(request):
    request.GET = request.GET.copy()
    request.GET['start'] = 1
    if request.POST:
        user = User.objects.get(facebookid=request.POST['id'])
        if request.POST['like'] == '1':
            target = Comment.objects.filter(id=request.GET['id'])
            target.update(like=F('like') + int(request.POST['like']))
            obj, created = LikesFromUser.objects.get_or_create(author=user)
            obj.comment.add(target[0])
            return JsonResponse({"like":'success'})
        elif request.POST['like'] == '-1':
            Comment.objects.filter(id=request.GET['id']).update(like=F('like') + int(request.POST['like']))
            LikesFromUser.objects.get(author=user).comment.remove(Comment.objects.get(id=request.GET['id']))
            return JsonResponse({"like":'success'})

@queryString_required(['id'])
@user_verify
def questionnaire(request):
    id = request.GET['id']
    c = Course.objects.get(id=id)
    if request.method == 'POST' and request.POST:
        if User.objects.get(facebookid=request.POST['id']) in c.attendee.all():
            return JsonResponse({'alreadySubmit':True})
        if 'rating' in request.POST:
            data = json.loads(request.POST['rating'])
            amount = c.feedback_amount + 1
            modelDict = {'feedback_amount':amount}
            modelDict['feedback_freedom'] = (c.feedback_freedom*(amount-1) + (data[0]*3/4 + data[1]/4)) /amount
            modelDict['feedback_GPA'] = (c.feedback_GPA*(amount-1) + data[2]) / amount
            modelDict['feedback_easy'] = (c.feedback_easy*(amount-1) + (data[3]/12 + data[4]/12  + data[7]*9/12 + data[8]/12)) / amount
            modelDict['feedback_knowledgeable'] = (c.feedback_knowledgeable*(amount-1) + data[6]) / amount
            modelDict['feedback_FU'] = (c.feedback_FU*(amount-1) + data[5]) / amount
            Course.objects.update_or_create(id=id, defaults=modelDict)
            Course.objects.get(id=id).attendee.add(User.objects.get(facebookid=request.POST['id']))
            return JsonResponse({'submitSuccess':True})

# 建立特定一門課程的留言評論
@user_verify
@queryString_required(['id'])
def CreateComment(request):
    id = request.GET['id']
    c = Course.objects.prefetch_related('comment_set').get(id=id)
    if len(c.comment_set.all().filter(author=User.objects.get(facebookid=request.POST['id'])))==0:
        Comment.objects.create(course=c, author=User.objects.get(facebookid=request.POST['id']) , create=timezone.now(), raw=request.POST['comments'], emotion=request.POST['emotion'])
        return True
    return False

def logPage(request):
    PageLog.objects.create(user=User.objects.get(facebookid=request.POST['id']), course=Course.objects.get(id=request.GET['id']), create=timezone.now())
