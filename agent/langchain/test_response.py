import os
from dotenv import load_dotenv
load_dotenv(override=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")

try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好，请简单介绍一下你自己"}
        ],
    )
    
    print("🎉 请求成功！")
    print("\n" + "="*50)
    print("RESPONSE 对象的完整结构：")
    print("="*50)
    
    # 1. 基本信息
    print(f"📋 请求ID: {response.id}")
    print(f"🤖 使用模型: {response.model}")
    print(f"⏰ 创建时间: {response.created}")
    
    # 2. 回复内容
    print(f"\n💬 AI回复内容:")
    print(f"   角色: {response.choices[0].message.role}")
    print(f"   内容: {response.choices[0].message.content}")
    
    # 3. 使用统计
    print(f"\n📊 使用统计:")
    print(f"   输入tokens: {response.usage.prompt_tokens}")
    print(f"   输出tokens: {response.usage.completion_tokens}")
    print(f"   总tokens: {response.usage.total_tokens}")
    
    # 4. 完整response对象
    print(f"\n🔍 完整response对象类型: {type(response)}")
    print(f"   所有属性: {dir(response)}")
    
except Exception as e:
    print(f"❌ 请求失败：{e}")
