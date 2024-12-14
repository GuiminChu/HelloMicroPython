import urequests


# https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html

def build_url_with_params(base_url, params):
    """
    拼接 URL 和请求参数。

    :param base_url: 基础 URL，字符串类型。
    :param params: 请求参数，字典类型。
    :return: 拼接后的完整 URL，字符串类型。
    """
    # 将字典转为查询字符串
    query_string = "&".join(f"{key}={value}" for key, value in params.items())
    # 拼接基础 URL 和查询字符串
    full_url = f"{base_url}?{query_string}"
    return full_url


def speech_recognizer(audio_data):
    print(type(audio_data))
    # 阿里云ASR接口地址
    url = "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/asr"

    # 请求参数
    params = {
        "appkey": "VPfLmqUAxFMX3FNP",
        "sample_rate": 16000,
        "enable_punctuation_prediction": True
    }

    full_url = build_url_with_params(url, params)

    # 请求头
    headers = {
        "X-NLS-Token": "5e8c728eab5844a3b7a3b40efefe74f8",
    }

    # 读取音频文件为二进制流
    try:

        # 设置 Content-Length
        headers["Content-Length"] = str(len(audio_data))

        # 发起 POST 请求
        response = urequests.post(
            full_url,
            headers=headers,
            data=audio_data,
        )

        # 打印结果
        if response.status_code == 200:
            print("Result:", response.text)
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
