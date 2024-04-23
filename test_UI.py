from playwright.sync_api import Page, expect
import pytest
import models.openPages

@pytest.fixture(autouse=True)
def go_to_uiTesting(page:Page):
    page.goto("http://www.uitestingplayground.com/")
    
def test_dynamicId(page:Page):
    models.openPages.gotoButtonLinks(page,link="Dynamic ID")
    
    dynamic_btn = page.get_by_role("button",name="Button with Dynamic ID")
    expect(dynamic_btn).to_be_enabled
    
    dynamic_btn.click()
    
    #restart
    page.goto("http://www.uitestingplayground.com/dynamicid")    
    dynamic_btn = page.get_by_role("button",name="Button with Dynamic ID")
    expect(dynamic_btn).to_be_enabled
    dynamic_btn.click()
    
def test_Class_Attribute(page:Page):
    models.openPages.gotoButtonLinks(page,link="Class Attribute")
    
    correct_btn = page.locator("//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]")
    expect(correct_btn).to_be_visible()
    correct_btn.click()
    
def test_HiddenLayers(page:Page):
    models.openPages.gotoButtonLinks(page,link="Hidden Layers")
    
    green_btn = page.locator("button#greenButton")
    green_btn.click()
    
    #now the blue button should be available
    blue_btn = page.locator("button#blueButton")
    expect(blue_btn).to_be_enabled()
    
    
def test_LoadDelay(page:Page):    
    models.openPages.gotoButtonLinks(page,link="Load Delay")
            
    enabledBtn = page.get_by_role("button",name="Button Appearing After Delay")
    enabledBtn.wait_for(timeout=10_000)
    expect(enabledBtn).to_be_enabled()
    
def test_ajaxData(page:Page):    
    models.openPages.gotoButtonLinks(page,link="AJAX Data")
    
    ajaxTrigger = page.get_by_role("button",name="Button Triggering AJAX Request")
    ajaxTrigger.click()
    
    successMessage = page.locator("p.bg-success")
    successMessage.wait_for()
    
    expect(successMessage).to_be_visible()
    
def test_clientSideDelay(page:Page):
    models.openPages.gotoButtonLinks(page,link="Client Side Delay")
    
    btn_Trigger = page.get_by_role("button",name="Button Triggering Client Side Logic")
    btn_Trigger.click()
    
    successMessage = page.locator("p.bg-success")
    successMessage.wait_for()
    
    expect(successMessage).to_be_visible()
    
def test_click(page:Page):
    models.openPages.gotoButtonLinks(page,link="Click")
    
    clickBtn = page.get_by_role("button",name="Button That Ignores DOM Click Event")
    clickBtn.click()
    
    expect(clickBtn).to_have_class("btn btn-success")
    
def test_text_input(page:Page):
    models.openPages.gotoButtonLinks(page,link="Text Input")
    
    inputArea = page.get_by_placeholder("MyButton")
    inputArea.fill("asdf")
    
    button = page.locator("button.btn-primary")
    button.click()
    
    expect(button).to_have_text("asdf")
    
def test_scrollbars(page:Page):
    models.openPages.gotoButtonLinks(page,link="Scrollbars")
    
    hidingButton = page.get_by_role("button",name="Hiding Button")
    hidingButton.scroll_into_view_if_needed()
    
    hidingButton.click()
    expect(hidingButton).to_be_visible()
    
def test_dynamicTable(page:Page):
    models.openPages.gotoButtonLinks(page,link="Dynamic Table")
    
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