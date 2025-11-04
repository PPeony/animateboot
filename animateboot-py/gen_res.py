import json

# 1. 你的原始输入数据
# (假设你已经有了一个名为 data 的 Python 字典)
# data = ...
#
filename = '11021929.json'
with open(f'output/{filename}', 'r', encoding='utf-8') as file:
    input_json_string = file.read()

# 将 JSON 字符串解析为 Python 字典
data = json.loads(input_json_string)

# 2. 核心转换逻辑
final_anime_list = []
matched_pairs_list = data.get('matched_pairs', [])  # 安全地获取列表

for pair in matched_pairs_list:
    try:
        # 为了代码更健壮，使用 .get() 来防止 KeyError
        a_item_full = pair.get('a_item_full', {})
        b_item_full = pair.get('b_item_full', {})

        # 按照你指定的规则构建新字典
        new_anime_object = {
            "cn_name": pair.get('a_item_name'),
            "tw_name": pair.get('b_item_name'),
            "jp_name": a_item_full.get('jp_name'),
            "pic": a_item_full.get('pic'),
            "op": b_item_full.get('op', []),  # 如果 op 不存在，默认为空列表
            "ed": b_item_full.get('ed', [])  # 如果 ed 不存在，默认为空列表
        }

        final_anime_list.append(new_anime_object)

    except Exception as e:
        print(f"处理条目时出错: {e} - 条目: {pair.get('a_item_name')}")

# 3. 将最终的列表转换为 JSON 字符串
# ensure_ascii=False 确保中文正常显示
# indent=2 格式化输出
output_json = json.dumps(final_anime_list, ensure_ascii=False, indent=2)

# 4. 打印结果
print(output_json)

with open(f'data/{filename}', 'w', encoding='utf-8') as file:
    file.write(output_json)