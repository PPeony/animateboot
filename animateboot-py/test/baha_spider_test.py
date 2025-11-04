import unittest
from bs4 import BeautifulSoup, Tag, NavigableString

# -----------------------------------------------------------------
# 1. 粘贴你需要测试的函数
# -----------------------------------------------------------------
def get_font_text(cell_tag: Tag) -> str:
    """
    安全地从 <td> 标签内的第一个 <font> 标签中，
    提取第一个 <a> 标签 *之前* 的所有文本内容。
    """
    if not cell_tag:
        return ""

    first_font = cell_tag.find('font')

    if first_font:
        # --- 这是新的、更健壮的逻辑 ---
        texts = [] # 用于收集所有文本片段

        # 1. 遍历 first_font 标签的所有后代节点（包括文本、<br>、<font>等）
        for node in first_font.descendants:

            # 2. 如果遇到 <a> 标签，立即停止遍历
            if node.name == 'a':
                break

            # 3. 如果这个节点是文本 (NavigableString)，就收集它
            if isinstance(node, NavigableString):
                texts.append(str(node))

        # 4. 将收集到的所有文本片段连接起来
        full_text = "".join(texts)

        # 5. 清理文本：
        #    - .split() 会按所有空白（包括\n）分割
        #    - " ".join(...) 会用单个空格重新组合
        #    - .strip() 去除首尾多余空格
        cleaned_text = " ".join(full_text.split()).strip()

        return cleaned_text
        # --- 新逻辑结束 ---

    else:
        # Fallback：如果 <td> 里根本没有 <font> 标签
        return cell_tag.get_text(strip=True)

# -----------------------------------------------------------------
# 2. 编写测试用例
# -----------------------------------------------------------------
class TestGetFontText(unittest.TestCase):

    def test_case_1_horizontal_line(self):
        """
        测试 "水平線は僕の古傷" 案例：
        应包含 <br> 后的多行文本，但在 <a> 处停止。
        """
        html_snippet = """
        <td align="center" colspan="2">
          <font face="微軟正黑體">
            「水平線は僕の古傷」<br>
            廣川卯月、赤城郁實、姫路紗良、霧島透子、岩見澤寧寧<br>
            <font size="2"><a href="..." target="_blank">TV size(広川卯月)</a> × </font>
            <font size="2"><a href="..." target="_blank">TV size(赤城郁実)</a></font>
          </font>
        </td>
        """
        # 预期结果：<br> 标签被视为空格，<a> 标签后的内容被忽略
        expected = "「水平線は僕の古傷」 廣川卯月、赤城郁實、姫路紗良、霧島透子、岩見澤寧寧"

        # 执行测试
        soup = BeautifulSoup(html_snippet, 'html.parser')
        cell_tag = soup.find('td')
        actual = get_font_text(cell_tag)

        # 断言
        self.assertEqual(actual, expected)

    def test_case_2_silent_night(self):
        """
        测试 "Silent Night" 案例：
        应包含子 <font> 标签中的文本，因为没有 <a> 标签。
        """
        html_snippet = """
        <td align="center" colspan="2">
          <font face="微軟正黑體">
            「Silent Night」<font size="3">霧島透子</font>
          </font>
        </td>
        """
        # 预期结果：两个文本节点被合并（注意：它们之间没有空格）
        expected = "「Silent Night」霧島透子"

        # 执行测试
        soup = BeautifulSoup(html_snippet, 'html.parser')
        cell_tag = soup.find('td')
        actual = get_font_text(cell_tag)

        # 断言
        self.assertEqual(actual, expected)

    def test_case_3_gridout_yama(self):
        """
        测试 "GRIDOUT" 案例 (来自之前的对话)：
        应只包含 "「GRIDOUT」yama"，并在 <a> 处停止。
        """
        html_snippet = """
        <td align="center" colspan="2">
          <font face="微軟正黑體">
            「GRIDOUT」yama<br>
            <font size="2"><a href="..." target="_blank">Music Video</a></font>
          </font>
        </td>
        """
        # 预期结果：只包含第一行文本
        expected = "「GRIDOUT」yama"

        # 执行测试
        soup = BeautifulSoup(html_snippet, 'html.parser')
        cell_tag = soup.find('td')
        actual = get_font_text(cell_tag)

        # 断言
        self.assertEqual(actual, expected)

# -----------------------------------------------------------------
# 3. 运行测试
# -----------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()