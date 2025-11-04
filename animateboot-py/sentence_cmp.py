import ssl
import os
import time

# -------------------------------------------------------------------
# 解决方案 (Python 3.11+ 最终版，IDE 兼容)
# -------------------------------------------------------------------

# 1. (Hugging Face 专用) 禁用 Hugging Face Hub 的 SSL 验证
os.environ['HF_HUB_DISABLE_SSL_VERIFY'] = 'True'

# 2. (全局)
#    创建一个 *不验证证书* 的 SSL 上下文
#    这是官方的、公开的 API，你的 IDE 会认识
try:
    unverified_context = ssl.create_default_context()
    unverified_context.check_hostname = False  # 不检查主机名
    unverified_context.verify_mode = ssl.CERT_NONE  # 不验证证书

    # 3. 将这个“不验证”的上下文设置为 Python 的默认值
    #    lambda: unverified_context 确保每次都返回这个配置好的上下文
    ssl.create_default_context = lambda: unverified_context
except Exception as e:
    print(f"警告: 无法设置全局 SSL 不验证。模型下载可能失败。错误: {e}")

# -------------------------------------------------------------------
# 你原来的代码
# -------------------------------------------------------------------
from sentence_transformers import SentenceTransformer, util

# 1. 加载一个预训练好的、支持中文的模型
print("正在加载模型...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def cmp_s1_s2(s1, s2):
    if s2 is None:
        return False
    start = time.time()
    embedding1 = model.encode(s1, convert_to_tensor=True)
    embedding2 = model.encode(s2, convert_to_tensor=True)
    cosine_score = util.cos_sim(embedding1, embedding2)[0][0]
    end = time.time()
    # print(f"相似度得分: {cosine_score:.4f}")
    # print(f'cost time {end - start}')
    return cosine_score > 0.8
# 2. 准备你的句子
# sentence1 = "男女之间存在纯友情吗"
# sentence2 = "男女之间存在纯友谊吗"
# sentence3 = "男女之間存在純友情嗎"
#
# # 3. 将句子编码为向量（Embeddings）
# embedding1 = model.encode(sentence1, convert_to_tensor=True)
# embedding2 = model.encode(sentence2, convert_to_tensor=True)
# embedding3 = model.encode(sentence3, convert_to_tensor=True)
#
#
# # 4. 计算两个向量的余弦相似度
# cosine_score = util.cos_sim(embedding1, embedding2)[0][0]
# cosine_score_diff = util.cos_sim(embedding1, embedding3)[0][0]
# end = time.time()
# print(f"句子1: {sentence1}")
# print(f"句子2: {sentence2}")
# print(f"相似度得分: {cosine_score:.4f}")
#
# print("-" * 20)
#
# print(f"句子1: {sentence1}")
# print(f"句子3: {sentence3}")
# print(f"相似度得分: {cosine_score_diff:.4f}")
# print(f'cost time {end - start}')
