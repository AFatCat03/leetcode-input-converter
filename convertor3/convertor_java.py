from playwright.sync_api import sync_playwright

types = []

def set_types(page):
    page.wait_for_selector('span.mtk10')
    page.wait_for_selector('span.mtk9')
    mtk10_locator = page.locator('span.mtk10')
    assert mtk10_locator.count() == 1, f'Only support problems which has only one function {mtk10_locator.count()}'

    mtk9_locator = mtk10_locator.locator('css=~ span.mtk9')
    for mtk9 in mtk9_locator.all():
        types.append(mtk9.inner_text() + mtk9.locator('css=+ span.mtk1').inner_text()[:-1]) # 最后的切片去除mtk1元素中末尾的空格


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

def convert(input_elems):
    res = ''
    for i in range(input_elems.count()):
        res += ', '
        elem = input_elems.nth(i).inner_text()
        cur_type = types[i]
        if cur_type[-2:] == '[]':
            res += array_convert(cur_type, elem)
        else:
            res += other_convert(elem)

    res = res[2:]
    return res
