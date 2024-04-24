from playwright.sync_api import Page

def gotoButtonLinks(page:Page,link)->str:
    btn = page.get_by_role("link",name=link)
    btn.click()
    
def loginSampleApp(page:Page,username:str,password:str):
    username_area = page.get_by_placeholder("User Name")
    password_area = page.get_by_placeholder("********")
    loginButton = page.get_by_role("button",name="Log In")
    username_area.fill(username)
    password_area.fill(password)
    
    loginButton.click()