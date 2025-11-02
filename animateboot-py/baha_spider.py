import json
import os
import traceback
from youtubemusic import search_in_youtube

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
div_list = soup.find_all('div', class_='MSG-list8C')

if not div_list:
    print("错误: 未找到 class='MSG-list8C' 的 div 标签。")
    exit()

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
                cell_text = cell.get_text(strip=True)
                if cell_text.startswith('OP') and len(cell_text) < 5:  # 应该是 OD1, OD2这种，长度判断为了过滤掉 “OP 發售日 2025.07.16”
                    op = {}
                    op['ep_id'] = -1
                    next_cell = cells[i + 1]

                    op['text'] = get_font_text(next_cell)
                    op['youtube'] = search_in_youtube(op['text'])

                    result_list.append(op)
        return result_list  # 遍历完也没找到 "OP"，返回空列表

    # --- 处理 ED (只有当 type == "ED" 时才会运行到这里) ---
    for row in rows:
        cells = row.find_all('td')
        for i, cell in enumerate(cells):
            cell_text = cell.get_text(strip=True)
            if cell_text.startswith('EP'):
                if i + 1 < len(cells):
                    ep = {}
                    ep['ep_id'] = cell_text
                    next_cell = cells[i + 1]

                    ep['text'] = get_font_text(next_cell)
                    ep['youtube'] = search_in_youtube(ep['text'])

                    result_list.append(ep)
            elif cell_text.startswith('ED') and len(cell_text) < 5: # 应该是 ED1, ED2这种，长度判断为了过滤掉 “ED 發售日 2025.07.16”
                ep = {}
                ep['ep_id'] = -1
                next_cell = cells[i + 1]

                ep['text'] = get_font_text(next_cell)
                ep['youtube'] = search_in_youtube(ep['text'])

                result_list.append(ep)

    return result_list  # 返回所有找到的 ED


# 在<div class="MSG-list8C">下查找第3个<tr>的第2个<td>的文本内容

for div in div_list:
    table_list = div.find_all('table')
    for tbl in table_list:
        # 2. 为每个条目创建一个字典
        anime_data = {}
        name = ""  # 用于错误追踪
        try:
            tbody = tbl.find('tbody')
            if not tbody:
                continue  # 跳过没有 tbody 的 table

            # 获取名称
            tr_list = tbody.find_all('tr')
            name_cell = tr_list[0].find('td')
            if name_cell:
                name = name_cell.get_text(strip=True)
                anime_data['name'] = name
                anime_data['jp_name'] = ''
                if len(tr_list) > 1 and tr_list[1] and tr_list[1].find('td'):
                    anime_data['jp_name'] = tr_list[1].find('td').get_text(strip=True)
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
