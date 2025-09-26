# def __init__(self,hop_size: int = 256, threshold: float = 0.5):
# 初始化
# hop_size: 什么是hop_size？
# hop_size是每次处理的音频样本数量
# 默认256意味着每次处理256个音频样本
# 这决定了VAD的"时间分辨率"
# 如何选择hop_size？
# 较小的hop_size (如128, 256)：检测更敏感，响应更快，但计算量更大
# 较大的hop_size (如512, 1024)：检测较稳定，计算量小，但响应较慢
# 时间计算：
# 在16kHz采样率下，256样本 = 256/16000 = 16毫秒
# 这意味着VAD每16毫秒检测一次语音活动
# threshold: 什么是threshold？
# threshold是VAD的阈值
# 默认0.5意味着VAD检测到语音活动的概率为50%
# 如何选择threshold？
# 较小的threshold (如0.3, 0.4)：检测更敏感，响应更快，但误判率更高
# 较大的threshold (如0.7, 0.8)：检测较稳定，误判率较低，但响应较慢
# 时间计算：
# 在16kHz采样率下，256样本 = 256/16000 = 16毫秒
# 这意味着VAD每16毫秒检测一次语音活动

# 返回值：
# out_probability: 语音活动的概率
# out_flag: 语音活动的标志 （0表示非语音活动，1表示语音活动）

# 音频数据格式要求：
# 数据类型必须是np.int16 必须为一个一维数组，长度等于hop_size 采样率一般为16kHZ

# import numpy as np
# import sounddevice as sd
# import sys
# import os

# def process_audio_chunk(hop_size: int, threshold: float, samplerate: int):
#     audio_data = sd.rec(
#         frames=hop_size, 
#         samplerate=samplerate, 
#         channels=2, dtype='int16', 
#         blocking=True
#     )

#     sd.wait()

#     print(f"音频形状:{audio_data.shape}")
#     print(f"数据类型:{audio_data.dtype}")
#     print(f"音频大小:{len(audio_data)}")

#     return audio_data

# if __name__ == "__main__":
#     process_audio_chunk(512, 0.5, 16000)

# import numpy as np
# import sounddevice as sd
# import sys
# import os

# current_dir = os.path.dirname(__file__)
# ten_vad_path = os.path.join(current_dir, "..", "ten-vad","include")
# abs_ten_vad_path = os.path.abspath(ten_vad_path)
# sys.path.append(abs_ten_vad_path)

# def test_vad():
#     try:
#         from ten_vad import TenVad
#         vad = TenVad(hop_size=512, threshold=0.5)
#         chunk = sd.rec(
#             frames = 512,
#             samplerate = 16000,
#             channels = 1,
#             dtype = 'int16'
#         )
#         sd.wait()

#         speech_prob, speech_flag = vad.process(chunk)

#         print(f"语音概率：{speech_prob}")
#         print(f"语音标志：{speech_flag}")

#         if speech_flag == 1:
#             print("检测到语音")
#         else:
#             print("未接收到语音")

#     except Exception as e:
#         print(f"检测模块报错：{e}")

# if __name__ == "__main__":
#     test_vad()

# import numpy as np
# import sounddevice as sd
# import sys
# import os

# current_dir = os.path.dirname(__file__)
# ten_vad_path = os.path.join(current_dir, "..", "ten-vad", "include")
# abs_ten_vad_path = os.path.abspath(ten_vad_path)
# sys.path.append(abs_ten_vad_path)

# def stream_vad():
#     try:
#         from ten_vad import TenVad
#         vad = TenVad(hop_size = 512,threshold = 0.5)
#         while True:
#             audio_data = sd.rec(
#                 frames = 512,
#                 samplerate = 16000,
#                 channels = 1,
#                 dtype = 'int16'
#             )
#             sd.wait()
#             speech_prob, speech_flag = vad.process(audio_data)
#             print(f"语音概率：{speech_prob:.3f}")
#             if speech_flag == 1:
#                 continue
#             else:
#                 print("未接收到语音")
#                 break
#     except KeyboardInterrupt:
#         print("\n用户中断")
#     except Exception as e:
#         print(f"检测模块报错：{e}")

# if __name__ == "__main__":
#     stream_vad()

import numpy as np
import sounddevice as sd
import sys
import os

current_dir = os.path.dirname(__file__)
ten_vad_path = os.path.join(current_dir, "..", "ten-vad", "include")
abs_ten_vad_path = os.path.abspath(ten_vad_path)
sys.path.append(abs_ten_vad_path)

def smart_record():
    try:
        from ten_vad import TenVad
        audio_result = []
        vad = TenVad(hop_size = 512, threshold = 0.5)
        while True:
            audio_data = sd.rec(
                frames = 512,
                samplerate =16000,
                channels = 1,
                dtype = 'int16'
            )
            sd.wait()
            speech_prob, speech_flag = vad.process(audio_data)
            if speech_flag == 0:
                if(len(audio_result) > 0):
                    return np.concatenate(audio_result)
                else:
                    print("等待录音")
                    continue
            else:
                audio_result.append(audio_data)
                continue

    except Exception as e:
        print(f"检测模块报错：{e}")
        return None

if __name__ == "__main__":
    audio = smart_record()
    if audio is not None:
        print(f"录音完成啦！录音时长：{len(audio)}")

