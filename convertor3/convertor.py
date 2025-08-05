from playwright.sync_api import sync_playwright
from convertor_total import convert

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

    # 更换至指定语言
    page.get_by_text("C++").wait_for(state="visible")
    page.get_by_text("C++").click()
    page.get_by_text(lang, exact=True).last.click()

    convert(page, lang)



playwright = sync_playwright().start()
# browser = playwright.chromium.launch(headless=False, slow_mo=100)
browser = playwright.chromium.launch(slow_mo=100)
page = browser.new_page()
problem_page(get_daily_problem_url(browser), 'Java')
# problem_page(r'https://leetcode.cn/problems/binary-tree-tilt/description/', 'Java')
page.close()
