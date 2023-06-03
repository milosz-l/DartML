from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    # def test_demo_site(self):
    #     self.open("https://seleniumbase.io/demo_page")
    #     self.type("#myTextInput", "This is Automated")
    #     self.click("#myButton")
    #     self.assert_element("tbody#tbodyId")
    #     self.assert_text("Automation Practice", "h3")
    #     self.click_link("SeleniumBase Demo Page")
    #     self.assert_exact_text("Demo Page", "h1")
    #     self.assert_no_js_errors()
    
    def test_sample_page(self):
        self.open("http://localhost:8501")
        self.click_partial_link("Sample")
        # self.click('//button[text()="Browse files"]')
        self.click('p:contains("Use example data")')
        self.assert_element('p:contains("36275 rows")')
        self.assert_element('p:contains("19 columns")')
        # self.click_partial_link("Explore")
