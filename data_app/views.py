import json

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic.base import View

from data_app.models import Summoner, Comment, Like, CommentReport, Score


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
    def comment_format(self, request, comments):
        comment_list = []
        comment_sample = """
        <div class="comment" id="comment_{}">
            <div class="writer">
                <p style="margin:35px 0px 20px 0px; padding-left:15px;">{}<span class="comment_writer">{}</span><br><span class="written_date">{}</span></p>
            </div>
            <div class="comment_detail">
                <span class="comment_text">{}</span>
            </div>
            <div class="comment_set">
                <p style="margin-top: 0;margin-bottom: 40%;">
                    {}
                    <span class="report" onclick="open_report_modal({})"><i class="fas fa-exclamation-triangle" style="color:orange;"></i>&nbsp;신고</span>
                </p>
                <p>
                    {}
                    {}
                </p>
            </div>
        </div>
        """

        tier_sample = '<span class="tier_{}">{}&nbsp;</span>'
        delete_sample = '<span class="delete" onclick="{}({})"><i class="fas fa-trash" style="color:gray"></i>&nbsp;삭제</span>&nbsp;&nbsp;'
        like_sample = """
        <span class="like {}" onclick="like_submit('{}', 'like', '{}')"><i class="far fa-thumbs-up"></i> <span class="like_count">{}</span></span>&nbsp;&nbsp;&nbsp;&nbsp;
        """
        dislike_sample = """
            <span class="dislike {}" onclick="like_submit('{}', 'dislike', '{}')"><i class="far fa-thumbs-down"></i> <span class="dislike_count">{}</span></span>&nbsp;&nbsp;&nbsp;&nbsp;
            """

        if self.request.user.is_superuser:
            for x in comments:
                if x.writer:
                    tier = tier_sample.format('C', 'C')
                    delete_element = delete_sample.format('direct_delete', x.id)
                    name = x.writer.profile.nickname

                else:
                    delete_element = delete_sample.format('open_delete_modal', x.id)
                    name = x.nickname
                    tier = ''

                like = Like.objects.filter(liker=self.request.user, comment__id=x.id)

                if like.count() > 0:
                    if like[0].like and not like[0].dislike:
                        like_element = like_sample.format('liked', 'cancel', x.id, x.like)
                        dislike_element = dislike_sample.format('', 'submit', x.id, x.dislike)
                    else:
                        like_element = like_sample.format('', 'submit', x.id, x.like)
                        dislike_element = dislike_sample.format('disliked', 'cancel', x.id, x.dislike)
                else:
                    like_element = like_sample.format('', 'submit', x.id, x.like)
                    dislike_element = dislike_sample.format('', 'submit', x.id, x.dislike)

                comment_list.append(
                    comment_sample.format(x.id, tier, name, str(x.written_date)[:16], x.comment, delete_element, x.id, like_element, dislike_element))

        elif self.request.user.is_authenticated:
            for x in comments:
                if x.writer:
                    tier = tier_sample.format('C', 'C')
                    if x.writer == self.request.user:
                        delete_element = delete_sample.format('direct_delete', x.id)
                    else:
                        delete_element = ''

                    name = x.writer.profile.nickname

                else:
                    delete_element = delete_sample.format('open_delete_modal', x.id)
                    name = x.nickname
                    tier = ''

                like = Like.objects.filter(liker=self.request.user, comment__id=x.id)

                if like.count() > 0:
                    if like[0].like and not like[0].dislike:
                        like_element = like_sample.format('liked', 'cancel', x.id, x.like)
                        dislike_element = dislike_sample.format('', 'submit', x.id, x.dislike)
                    else:
                        like_element = like_sample.format('', 'submit', x.id, x.like)
                        dislike_element = dislike_sample.format('disliked', 'cancel', x.id, x.dislike)
                else:
                    like_element = like_sample.format('', 'submit', x.id, x.like)
                    dislike_element = dislike_sample.format('', 'submit', x.id, x.dislike)

                comment_list.append(
                    comment_sample.format(x.id, tier, name, str(x.written_date)[:16], x.comment, delete_element, x.id, like_element, dislike_element))

        else:
            for x in comments:
                if x.writer:
                    tier = tier_sample.format('C', 'C')
                    delete_element = ''

                    name = x.writer.profile.nickname

                else:
                    delete_element = delete_sample.format('open_delete_modal', x.id)
                    name = x.nickname
                    tier = ''

                like = Like.objects.filter(ip_addr=request.session._session['ip'], comment__id=x.id)

                if like.count() > 0:
                    if like[0].like and not like[0].dislike:
                        like_element = like_sample.format('liked', 'cancel', x.id, x.like)
                        dislike_element = dislike_sample.format('', 'submit', x.id, x.dislike)
                    else:
                        like_element = like_sample.format('', 'submit', x.id, x.like)
                        dislike_element = dislike_sample.format('disliked', 'cancel', x.id, x.dislike)
                else:
                    like_element = like_sample.format('', 'submit', x.id, x.like)
                    dislike_element = dislike_sample.format('', 'submit', x.id, x.dislike)

                comment_list.append(
                    comment_sample.format(x.id, tier, name, str(x.written_date)[:16], x.comment, delete_element, x.id, like_element, dislike_element))

        return comment_list

    def post(self, request):
        summoner = get_object_or_404(Summoner, id=self.request.POST.get('summoner'))
        order_type = self.request.POST.get('order_type')

        if order_type == 'recent':
            comments = Comment.objects.filter(summoner=summoner).order_by('-written_date')

        elif order_type == 'like':
            comments = Comment.objects.filter(summoner=summoner).order_by('-total')

        else:
            raise Http404

        comment_list = self.comment_format(self.request, comments)

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

        if like_type == 'like':
            if method == 'submit':
                like.like = True
            like.dislike = False

        elif like_type == 'dislike':
            if method == 'submit':
                like.dislike = True
            like.like = False

        if method == 'cancel':
            like.delete()
        else:
            like.save()


        self.calculate_comment_like(self.request, comment)
        context = {'comment': comment.id, 'type': like_type, 'method': method, 'like_count': comment.like,
                   'dislike_count': comment.dislike}

        return HttpResponse(json.dumps(context), content_type="application/json")


class SummonerScoreView(View):
    def post(self, request):
        summoner = get_object_or_404(Summoner, id=self.request.POST.get('summoner_id'))
        score = self.request.POST.get('score').count('★')

        if self.request.user.is_authenticated:
            score, created = Score.objects.get_or_create(target=summoner, score=score, valuer=self.request.user)
        else:
            score, created = Score.objects.get_or_create(target=summoner, score=score, ip_addr=request.session._session['ip'])

        print(created)
        if not created:
            context = {'status': 'already'}
        else:
            context = {'status': 'success'}

        return HttpResponse(json.dumps(context), content_type="application/json")
