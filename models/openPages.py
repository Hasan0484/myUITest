from playwright.sync_api import Page

def gotoButtonLinks(page:Page,link)->str:
    btn = page.get_by_role("link",name=link)
    btn.click()