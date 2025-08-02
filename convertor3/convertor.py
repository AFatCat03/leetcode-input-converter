from playwright.sync_api import sync_playwright
from convertor_total import set_types, convert
import convertor_java

# 获取每日一题页面URL
def get_daily_problem_url(browser):
    page.goto('https://leetcode.cn/')
    page.wait_for_selector('text="每日 1 题"', state="visible")
    elems = page.get_by_text("每日 1 题").locator("..").locator("..")
    # print(elems.count())
    elem = elems.nth(0)
    return elem.get_attribute('href')


# 进入题目所在页
def problem_page(url, lang):
    page.goto(url)

    # 等待页面加载
    page.wait_for_selector('[data-e2e-locator="console-testcase-tag"]', state="visible")
    cases = page.locator('[data-e2e-locator="console-testcase-tag"]')

    # 更换至指定语言
    page.get_by_text("C++").click()
    page.get_by_text(lang, exact=True).last.click()
    set_types(page, lang)

    # print(cases.count())
    for case in cases.all():
        # case.click()
        case.evaluate("element => element.click()") # 切换测试用例
        input_elems = page.get_by_placeholder('请输入测试用例')
        output_elems = convert(input_elems, lang)
        print(output_elems)



playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=50)
page = browser.new_page()
problem_page(get_daily_problem_url(browser), 'Java')
# problem_page(r'https://leetcode.cn/problems/rearranging-fruits/description/?envType=daily-question&envId=2025-08-02', 'Java')
