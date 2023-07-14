import datetime
import logging
import random
import sys
import time

import requests

# format code use black
logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s:%(lineno)3d: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


def printf(text, userId=""):
    ti = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"[{ti}][{userId}]: {text}")
    sys.stdout.flush()


def generate_random_str(randomlength=16):
    # random.sample??
    random_str = ""
    base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def getNowTime():
    return int(round(time.time() * 1000))


def createGame():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/create?session_token={token}"
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
    }
    data = {"activity_id": activity_id, "game_pk_id": game_pk_id}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    # printf(res)
    _datas = res.get("data")
    if _datas:
        return _datas
    logging.info(res)


def startGame():
    url = f"https://payapp.weixin.qq.com/coupon-center-report/statistic/batchreport?session_token={token}"
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
    }
    data = {
        "source_scene": "scene",
        "device": "DEVICE_ANDROID",
        "device_platform": "DEVICE_ANDROID",
        "device_system": "DEVICE_ANDROID",
        "device_brand": "DEVICE_ANDROID",
        "device_model": "DEVICE_ANDROID",
        "wechat_version": "1.0.0",
        "wxa_sdk_version": "1.0.0",
        "wxa_custom_version": "1.1.6",
        "event_list": [
            {
                "event_code": "ActivityGameBegin",
                "event_target": str(activity_id),
                "intval1": 2,
                "strval1": gameId,
            }
        ],
    }
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    logging.info(res)


def submitGame(items, score):
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/report?session_token={token}"
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
    }
    data = {
        "activity_id": activity_id,
        "game_id": gameId,
        "game_report_score_info": {
            "score_items": items,
            "game_score": score,
            "total_score": score,
        },
    }
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    logging.info(res)


def getScore():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/get?session_token={token}&activity_id=1000000&game_id={gameId}&sid=a5299654f1f5e423c1fc9757f9bf071d&coutom_version=6.30.6"
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
    }

    res = requests.get(url=url, headers=head, timeout=5).json()
    return res["data"]


def getConpun():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/award/obtain?session_token={token}"
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
    }
    data = {
        "activity_id": activity_id,
        "game_id": gameId,
        "obtain_ornament": True,
        "request_id": "osd2L5ZiTu4UDWiNrB8bxnlVB-bQ_lj440mdj_" + generate_random_str(4),
        "sid": "3bec088206a229c0cd925c464809cd24",
        "coutom_version": "6.30.8",
    }
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    logging.info(res)


if __name__ == "__main__":
    # 账号token
    token = 'GkvznYhTJVqVmeQ8w4icCGt72uBibiajiad6Rz8KWYzic8SjazWZmH1iaMweDRGB'
    # 大于多少分提交游戏领取提现券
    maxScore = 10000
    activity_id = 1000005
    game_pk_id = ''
    while True:
        items = []
        datas = createGame()
        if datas is None:
            time.sleep(2)
            logging.info("not data sleep 2")
            continue
        gameId = datas["game_id"]
        score = 0
        for it in datas["play_script"]["dragon_boat_2023_play_script"]["tracks"]:
            for em in it["props"]:
                if "score" not in em.keys():
                    continue
                upScore = em["score"]
                score = score + upScore

        logging.info(f"预测分数：{score}")
        if score < maxScore:
            continue
        logging.info(f'分数达标，开始玩游戏，请耐心等待。。。')
        startGame()
        score = 0
        for it in datas["play_script"]["dragon_boat_2023_play_script"]["tracks"]:
            for em in it["props"]:
                if "score" not in em.keys():
                    continue
                upScore = em["score"]
                items.append(
                    {
                        "prop_id": em["prop_id"],
                        "award_score": upScore,
                        "fetch_timestamp_ms": getNowTime(),
                    }
                )
                score = score + upScore
                time.sleep(0.07)
        submitGame(items, score)
        scoreItem = getScore()
        logging.info(f'分数：{scoreItem["gamer_play_score"]} 游戏id：{scoreItem["game_id"]}')
        getConpun()
        break
