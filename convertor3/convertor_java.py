from playwright.sync_api import sync_playwright
from datetime import date
from pathlib import Path
import re


types = []

def get_class_name(page):

    # 获取题目序号
    problem_name = page.locator('.text-title-large > a').first.inner_text()
    problem_id = problem_name[:problem_name.index('.')]

    basename_re = re.compile(r'problems/(.*)/')
    basename_match = basename_re.search(page.url)
    basename = basename_match.group(1)

    pattern = re.compile(r'-(.)')
    modified_basename = pattern.sub(lambda match: match.group(1).upper(), basename)

    classname = modified_basename[0].upper() + modified_basename[1:] + problem_id

    return classname

def get_extension():
    return '.java'


def set_types(page):
    global types

    page.wait_for_selector('span.mtk10')
    page.wait_for_selector('span.mtk9')
    mtk10_locator = page.locator('span.mtk10')
    assert mtk10_locator.count() == 1, f'Only support problems which has only one function {mtk10_locator.count()}'

    #mtk9_locator = mtk10_locator.locator('css=~ span.mtk9')
    mtk9_locator = page.locator('xpath=//span[contains(@class, "mtk10")]/following::span[contains(@class, "mtk9")]')
    for mtk9 in mtk9_locator.all():
        types.append(mtk9.inner_text() + mtk9.locator('css=+ span.mtk1').inner_text()[:-1]) # 最后的切片去除mtk1元素中末尾的空格
    #print(types)

    newTypes = []
    index = 0
    while index < len(types):
        newTypes.append(types[index])
        while index < len(types) and types[index] == 'List':
            index += 1
        index += 1
    types = newTypes
    # print(types)


def treenode(values, index):
    if index >= len(values) or values[index] == 'null':
        return 'null'
    else:
        return f'new TreeNode({int(values[index])}, {treenode(values, 2 * index)}, {treenode(values, 2 * index + 1)})'

def treenode_convert(elem):
    values = elem[1:-1].split(',')
    if len(values) == 1 and values[0] == '':
        return 'null'
    values.insert(0, '')
    return treenode(values, 1)


def listnode_convert(values):
    if len(values) <= 0:
        return 'null'
    return f'new ListNode({int(values[0])}, {listnode_convert(values[1:])})'


def list_convert(elem):
    return elem.replace(',', ', ').replace('[', 'List.of(').replace(']', ')')


def char_array_convert(elem):
    return other_array_convert(elem).replace('"', '\'')

def other_array_convert(elem):
    return elem.replace('[', '{').replace(']', '}').replace(',', ', ')

def array_convert(cur_type, elem):
    res = 'new ' + cur_type
    if cur_type[:4] == 'char':
        res += char_array_convert(elem)
    else:
        res += other_array_convert(elem)
    return res


def other_convert(cur_type, elem):
    return elem


def input_convert(input_elems):
    # print(types)
    res = ''
    for i in range(input_elems.count()):
        res += ', '
        elem = input_elems.nth(i).inner_text()
        cur_type = types[i]
        # print(cur_type)
        if cur_type == 'TreeNode':
            res += treenode_convert(elem)
        elif cur_type == 'ListNode':
            res += listnode_convert(elem[1:-1].split(','))
        elif cur_type == 'List':
            res += list_convert(elem)
        elif cur_type[-2:] == '[]':
            res += array_convert(cur_type, elem)
        else:
            res += other_convert(cur_type, elem)

    res = res[2:]
    return res


def convert(page):
    # 等待页面加载
    page.wait_for_selector('[data-e2e-locator="console-testcase-tag"]', state="visible")
    cases = page.locator('[data-e2e-locator="console-testcase-tag"]')

    set_types(page)
    #print(types)

    author = 'AFatCat03'
    class_name = get_class_name(page)
    instance_name = class_name[0].lower() + class_name[1:]
    func_name = page.locator('span.mtk10').inner_text()

    (Path.home() / 'Desktop/leetcode').mkdir(exist_ok=True)
    output_file = open(Path.home() / f"Desktop/leetcode/{class_name}{get_extension()}", 'w', encoding='UTF-8')

    output_file.write('/**\n')
    output_file.write(f' * @author {author}\n')
    output_file.write(f" * @date {str(date.today()).replace('-', '/')}\n")
    output_file.write(' */\n')
    output_file.write(f'public class {class_name}\n')
    output_file.write('{\n')

    func_line = page.locator('span.mtk10').locator('..').inner_text()
    output_file.write((func_line[:-1]).replace(' ', ' '))
    if func_line[-1] != '{':
        next_line_locator = page.locator('xpath=//span[contains(@class, "mtk10")]/ancestor::div[1]/following-sibling::div[1]')
        output_file.write(' ' + (next_line_locator.inner_text()[:-1]).replace(' ', ' '))
    output_file.write('\n')

    output_file.write('    {\n')
    output_file.write('        \n')
    output_file.write('    }\n')
    output_file.write('\n')
    output_file.write('    public static void main(String[] args)\n')
    output_file.write('    {\n')
    output_file.write(f'        {class_name} {instance_name} = new {class_name}();\n')

    for case in cases.all():
        case.evaluate("element => element.click()") # 切换测试用例
        input_elems = page.get_by_placeholder('请输入测试用例')
        output_elems = input_convert(input_elems)
        output_file.write(f'        System.out.println({instance_name}.{func_name}({output_elems}));\n')

    output_file.write('    }\n')
    output_file.write('}\n')

    output_file.close()
