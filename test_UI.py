from playwright.sync_api import Page, expect, TimeoutError
import pytest
import models.shortCuts
from tkinter import Tk

@pytest.fixture(autouse=True)
def go_to_uiTesting(page:Page):
    page.goto("http://www.uitestingplayground.com/")
    
def test_dynamicId(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Dynamic ID")
    
    dynamic_btn = page.get_by_role("button",name="Button with Dynamic ID")
    expect(dynamic_btn).to_be_enabled
    
    dynamic_btn.click()
    
    #restart
    page.goto("http://www.uitestingplayground.com/dynamicid")    
    dynamic_btn = page.get_by_role("button",name="Button with Dynamic ID")
    expect(dynamic_btn).to_be_enabled
    dynamic_btn.click()
    
def test_Class_Attribute(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Class Attribute")
    
    correct_btn = page.locator("//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]")
    expect(correct_btn).to_be_visible()
    correct_btn.click()
    
def test_HiddenLayers(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Hidden Layers")
    
    green_btn = page.locator("button#greenButton")
    green_btn.click()
    
    #now the blue button should be available
    blue_btn = page.locator("button#blueButton")
    expect(blue_btn).to_be_enabled()
    
    
def test_LoadDelay(page:Page):    
    models.shortCuts.gotoButtonLinks(page,link="Load Delay")
            
    enabledBtn = page.get_by_role("button",name="Button Appearing After Delay")
    enabledBtn.wait_for(timeout=10_000)
    expect(enabledBtn).to_be_enabled()
    
def test_ajaxData(page:Page):    
    models.shortCuts.gotoButtonLinks(page,link="AJAX Data")
    
    ajaxTrigger = page.get_by_role("button",name="Button Triggering AJAX Request")
    ajaxTrigger.click()
    
    successMessage = page.locator("p.bg-success")
    successMessage.wait_for()
    
    expect(successMessage).to_be_visible()
    
def test_clientSideDelay(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Client Side Delay")
    
    btn_Trigger = page.get_by_role("button",name="Button Triggering Client Side Logic")
    btn_Trigger.click()
    
    successMessage = page.locator("p.bg-success")
    successMessage.wait_for()
    
    expect(successMessage).to_be_visible()
    
def test_click(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Click")
    
    clickBtn = page.get_by_role("button",name="Button That Ignores DOM Click Event")
    clickBtn.click()
    
    expect(clickBtn).to_have_class("btn btn-success")
    
def test_text_input(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Text Input")
    
    inputArea = page.get_by_placeholder("MyButton")
    inputArea.fill("asdf")
    
    button = page.locator("button.btn-primary")
    button.click()
    
    expect(button).to_have_text("asdf")
    
def test_scrollbars(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Scrollbars")
    
    hidingButton = page.get_by_role("button",name="Hiding Button")
    hidingButton.scroll_into_view_if_needed()
    
    hidingButton.click()
    expect(hidingButton).to_be_visible()
    
def test_dynamicTable(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Dynamic Table")
    
    headers = page.get_by_role("columnheader")        
    cpu_column = None
    
    for cpuIndex in range(headers.count()):
        CPUheader = headers.nth(cpuIndex)
        
        if CPUheader.inner_text() == "CPU": 
            cpu_column=cpuIndex
            break        
        
    assert cpu_column !=None
    ###
    rowGroup = page.get_by_role("rowgroup").last
    chromeRow = rowGroup.get_by_role("row").filter(has_text="Chrome")
            
    CPUvalue = chromeRow.get_by_role("cell").nth(cpu_column)
    
    ######expected value taken from the area    
    valueAreaText = page.locator("p.bg-warning").inner_text()
    expectedValue = valueAreaText.split()[-1] #this will take something like **%
    
    expect(CPUvalue).to_have_text(expectedValue)
    
def test_verify_text(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Verify Text")
    
    textArea = page.locator("div.bg-primary")
    
    expect(textArea).to_have_text("Welcome UserName!")
    
def test_progressBar(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Progress Bar")
    
    progressBar = page.get_by_role("progressbar")
    start_btn = page.get_by_role("button",name="Start")    
    stop_btn = page.locator("button#stopButton")
    
    start_btn.click()
    
    while(True):
        if int(progressBar.get_attribute("aria-valuenow"))>=75:
            stop_btn.click()
            break
        
    lastValue = int(progressBar.get_attribute("aria-valuenow"))
    assert(lastValue>=75) #expect doesn't work with integer values
    
def test_visibility(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Visibility")
    
    btn_Hide = page.get_by_role("button",name="Hide")
    btn_Opactiy0 = page.get_by_role("button",name="Opacity 0")
    btn_removed = page.get_by_role("button",name="Removed")
    btn_visibilityHidden = page.get_by_role("button",name="Visibility Hidden")
    btn_zeroWidth = page.get_by_role("button",name="Zero Width")
    btn_displayNone = page.get_by_role("button",name="Display None")
    btn_overlapped = page.get_by_role("button",name="Overlapped")
    btn_offscreen = page.get_by_role("button",name="Offscreen")
    
    btn_Hide.click()
    
    expect(btn_Opactiy0).to_have_css("opacity","0")
    expect(btn_removed).to_be_hidden()
    expect(btn_visibilityHidden).to_be_hidden()
    expect(btn_zeroWidth).to_have_css("width","0px")
    expect(btn_displayNone).to_be_hidden()
    
    #Overlapped button is still available but can not be clicked.
    #We can't see it with our eyes but is still visible on computer vision
    #So we'll try to click until 2 secs. Then raise error. Which is fine
    with pytest.raises(TimeoutError):
        btn_overlapped.click(timeout=2000)
        
    expect(btn_offscreen).not_to_be_in_viewport()
    
def test_sample_app(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Sample App")
    username = "myName"
        
    #Invalid Login
    models.shortCuts.loginSampleApp(page,username=username,password="asd")        
        
    loginStatus = page.locator("label#loginstatus")
    expect(loginStatus).to_have_text("Invalid username/password")
    
    #Valid Login
    models.shortCuts.loginSampleApp(page,username=username,password="pwd")
    
    loginStatus = page.locator("label#loginstatus")
    expect(loginStatus).to_have_text(f"Welcome, {username}!")
    
def test_mouse_over(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Mouse Over")
    hoverLink = page.get_by_title("Click me")

    hoverLink.hover()
    
    active_link = page.get_by_title("Active Link")    
    active_link.click(click_count=2)
    
    clickCount = page.locator("span#clickCount")
    
    expect(clickCount).to_have_text("2")
    
def test_overlappedElement(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Overlapped Element")
    testString = "RandomName"
    
    
    nameInput = page.get_by_placeholder("Name")
    overlapArea = nameInput.locator("..")
    overlapArea.hover()
    
    page.mouse.wheel(delta_x=0,delta_y=300)
        
    nameInput.fill(testString)
    
    expect(nameInput).to_have_value(testString)
    overlapArea.screenshot(path="overlappedArea_Test.jpeg")
    
    
    
def test_shadowDom(page:Page):
    models.shortCuts.gotoButtonLinks(page,link="Shadow DOM")
    textArea = page.locator("input#editField")
    generate_btn = page.locator("button#buttonGenerate")
    generate_btn.click()
    
    textArea.click()
    
    page.keyboard.press("Control+KeyA")
    page.keyboard.press("Control+KeyC")
    
    page.keyboard.press("Backspace")
    
    data = Tk().clipboard_get()
    
    generate_btn.click(click_count=3)
    textArea.click()
    page.keyboard.press("Control+KeyA")
    page.keyboard.press("Control+KeyV")
    
    page.keyboard.press("Control+KeyA")
    page.keyboard.press("Control+KeyC")
    
    data2 = Tk().clipboard_get()
    
    assert data == data2               