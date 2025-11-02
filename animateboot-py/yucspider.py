import json
import re
from bs4 import BeautifulSoup, Comment

# ----------------------------------------------------------------
# 1. 加载你的 HTML 内容
# ----------------------------------------------------------------


# 方式二：从文件读取 (如果你的 HTML 在文件中)
try:
    with open('yuc\\202507.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
except FileNotFoundError:
    print("错误：HTML 文件未找到。")
    exit()

# ----------------------------------------------------------------
# 2. 开始解析
# ----------------------------------------------------------------
soup = BeautifulSoup(html_content, 'html.parser')
results = []

# 编译正则表达式
# 1. 匹配注释内容，如 #A01, #B123
comment_regex = re.compile(r'^#[A-Za-z]\d+$')
# 2. 匹配 class，如 title_cn_r, title_cn_r1
class_cn_regex = re.compile(r'^title_cn_r')
# 3. 匹配 class，如 title_jp_r
class_jp_regex = re.compile(r'^title_jp_r')

# 查找所有注释
all_comments = soup.find_all(string=lambda text: isinstance(text, Comment))

# 过滤出作为“起始锚点”的注释
start_comments = [c for c in all_comments if comment_regex.match(c.string)]

print(f"找到了 {len(start_comments)} 个匹配的条目...")

for comment in start_comments:
    item = {
        "name": None,
        "jp_name": None,
        "pic": None
    }
    try:
        # 1. 查找第一个 div (包含图片)
        # .find_next_sibling('div') 会自动跳过注释和div间的换行符(NavigableString)
        div1 = comment.find_next_sibling('div')
        if not div1:
            print(f"警告: 找不到 '{comment.string}' 后面的第一个 div")
            continue

        # 2. 查找第二个 div (包含信息)
        div2 = div1.find_next_sibling('div')
        if not div2:
            print(f"警告: 找不到 '{comment.string}' 后面的第二个 div")
            continue

        # --- 开始提取数据 ---

        # 提取 'pic'
        pic_tag = div1.find('a', class_='fancybox')
        if pic_tag and pic_tag.has_attr('href'):
            item['pic'] = pic_tag['href']

        # 提取 'name' (使用 class 正则表达式)
        name_tag = div2.find('p', class_=class_cn_regex)
        if name_tag:
            item['name'] = name_tag.get_text(strip=True)

        # 提取 'jp_name'
        jp_name_tag = div2.find('p', class_=class_jp_regex)
        if jp_name_tag:
            item['jp_name'] = jp_name_tag.get_text(strip=True)

        results.append(item)

    except Exception as e:
        print(f"处理条目 '{comment.string}' 时出错: {e}")

# ----------------------------------------------------------------
# 3. 转换为 JSON 并打印
# ----------------------------------------------------------------
json_output = json.dumps(results, ensure_ascii=False, indent=2)
print(json_output)