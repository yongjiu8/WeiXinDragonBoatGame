import datetime
import random
import sys
import time

import requests


def printf(text, userId=''):
    ti = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f'[{ti}][{userId}]: {text}')
    sys.stdout.flush()


def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def getNowTime():
    return int(round(time.time() * 1000))


def createGame():
    url = f'https://payapp.weixin.qq.com/coupon-center-activity/game/create?session_token={token}'
    head = {
        'Referer': 'https://td.cdn-go.cn/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'com.tencent.mm'
    }
    data = {"activity_id": 1000000, "game_pk_id": "7398502-00-V2D-WXzWj2QxYjE4YjU"}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    printf(res)
    return res['data']


def startGame():
    url = f'https://payapp.weixin.qq.com/coupon-center-report/statistic/batchreport?session_token={token}'
    head = {
        'Referer': 'https://td.cdn-go.cn/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'com.tencent.mm'
    }
    data = {"source_scene": "scene", "device": "DEVICE_ANDROID", "device_platform": "DEVICE_ANDROID",
            "device_system": "DEVICE_ANDROID", "device_brand": "DEVICE_ANDROID", "device_model": "DEVICE_ANDROID",
            "wechat_version": "1.0.0", "wxa_sdk_version": "1.0.0", "wxa_custom_version": "1.1.6", "event_list": [
            {"event_code": "ActivityGameBegin", "event_target": "1000000", "intval1": 2,
             "strval1": gameId}]}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    printf(res)


def submitGame(items, score):
    url = f'https://payapp.weixin.qq.com/coupon-center-activity/game/report?session_token={token}'
    head = {
        'Referer': 'https://td.cdn-go.cn/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'com.tencent.mm'
    }
    data = {"activity_id": 1000000, "game_id": gameId, "game_report_score_info": {
        "score_items": items,
        "game_score": score, "total_score": score}}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    printf(res)


def getScore():
    url = f'https://payapp.weixin.qq.com/coupon-center-activity/game/get?session_token={token}&activity_id=1000000&game_id={gameId}&sid=a5299654f1f5e423c1fc9757f9bf071d&coutom_version=6.30.6'
    head = {
        'Referer': 'https://td.cdn-go.cn/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'com.tencent.mm'
    }

    res = requests.get(url=url, headers=head, timeout=5).json()
    return res['data']


def getConpun():
    url = f'https://payapp.weixin.qq.com/coupon-center-activity/award/obtain?session_token={token}'
    head = {
        'Referer': 'https://td.cdn-go.cn/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'com.tencent.mm'
    }
    data = {"activity_id": 1000000, "game_id": gameId, "obtain_ornament": True,
            "request_id": "osd2L5ZiTu4UDWiNrB8bxnlVB-bQ_lj440mdj_"+generate_random_str(4), "sid": "3bec088206a229c0cd925c464809cd24",
            "coutom_version": "6.30.8"}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    printf(res)


if __name__ == '__main__':
    while True:
        items = []
        #账号token
        token = '示例 请修改为自己账号的token'
        #大于多少分提交游戏领取提现券
        maxScore = 7000

        datas = createGame()
        gameId = datas['game_id']
        score = 0
        for it in datas['play_script']['dragon_boat_2023_play_script']['tracks']:
            for em in it['props']:
                if 'score' not in em.keys():
                    continue
                upScore = em['score']
                score = score + upScore

        if score < maxScore:
            printf(f'预测分数：{score}')
            continue

        startGame()
        score = 0
        for it in datas['play_script']['dragon_boat_2023_play_script']['tracks']:
            for em in it['props']:
                if 'score' not in em.keys():
                    continue
                upScore = em['score']
                items.append(
                    {"prop_id": em['prop_id'], "award_score": upScore, "fetch_timestamp_ms": getNowTime()}
                )
                score = score + upScore
                time.sleep(0.07)
        submitGame(items, score)
        scoreItem = getScore()
        printf(f'分数：{scoreItem["gamer_play_score"]} 游戏id：{scoreItem["game_id"]}')
        getConpun()
        break
