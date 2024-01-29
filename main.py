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
        "charset": "utf-8",
        "mpm-sdkversion": "3.3.3",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/2090 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "mpm-model": "Redmi Note 8 Pro",
        "wepaytest-proxyip": "",
        "mpm-platform": "android",
        "mpm-appversion": "6.49.0",
        "mpm-sourcescene": "1007",
        "mpm-scene": "1007",
        "mpm-brand": "Redmi",
        "mpm-system": "Android 11",
        "content-type": "application/json",
        "mpm-version": "8.0.46",
    }
    #data = {"activity_id": activity_id, "game_pk_id": game_pk_id}
    data = {"activity_id": activity_id}
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
        "device_platform": "android",
        "device_system": "Android 9",
        "device_brand": "OnePlus",
        "device_model": "HD1910",
        "wechat_version": "8.0.46",
        "wxa_sdk_version": "3.3.3",
        "wxa_custom_version": "6.49.0",
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
        "charset": "utf-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/2090 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "content-type": "application/json",
        "mpm-version": "8.0.46",
    }
    if module:
        data = {
            "activity_id": activity_id,
            "game_id": gameId,
            "game_report_score_info": {
                "score_items": items,
                "game_score": score,
                "total_score": score + pk_f,
            },
        }
    else:
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
        "request_id": "sd2L5dpgD3196UtSWjtdVhTz2Zs_lryivcmz_" + generate_random_str(4),
        "coutom_version": "6.49.0",
    }
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()
    logging.info(res)


if __name__ == "__main__":
    logging.info('本脚本可跑俩次,一次pk模式和一次正常模式,超出均会系统错误')
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
        "charset": "utf-8",
        "mpm-sdkversion": "3.3.3",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/2090 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "mpm-model": "Redmi Note 8 Pro",
        "wepaytest-proxyip": "",
        "mpm-platform": "android",
        "mpm-appversion": "6.49.0",
        "mpm-sourcescene": "1007",
        "mpm-scene": "1007",
        "mpm-brand": "Redmi",
        "mpm-system": "Android 11",
        "content-type": "application/json",
        "mpm-version": "8.0.46",
    }
    # 账号token
    token = ''
    # 大于多少分提交游戏领取提现券
    maxScore = 7373
    activity_id = 1000013
    # 模式，True为开启pk，False为关闭
    module = True
    # pk_id
    game_pk_id = ''
    # pk_id分数
    pk_f = 7373
    if token == '':
        print('请输入token')
        exit()
    if module:
        logging.info('当前为pk模式,如果最后系统错误大概率是pk_id和分数不对应或已领取过pk奖励')
        if game_pk_id == '':
            print("请输入pk_id和相应分数")
            exit()
    else:
        logging.info('当前为正常模式,如果最后系统错误大概率是已领取过')
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
        if module:
            txq = scoreItem["gamer_play_score"]+pk_f
        else:
            txq = scoreItem["gamer_play_score"]
        logging.info(f'提现券：{txq}元')
        getConpun()
        break
