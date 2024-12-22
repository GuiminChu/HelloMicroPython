import ubinascii
from mrequests import mrequests
from config import FAST_LLM_BASE_URL
import utils
import max98357a
import ali_speech_recognizer
import oled_091

group_id = '1810541336101667762'
api_key = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLlsbHkuJzpnZLpuJ_lt6XkuJrkupLogZTnvZHmnInpmZDlhazlj7giLCJVc2VyTmFtZSI6IuWxseS4nOmdkum4n-W3peS4muS6kuiBlOe9keaciemZkOWFrOWPuCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODEwNTQxMzM2MTEwMDU2MzcwIiwiUGhvbmUiOiIxODY3ODg4NjYzOCIsIkdyb3VwSUQiOiIxODEwNTQxMzM2MTAxNjY3NzYyIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMTItMTcgMDk6NDE6MzMiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.GUnpt8amhnKr4myiuN9-KsEwvUYVHExk3mBxPioqlp4qkXR9X8rzC0KHhjgrGmVOCwJ7P4ZNJy86SaPnXdvXdfJCyo0bqU0zJv-LHYmYAd42wl_-VHQ8DNQPQES1u2w5_u3xx49Jl2tffy9M7VhntolGS3dkWw6rZ8rLuNaUVW2F9rdvn330yljs0P0YWo6H7zCWrH8_gGErva1cl_eMlq3saUBWVZsAFwHCmDOSPjfEms201RTQqAMlnMEnJkt74FQG1iBHCLyOd8t4fa84Nn0aFgJeOABaXFS0y2UGaCiQPvKG1BbcJ7Ntu6lzWwSLsLUGLbWUXchWwijlGYteyw'

url = f"https://api.minimax.chat/v1/t2a_v2?GroupId={group_id}"

buf = bytearray(1024)

is_audio_playing = False


class ResponseWithProgress(mrequests.Response):
    _total_read = 0

    def readinto(self, buf, size=0):
        bytes_read = super().readinto(buf, size)
        self._total_read += bytes_read
        # utils.get_current_time()
        # print("Progress: {:.2f}%".format(self._total_read / (self._content_size * 0.01)))
        return bytes_read


def tts_mrequest(url: str, text: str):
    global is_audio_playing
    if not text:
        return

    r = mrequests.get(url, headers={b"accept": b"audio/pcm"}, response_class=ResponseWithProgress)

    if r.status_code == 200:
        print(f"语音开始返回，时间: {utils.get_current_time()}")
        # 在下载过程中异步播放
        while r._total_read < r._content_size:
            r.readinto(buf)
            max98357a.play_audio(buf)

        filename = "recording.wav"
        r.save(filename, buf=buf)
        # print("Audio saved to '{}'.".format(filename))
        is_audio_playing = False
        print(f"语音结束，时间: {utils.get_current_time()}")
    else:
        print("Request failed. Status: {}".format(r.status_code))

    r.close()


def get_answer_tts(recorded_data: bytearray):
    """
    先获取语音识别结果，再语言大模型回答，再合成语音
    """
    global is_audio_playing

    # 进行语音识别
    text = ali_speech_recognizer.speech_recognizer(recorded_data)
    print(f"获取录音识别结果: [{text}]，开始请求语音，时间: {utils.get_current_time()}")
    if text:
        encoded_text = text.encode("utf-8")
        encoded_base64 = ubinascii.b2a_base64(encoded_text)
        url = f"{FAST_LLM_BASE_URL}/tts/question?question={encoded_base64.hex()}"
        tts_mrequest(url, text)
    else:
        is_audio_playing = False
        print("识别结果为空，结束执行。")


def get_tts(text: str):
    """
    直接文字合成语音
    """

    global is_audio_playing

    if text:
        is_audio_playing = True
        encoded_text = text.encode("utf-8")
        encoded_base64 = ubinascii.b2a_base64(encoded_text)
        url = f"{FAST_LLM_BASE_URL}/tts/text?text={encoded_base64.hex()}"
        tts_mrequest(url, text)
    else:
        is_audio_playing = False
