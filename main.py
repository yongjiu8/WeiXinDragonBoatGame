import datetime
import logging
import random
import sys
import time
from urllib.parse import unquote, quote

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
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/create?session_token={token}&activity_id={activity_id}&online_game_play_mode=ONLINE_SINGLE_PLAY_MODE&sid=62af092da7f16c9a314c396df8942a59&coutom_version=6.34.6"
    res = requests.get(url=url, headers=head, timeout=5).json()
    logging.info(res)
    _datas = res.get("data")
    if _datas:
        return _datas


def ActivityCreateGame():
    event = '[{"event_code":"ActivityCreateGame","strval1":"' + gameId + '","intval1":1,"intval2":1,"event_target":"' + str(
        activity_id) + '","logid":"jca659v71ls0000000"},' \
                       '{"event_code":"SelectLanternPageExpo","intval1":1,"intval2":1,"strval1":"快乐","event_target":"1000007","logid":"avva8vpml0c0000000"},' \
                       '{"event_code":"SelectedBtnClick","intval1":1,"strval1":"期待","event_target":"1000007","logid":"3p8o5worqfc00000000"},' \
                       '{"event_code":"GoToSign","intval1":1,"intval2":1,"event_target":"1000007","logid":"8ihqrgdiexg00000000"}]'
    url = f'https://payapp.weixin.qq.com/coupon-center-report/statistic/batchreport?session_token={token}&device=DEVICE_ANDROID&device_platform=android&device_system=Android 11&device_brand=Redmi&device_model=Redmi Note 8 Pro&wechat_version=8.0.40&wxa_sdk_version=3.0.0&wxa_custom_version=6.34.6&source_scene=1089&event_list={quote(event)}&sid=62af092da7f16c9a314c396df8942a59&coutom_version=6.34.6'
    res = requests.get(url=url, headers=head, timeout=5).json()
    logging.info(res)
    _datas = res.get("data")
    if _datas:
        return _datas


def ONLINE_REPORT_STEP_JOIN():
    game_online_report_step_info = '{"step_type":"ONLINE_REPORT_STEP_JOIN","step_data":"期待"}'
    url = f'https://payapp.weixin.qq.com/coupon-center-activity/game/report?session_token={token}&activity_id={activity_id}&game_id={gameId}&game_online_report_step_info={game_online_report_step_info}&sid=ff681aa72a5c679b55520505262a8fff&coutom_version=6.34.6'
    res = requests.get(url=url, headers=head, timeout=5).json()
    _datas = res.get("data")
    if _datas:
        return _datas


def startGame(event_code):
    url = f"https://payapp.weixin.qq.com/coupon-center-report/statistic/batchreport?session_token={token}"
    data = {"source_scene": "light-up", "device": "DEVICE_ANDROID", "device_platform": "DEVICE_ANDROID",
            "device_system": "DEVICE_ANDROID", "device_brand": "DEVICE_ANDROID", "device_model": "DEVICE_ANDROID",
            "wechat_version": "1.0.0", "wxa_sdk_version": "1.0.0", "wxa_custom_version": "1.0.9", "event_list": [
            {"event_code": event_code, "event_target": str(activity_id), "intval1": 1, "intval2": 1}]}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()


def submitGame():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/report?session_token={token}"
    data = {"activity_id": activity_id, "game_id": gameId,
            "game_online_report_step_info": {"step_type": "ONLINE_REPORT_STEP_PLAY",
                                             "step_data": "data:image/png;base64,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" + generate_random_str(
                                                 20) + "="}}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()


def ONLINE_REPORT_STEP_FINISH():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/report?session_token={token}"
    data = {"activity_id": activity_id, "game_id": gameId,
            "game_online_report_step_info": {"step_type": "ONLINE_REPORT_STEP_FINISH",
                                             "step_data": ""}}
    res = requests.post(url=url, headers=head, json=data, timeout=5).json()


def getScore():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/game/get?session_token={token}&activity_id={activity_id}&game_id={gameId}&sid=a5299654f1f5e423c1fc9757f9bf071d&coutom_version=6.30.6"
    res = requests.get(url=url, headers=head, timeout=5).json()
    return res["data"]


def getConpun():
    url = f"https://payapp.weixin.qq.com/coupon-center-activity/award/obtain?session_token={token}"
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
    head = {
        "Referer": "https://td.cdn-go.cn/",
        "Content-Type": "application/json",
        "X-Requested-With": "com.tencent.mm",
        "charset": "utf-8",
        "mpm-sdkversion": "3.0.0",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/2090 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "mpm-model": "Redmi Note 8 Pro",
        "wepaytest-proxyip": "",
        "mpm-platform": "android",
        "mpm-appversion": "6.34.6",
        "mpm-sourcescene": "1089",
        "mpm-scene": "1089",
        "mpm-brand": "Redmi",
        "mpm-system": "Android 11",
        "content-type": "application/json",
        "mpm-version": "8.0.40",
    }
    # 账号token
    token = '抓包获取session_token'
    # 大于多少分提交游戏领取提现券
    maxScore = 10000
    activity_id = 1000007
    game_pk_id = ''
    while True:
        items = []
        datas = createGame()
        if datas is None:
            time.sleep(2)
            logging.info("not data sleep 2")
            continue
        gameId = datas["game_id"]
        # ActivityCreateGame()
        ONLINE_REPORT_STEP_JOIN()
        # startGame('QixiH5ExposureActivityPageSign')
        # startGame('QixiH5ExposureActivityPage')
        submitGame()
        # startGame('QixiH5ClickSignSuccessBtn')
        # startGame('QixiH5ExposureActivityPageLightLantern')
        ONLINE_REPORT_STEP_FINISH()
        # startGame('QixiH5ClickLightLanternBtn')
        # startGame('QixiH5LightLanternCompleted')
        # startGame('QixiH5ExposureActivityPageEnding')
        # startGame('QixiH5PlayEndingVideoCompleted')
        # startGame('QixiH5ClickObtainAwardBtn')

        scoreItem = getScore()
        logging.info(f'分数：{scoreItem["game_award_value"]} 游戏id：{scoreItem["game_id"]}')
        # getConpun()
