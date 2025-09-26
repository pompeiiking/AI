# # 测试FunASR安装
# import sys
# print(f"Python版本: {sys.version}")

# try:
#     import editdistance
#     print("✅ editdistance 安装成功")
# except ImportError:
#     print("❌ editdistance 安装失败")

# try:
#     from funasr import AutoModel
#     print("✅ FunASR 安装成功")
    
#     # 测试流式模型加载
#     print("正在加载流式模型...")
#     model = AutoModel(model="paraformer-zh-streaming", device="cpu")
#     print("✅ 流式模型加载成功")
    
# except ImportError as e:
#     print(f"❌ FunASR 导入失败: {e}")
# except Exception as e:
#     print(f"❌ 模型加载失败: {e}")

#     # 我已经学会了TEN-VAD的使用，但我知道vad只是负责进行流式语音记录的功能，接下来需要一套asr模块来进行语音识别，我经过查询找到了FunAsr，@https://github.com/modelscope/FunASR ，之后将要将TEN-VAD流式接收的语音切片流式地传输给FunAsr进行实时语音检测，替换掉@test copy 4.py 中的语音识别模块，但重要的是现在先让我逐步学习并独立自主地搭建一套FunAsr流式检测系统，请基于此对我进行教学，逐步掌握搭建方法，我是完全的萌新，请尽可能详细地为我讲解每个组件，各个语法与参数，并尽量少地生成代码，引导我自己完成，现在开始教学
    
#     # 现在开始学习流式识别基础实现
#     print("\n=== 开始学习FunASR流式识别 ===")
    
#     # 第一步：了解流式识别的基本参数
#     print("流式识别关键参数：")
#     print("- chunk_size: 每次处理的音频长度（样本数）")
#     print("- chunk_interval: 处理间隔（毫秒）")
#     print("- is_final: 是否为最终结果")
    
#     # 第二步：创建流式识别器
#     print("\n创建流式识别器...")
#     # 这里需要你来完成：创建一个流式识别器实例
#     # 提示：使用 model.generate() 方法，设置 is_final=False

# result = model.generate(
#     input = audio_data,   # 输入音频数据
#     is_final = False,    # 是否为最终结果
#     chunk_size = 512 ,   # 每次处理的音频长度（样本数）
#     chunk_interval = 100, # 处理间隔（毫秒）
#     cache = {},          # 缓存

# )

# # # 参数说明：
# # input: 音频数据（numpy数组或文件路径）
# # is_final: False=流式中间结果，True=最终完整结果
# # chunk_size: 每次处理的样本数（512≈32ms，1024≈64ms）
# # chunk_interval: 处理间隔毫秒数，通常与chunk_size对应
# # cache: 用于保持流式状态的字典



import os
import sys

import numpy as np
import sounddevice as sd

from funasr import AutoModel

current_dir = os.path.dirname(__file__)
funasr_path = os.path.join(current_dir, "..", "funasr", "include")
abs_funasr_path = os.path.abspath(funasr_path)
sys.path.append(abs_funasr_path)

from ten_vad import TenVad

def steam_stt():
    audio_result = []
    asr_cache = {}
    vad = TenVad(
        hop_size = 512,
        threshold = 0.5,
    )
    model = AutoModel(
        model = "paraformer-zh-streaming",
        device = "cuda",
        disable_update = True,
        trust_remote_code = True
    )
    while True:
        audio_data = sd.rec(
            frames = 512,
            samplerate = 16000,
            channels = 1,
            dtype = 'int16'
        )
        sd.wait()

        speech_prob, speech_flag = vad.process(audio_data)
        if speech_flag == 0:
            if len(audio_result) >0:
                part_result = model.generate(
                    input = np.concatenate(audio_result),
                    is_final = True,
                    chunk_size = 512,
                    chunk_interval = 32,
                    cache = asr_cache
                )
                result = part_result[0]['text']
                asr_cache = {}
                audio_result = []
                print("最终结果：",result)
                return result

            else:
                print("等待录音")
                continue
        else:
            audio_result.append(audio_data)
            part_result =model.generate(
                input = audio_data,
                is_final = False,
                chunk_size = 512,
                chunk_interval = 32,
                cache = asr_cache
            )
            print("中间结果：",part_result[0]['text'])
            continue

