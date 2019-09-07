import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic.base import View

from data_app.models import Summoner, Comment


class CommentWriteView(View):
    def post(self, request):
        summoner = get_object_or_404(Summoner, id=self.request.POST.get('summoner'))
        comment = self.request.POST.get('comment')

        if self.request.user.is_authenticated:
            Comment.objects.create(summoner=summoner, comment=comment, writer=self.request.user)
        else:
            Comment.objects.create(summoner=summoner, comment=comment, nickname=request.session._session['nickname'],
                                   ip_addr=request.session._session['ip'], password=self.request.POST.get('password'))

        context = {}
        return HttpResponse(json.dumps(context), content_type="application/json")


class CommentListView(View):
    def post(self, request):
        summoner = get_object_or_404(Summoner, id=self.request.POST.get('summoner'))
        order_type = self.request.POST.get('order_type')
        comment_list = []
        comment_sample = '<div class="comment"><div class="writer"><p>{}</p><p>{}</p></div><div class="comment_detail"><pre>{}</pre></div><div class="comment_set">삭제 신고</div></div>'

        if order_type == 'recent':
            comments = Comment.objects.filter(summoner=summoner).order_by('-written_date')

            for x in comments:
                if x.writer:
                    comment_list.append(comment_sample.format(x.writer.profile.nickname, str(x.written_date)[:16], x.comment))
                else:
                    comment_list.append(
                        comment_sample.format(x.nickname, str(x.written_date)[:16], x.comment))

        if order_type == 'like':
            comments = Comment.objects.filter(summoner=summoner).order_by('total')

            for x in comments:
                if x.writer:
                    comment_list.append(comment_sample.format(x.writer.profile.nickname, str(x.written_date)[:16], x.comment))
                else:
                    comment_list.append(
                        comment_sample.format(x.nickname, str(x.written_date)[:16], x.comment))

        context = {'comment_list': comment_list}
        return HttpResponse(json.dumps(context), content_type="application/json")
