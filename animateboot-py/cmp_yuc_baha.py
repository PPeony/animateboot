import json

# ================================================================
# 1. 模拟你的输入数据
# ================================================================

# JSON A (来自你的上一步网页解析)
json_a = [
    {
        "name": "永恒余晖",
        "jp_name": "永久のユウグレ",
        "pic": "http://...1.jpg"
    },
    {
        "name": "SI-VIS: The Sound of Heroes",
        "jp_name": "SI-VIS: The Sound of Heroes",
        "pic": "http://...2.jpg"
    },
    {
        "name": "未匹配的动画",  # (用于测试 A 有 B 没有的情况)
        "jp_name": "未マッチ",
        "pic": "http://...3.jpg"
    }
]

# JSON B (已知的音乐库)
json_b = [
    {
        "name": "永恒余晖",  # (情况1: 1-to-1 匹配)
        "music": "Music for Yuugure"
    },
    {
        "name": "SI-VIS: The Sound of Heroes",  # (情况2: 1-to-N 匹配 - 1)
        "music": "Opening Song"
    },
    {
        "name": "SI-VIS",  # (情况2: 1-to-N 匹配 - 2)
        "music": "Ending Song"
    },
    {
        "name": "另一个动画",  # (B 中多余的)
        "music": "Some other music"
    }
]


# ================================================================
# 2. 【请替换】你的语义比较函数
# ================================================================
def comparej(s1: str, s2: str) -> bool:
    """
    【请在这里集成你的真实比较逻辑】
    例如：
    embedding1 = model.encode(s1)
    embedding2 = model.encode(s2)
    score = util.cos_sim(embedding1, embedding2)[0][0]
    return score > 0.9 # (比如阈值设为 0.9)
    """

    # --- 为了演示，我用一个简化的 "包含" 逻辑来模拟 ---
    # 这样 "SI-VIS: The Sound of Heroes" 就会同时匹配
    # "SI-VIS: The Sound of Heroes" 和 "SI-VIS"
    s1_lower = s1.lower()
    s2_lower = s2.lower()

    if s1_lower == s2_lower:
        return True

    # 模拟语义相关：如果 s2 更短且是 s1 的子串
    if len(s2) < len(s1) and (s2_lower in s1_lower):
        return True

    return False


# ================================================================
# 3. 核心匹配逻辑
# ================================================================

# 初始化三个结果容器
matched_pairs = []  # 1-to-1 唯一匹配
unmatched_in_a = []  # A 中有, B 中没有
ambiguous_matches = []  # 1-to-N 歧义匹配

print(f"开始匹配 {len(json_a)} (A) x {len(json_b)} (B) ...")

# 1. 遍历 A 中的每一项
for item_a in json_a:
    s1 = item_a['name']
    current_matches = []  # 存储当前 s1 命中的所有 B 项

    # 2. 遍历 B 中的每一项
    for item_b in json_b:
        s2 = item_b['name']

        # 调用你的比较函数
        try:
            if comparej(s1, s2):
                current_matches.append(item_b)
        except Exception as e:
            print(f"比较 '{s1}' 和 '{s2}' 时出错: {e}")

    # 3. 根据 B 中匹配到的数量，对 A 项进行分类
    if len(current_matches) == 0:
        # A 中有，B 中没有
        unmatched_in_a.append(item_a)

    elif len(current_matches) == 1:
        # 唯一匹配
        matched_pairs.append({
            "a_item_name": item_a['name'],
            "b_item_name": current_matches[0]['name'],
            "a_item_full": item_a,
            "b_item_full": current_matches[0]
        })

    else:
        # 1-to-N 歧义匹配
        ambiguous_matches.append({
            "a_item_name": item_a['name'],
            "a_item_full": item_a,
            "b_matches_full": current_matches  # 记录所有 B 中的匹配项
        })

# ================================================================
# 4. 打印报告
# ================================================================
print("\n" + "=" * 40)
print("         匹配结果报告")
print("=" * 40)

# 1. 打印歧义匹配 (最重要，优先人工排查)
print(f"\n### ❗ 1-N 歧义匹配 (需人工排查) ({len(ambiguous_matches)} 项) ###")
if ambiguous_matches:
    for item in ambiguous_matches:
        print(f"\n  [A] {item['a_item_name']}")
        print("    匹配到多个 [B] 项:")
        for b_match in item['b_matches_full']:
            print(f"    - {b_match['name']} (Music: {b_match['music']})")
else:
    print("  (无)")

# 2. 打印唯一匹配
print(f"\n### ✅ 1-1 唯一匹配 ({len(matched_pairs)} 项) ###")
if matched_pairs:
    for item in matched_pairs:
        print(f"  [A] {item['a_item_name']}  <--->  [B] {item['b_item_name']} (Music: {item['b_item_full']['music']})")
else:
    print("  (无)")

# 3. 打印A中未匹配
print(f"\n### ❌ A 中未匹配 ({len(unmatched_in_a)} 项) ###")
if unmatched_in_a:
    for item in unmatched_in_a:
        print(f"  - {item['name']}")
else:
    print("  (无)")

# (可选) 打印完整的 JSON 报告
final_report = {
    "ambiguous_matches": ambiguous_matches,
    "matched_pairs": matched_pairs,
    "unmatched_in_a": unmatched_in_a
}

# print("\n\n--- 完整 JSON 报告 ---")
# print(json.dumps(final_report, ensure_ascii=False, indent=2))