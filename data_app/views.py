import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic.base import View

from data_app.models import Summoner, Comment, Like, CommentReport


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
        comment_sample = '<div class="comment" id="comment_{}"><div class="writer"><p>{}</p><p>{}</p></div><div class="comment_detail"><pre>{}</pre></div><div class="comment_set">삭제 신고</div></div>'

        if order_type == 'recent':
            comments = Comment.objects.filter(summoner=summoner).order_by('-written_date')

            for x in comments:
                if x.writer:
                    comment_list.append(comment_sample.format(x.id, x.writer.profile.nickname, str(x.written_date)[:16], x.comment))
                else:
                    comment_list.append(
                        comment_sample.format(x.id, x.nickname, str(x.written_date)[:16], x.comment))

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


class CommentReportView(View):
    def get_report_object(self, request, comment):
        if self.request.user.is_authenticated:
            report, created = CommentReport.objects.get_or_create(comment=comment, reporter=self.request.user)
            comment.blind_count += 1
            comment.save()
        else:
            report, created = CommentReport.objects.get_or_create(comment=comment, ip_addr=request.session._session['ip'])
        return report, created

    def post(self, request):
        comment_id = self.request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)

        report, created = self.get_report_object(self.request, comment)

        if created:
            print(self.request.POST.get('reason'))
            report.reason = self.request.POST.get('reason')
            context = {'status': 'created'}
            report.save()
        else:
            context = {'status': 'existed'}

        return HttpResponse(json.dumps(context), content_type="application/json")


class CommentDeleteView(View):
    def post(self, request):
        comment_id = self.request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        password = self.request.POST.get('password')

        if comment.writer:
            if self.request.user.is_superuser or comment.writer == self.request.user:
                comment.delete()
                context = {'status': 'success'}
            else:
                context = {'status': 'wrong_request'}

        else:
            if password == comment.password:
                comment.delete()
                context = {'status': 'success'}

            else:
                context = {'status': 'wrong_password'}

        return HttpResponse(json.dumps(context), content_type="application/json")


class LikeSubmitView(View):
    def get_like_object(self, request, comment):
        if self.request.user.is_authenticated:
            like, created = Like.objects.get_or_create(liker=self.request.user, comment=comment)
        else:
            like, created = Like.objects.get_or_create(ip_addr=self.request.session._session['ip'], comment=comment)
        return like

    def calculate_comment_like(self, request, comment):
        likes = Like.objects.filter(comment=comment, like=True, dislike=False).count()
        dislikes = Like.objects.filter(comment=comment, like=False, dislike=True).count()
        total = likes-dislikes

        comment.like = likes
        comment.dislike = dislikes
        comment.total = total
        comment.save()
        return True

    def post(self, request):
        comment = get_object_or_404(Comment, id=self.request.POST.get('comment_id'))
        like_type = self.request.POST.get('like_type')
        method = self.request.POST.get('method')

        like = self.get_like_object(self.request, comment)

        context = {}

        if like_type == 'like':
            if method == 'submit':
                like.like = True
            elif method == 'cancel':
                like.like = False
            like.dislike = False

        elif like_type == 'dislike':
            if method == 'submit':
                like.dislike = True
            elif method == 'cancel':
                like.dislike = False
            like.like = False

        like.save()

        self.calculate_comment_like(self.request, comment)
        context = {'comment': comment.id, 'type': like_type, 'method': method, 'like_count': comment.like,
                   'dislike_count': comment.dislike}

        return HttpResponse(json.dumps(context), content_type="application/json")
