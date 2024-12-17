import urequests
import ubinascii

group_id = '18105413361016'
api_key = 'W3peS4muS6kuiBlOe9keaciemZkOWFrOWPuCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODEwNTQxMzM2MTEwMDU2MzcwIiwiUGhvbmUiOiIxODY3ODg4NjYzOCIsIkdyb3VwSUQiOiIxODEwNTQxMzM2MTAxNjY3NzYyIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMTItMTcgMDk6NDE6MzMiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.GUnpt8amhnKr4myiuN9-KsEwvUYVHExk3mBxPioqlp4qkXR9X8rzC0KHhjgrGmVOCwJ7P4ZNJy86SaPnXdvXdfJCyo0bqU0zJv-LHYmYAd42wl_-VHQ8DNQPQES1u2w5_u3xx49Jl2tffy9M7VhntolGS3dkWw6rZ8rLuNaUVW2F9rdvn330yljs0P0YWo6H7zCWrH8_gGErva1cl_eMlq3saUBWVZsAFwHCmDOSPjfEms201RTQqAMlnMEnJkt74FQG1iBHCLyOd8t4fa84Nn0aFgJeOABaXFS0y2UGaCiQPvKG1BbcJ7Ntu6lzWwSLsLUGLbWUXchWwijlGYteyw'

url = f"https://api.minimax.chat/v1/t2a_v2?GroupId={group_id}"


def tts_data(text: str):
    if not text:
        return

    encoded_text = text.encode("utf-8")

    # 使用 b2a_base64 编码为 Base64
    encoded_base64 = ubinascii.b2a_base64(encoded_text)

    data = '{"text":"' + encoded_base64.hex() + '"}'

    response = urequests.post("http://192.168.1.141:8086/tts/text", data=data)
    parsed_json = response.json()
    return parsed_json['data']


def tts(text: str):
    if not text:
        return
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # data = f'{{"model":"speech-01-turbo", "text":"{text}", "voice_setting":{{"voice_id":"male-qn-qingse"}}}}'

    data = '{"model":"speech-01-turbo", "text":"' + text + '", "voice_setting":{"voice_id":"male-qn-qingse"}}'
    new = "'" + data + "'"
    print(data)
    response = urequests.post(url, headers=headers, data=new)
    parsed_json = response.json()
    print(f"minimax res code: {parsed_json['base_resp']['status_code']}")
    # 获取audio字段的值
    return parsed_json['data']['audio']
