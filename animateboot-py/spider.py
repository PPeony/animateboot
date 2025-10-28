import json
import os
import traceback

from bs4 import BeautifulSoup, Tag

# 网页链接
# https://home.gamer.com.tw/creationDetail.php?sn=5963805
try:
    with open('sourcefile\\202507.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
except FileNotFoundError:
    print("错误: 找不到文件 ")
    exit()

# 使用Beautiful Soup解析网页内容
soup = BeautifulSoup(html_content, 'html.parser')

# 查找目标结构<div class="MSG-list8C">
div = soup.find('div', class_='MSG-list8C')

if not div:
    print("错误: 未找到 class='MSG-list8C' 的 div 标签。")
    exit()

# 在<div class="MSG-list8C">下查找第3个<tr>的第2个<td>的文本内容
table_list = div.find_all('table')
res = []


def get_font_text(cell_tag: Tag) -> str:
    """
    一个健壮的辅助函数：
    安全地从 <td> 标签内的第一个 <font> 标签中，
    提取第一个 *直接的* 文本内容。
    """
    if not cell_tag:
        return ""

    first_font = cell_tag.find('font')

    if first_font:
        # 1. 寻找第一个直接的文本节点，recursive=False 确保不进入子标签
        text_node = first_font.find(text=True, recursive=False)

        if text_node:
            # 2. 找到了，清理并返回
            return text_node.strip()
        else:
            # 3. Fallback：如果<font>里没有直接文本 (例如 <font><b>text</b></font>)
            #    就获取 <font> 里的所有文本
            return first_font.get_text(strip=True)
    else:
        # 4. Fallback：如果 <td> 里根本没有 <font> 标签
        return cell_tag.get_text(strip=True)


def find(tbody, type: str):
    rows = tbody.find_all('tr')
    result_list = []  # 重命名为 result_list 避免与 ed 混淆

    # --- 处理 OP ---
    if type == "OP":
        for row in rows:
            cells = row.find_all('td')
            for i, cell in enumerate(cells):
                # 使用 .get_text(strip=True) 比较，更安全
                if cell.get_text(strip=True) == type:
                    if i + 1 < len(cells):
                        next_cell = cells[i + 1]
                        ep = {}
                        ep['ep_id'] = -1
                        # === 这就是修复 ===
                        # 使用辅助函数确保我们得到的是字符串
                        ep['text'] = get_font_text(next_cell)
                        result_list.append(ep)
                        return result_list  # 找到 OP，立即返回
                    else:
                        return result_list  # 找到 "OP" 但没有下一个单元格，返回空列表
        return result_list  # 遍历完也没找到 "OP"，返回空列表

    # --- 处理 ED (只有当 type == "ED" 时才会运行到这里) ---
    for row in rows:
        cells = row.find_all('td')
        for i, cell in enumerate(cells):
            cell_text = cell.get_text(strip=True)  # 清理过的单元格文本
            if cell_text.startswith('EP'):
                if i + 1 < len(cells):
                    ep = {}
                    ep['ep_id'] = cell_text
                    next_cell = cells[i + 1]

                    # 同样使用辅助函数
                    ep['text'] = get_font_text(next_cell)

                    result_list.append(ep)
            elif cell_text.startswith('ED'):
                ep = {}
                ep['ep_id'] = -1
                next_cell = cells[i + 1]

                # 同样使用辅助函数
                ep['text'] = get_font_text(next_cell)

                result_list.append(ep)

    return result_list  # 返回所有找到的 ED


for tbl in table_list:
    # 2. 为每个条目创建一个字典
    anime_data = {}
    name = ""  # 用于错误追踪
    try:
        tbody = tbl.find('tbody')
        if not tbody:
            continue  # 跳过没有 tbody 的 table

        # 获取名称
        name_cell = tbody.find('tr').find('td')
        if name_cell:
            name = name_cell.get_text(strip=True)
            anime_data['name'] = name
        else:
            anime_data['name'] = "未知名称"

        # 获取 OP (现在返回一个列表)
        anime_data['op'] = find(tbody, "OP")

        # 获取 ED (现在返回一个列表)
        anime_data['ed'] = find(tbody, "ED")

        # 3. 将字典追加到结果列表
        res.append(anime_data)

    except Exception as e:
        traceback.print_exc()
        print(f"处理条目时出错: '{name}'")

# 4. 在循环结束后，将整个列表转为 JSON 字符串
json_output = json.dumps(res, ensure_ascii=False, indent=2)

# 5. 打印最终的 JSON 字符串
print(json_output)