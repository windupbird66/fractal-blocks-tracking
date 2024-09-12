import requests
from datetime import datetime, timezone, timedelta
import time

# 定义API地址
url_height = "https://explorer.unisat.io/fractal-mainnet/api/block/list?start=0&limit=1&mempool=true&sort="
url_fee = "https://explorer.unisat.io/fractal-mainnet/api/bitcoin-info/fee"

# Webhook URL (替换为你的机器人的 webhook URL)
webhook_url = ''

# 需要触发警报的区块高度
alert_blocks = [20000, 20500, 21000]

# 记录已经触发过的区块高度，避免重复推送
triggered_blocks = set()

# 推送消息到微信群
def send_wechat_message(content):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 200:
        print("消息推送成功")
    else:
        print(f"消息推送失败，状态码: {response.status_code}")

# 监控区块高度
while True:
    # 获取区块高度和费用信息
    response_height = requests.get(url_height)
    response_fee = requests.get(url_fee)
    print("一直在路上...")
    if response_height.status_code == 200 and response_fee.status_code == 200:
        data_height = response_height.json()
        data_h1 = data_height.get('data', {}).get('detail', [])[0]

        data_fee = response_fee.json()
        data_f1 = data_fee.get('data', {})

        block_height = data_h1.get('height')
        block_miner = data_h1.get('miner')
        block_timestamp = data_h1.get('timestamp')
        block_fee = data_f1.get('halfHourFee')

        # 设置时区为 UTC+8
        utc_plus_8 = timezone(timedelta(hours=8))
        block_time = datetime.fromtimestamp(block_timestamp, utc_plus_8).strftime('%Y-%m-%d %H:%M:%S')

        # 检查当前区块高度是否在指定的警报列表中
        if block_height in alert_blocks and block_height not in triggered_blocks:
            message_content = (
                f"嘀嘀嘀，BirdDAO帅哥美女们请注意！\n"
                f"当前区块高度: {block_height}\n"
                f"矿工: {block_miner}\n"
                f"Gas费: {block_fee}\n"
                f"生成时间 (UTC+8): {block_time}"
            )
            send_wechat_message(message_content)
            # 记录触发过的区块高度，避免重复推送
            triggered_blocks.add(block_height)
    else:
        print("请求失败")

    # 每隔 10 秒检查一次区块高度
    time.sleep(10)
