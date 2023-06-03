from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)
import time
import cv2

EXPLORE_PAGE_VISUALIZATION_TIME_SLEEP = 3

class MyTestClass(BaseCase):
    
    def test_explore_page(self):
        """
        Test whether visualizations on Explore page are rendered correctly
        """
        self.open("http://localhost:8501")
        self.click_partial_link("Sample")
        # self.click('//button[text()="Browse files"]')
        self.click('p:contains("Use example data")')
        self.assert_element('p:contains("36275 rows")')
        self.assert_element('p:contains("19 columns")')
        self.click_partial_link("Explore")
        time.sleep(EXPLORE_PAGE_VISUALIZATION_TIME_SLEEP)
        self.save_screenshot("tests/functional_tests/current_data/current_explore_page.png")

        current = cv2.imread("tests/functional_tests/current_data/current_explore_page.png")
        expected = cv2.imread("tests/functional_tests/expected_data/expected_explore_page.png")

        # check if the size of the pictures are identical
        assert current.shape == expected.shape

        # check if all three BGR channels are identical
        difference = cv2.subtract(current, expected)
        b, g, r = cv2.split(difference)
        assert cv2.countNonZero(b) == cv2.countNonZero(g) == cv2.countNonZero(r) == 0
