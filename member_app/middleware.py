import random

from django.utils import timezone
from ipware.ip import get_ip

from data_app.models import Champion
from member_app.models import NonMemberSession, NicknameEmotion, Profile


class VisitorSessionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET':
            # 로그인 한 경우
            if request.user.is_authenticated:
                pass
            # 로그인 하지 않은 경우
            else:
                ip = get_ip(request)
                ip_display = ip.split('.')[0] + '.' + ip.split('.')[1] + '. * . *'

                # 해당 ip의 세션이 존재하는지 탐색
                session_object, created = NonMemberSession.objects.get_or_create(ip=ip)
                if created:
                    while True:
                        emotion = random.choice(list(NicknameEmotion.objects.values('emotion')))
                        champ = random.choice(list(Champion.objects.values('champion_short')))
                        nickname = emotion['emotion'] + ' ' + champ['champion_short']
                        print(nickname)
                        if Profile.objects.filter(nickname=nickname).exists() or NonMemberSession.objects.filter(
                                nickname=nickname).exists():
                            pass
                        else:
                            session_object.nickname = nickname
                            session_object.save()
                            request.session['nickname'] = nickname
                            request.session['ip'] = ip
                            break

                elif not created:
                    session_object.last_use = timezone.now()
                    session_object.save()
                    request.session['nickname'] = session_object.nickname
                    request.session['ip'] = session_object.ip
                    # request.session['profile_session'] = session_object

        return response
