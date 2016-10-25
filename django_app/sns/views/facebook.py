import json
from collections import Counter

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from apis import facebook

__all__ = [
    'friends_ranking',
]

def friends_ranking(request):

    if request.method == 'GET':

        if request.GET.get('error'):
            return HttpResponse('사용자 로그인 거부')

        if request.GET.get('code'):
            code = request.GET.get('code')
            REDIRECT_URL = 'http://{host}{url}'.format(
                host=request.META['HTTP_HOST'],
                url=reverse('sns:friends_ranking'),
            )

            access_token = facebook.get_access_token(code, REDIRECT_URL)
            # return HttpResponse('%s<br>%s' % (REDIRECT_URL, access_token))
            user_id = facebook.get_user_id_from_token(access_token)
            # facebook에서 comment 하위 속성은 { } 형식으로 불러온다
            # {{}} 형식을 사용해야 format() 형식에서 사용 가능하다

            url_request_feed = 'https://graph.facebook.com/v2.8/{user_id}/feed?' \
                               'fields=comments{{from,comments}}&' \
                               'limit=1000&' \
                               'access_token={access_token}'.format(
                user_id=user_id,
                access_token=access_token,
            )

            r = requests.get(url_request_feed)
            dict_feed_info = r.json()
            json_data = json.dumps(dict_feed_info, indent=2)
            # print(json_data)
            # print(dict_feed_info)
            comment_list = []
            for feed in dict_feed_info.get('data'):
                # print(feed)
                if feed.get('comments'):
                    for comment in feed.get('comments').get('data'):
                        comment_list.append(comment)

            id_list = [
                comment.get('from', {}).get('id')
                for comment
                in comment_list
            ]
            """
            Counter 함수를 사용해보자
            >> >  # Tally occurrences of words in a list
            >> > cnt = Counter()
            >> > for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
                ...
                cnt[word] += 1
            >> > cnt
            Counter({'blue': 3, 'red': 2, 'green': 1})
            """
            counter = Counter()
            for id in id_list:
                counter[id] += 1
            # order by most
            most_id_list = counter.most_common()
            print(most_id_list)
            set_most_id_list = list(set(id_list))
            set_most_id_list = set_most_id_list[:50]
            str_set_most_id_list = ','.join(set_most_id_list)
            # print(str_set_most_id_list)

            uri_request_ids_info = 'https://graph.facebook.com/v2.8/{user_id}/' \
                              '?ids={ids}&' \
                              'fields=cover,email,picture,name&' \
                              'access_token={access_token}'.format(
                user_id=user_id,
                ids=str_set_most_id_list,
                access_token=access_token,
            )

            r = requests.get(uri_request_ids_info)
            dict_ids_info = r.json()
            print(json.dumps(dict_ids_info, indent=2))

            dict_ids_info_list = []
            for item in most_id_list:
                id = item[0]
                for k in dict_ids_info:
                    if k == id and k != user_id:
                        dict_ids_info_list.append({
                            'info': dict_ids_info[k],
                            'number': item[1],
                        })
            print(dict_ids_info_list)
            context = {'dict_ids_info_list': dict_ids_info_list}
            return render(request, 'sns/facebook/friends_ranking.html', context)

    elif request.method == 'POST':
        import ast
        str_item_list = request.POST.getlist('item')
        # string 을 list로 변환
        for str_item in str_item_list:
            item = ast.literal_eval(str_item)
            # print(item)



