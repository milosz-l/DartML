import time

from seleniumbase import BaseCase

from tests.functional_tests import config
from tests.functional_tests.utils import assert_identical_images

BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    def test_explore_page(self):
        """
        Test whether visualizations on Explore page are rendered correctly
        """
        # Load example data and go to Explore page
        self.open(config.HOST_URL)
        self.click_partial_link("Sample")
        self.click('p:contains("Use example data")')
        self.assert_element('p:contains("36275 rows")')
        self.assert_element('p:contains("19 columns")')
        self.click_partial_link("Explore")

        # wait for the visualizations to be rendered
        time.sleep(config.EXPLORE_PAGE_VISUALIZATION_TIME_SLEEP)
        # save screenshot of the page
        current_image_path = (
            "tests/functional_tests/current_data/current_explore_page.png"
        )
        self.save_screenshot(current_image_path)

        expected_image_path = (
            "tests/functional_tests/expected_data/expected_explore_page.png"
        )

        diff_image_path = (
            "tests/functional_tests/current_data/diff_explore_page.png"
        )

        # assert that the pages are identical
        assert_identical_images(current_image_path, expected_image_path, diff_image_path)

    def test_assess_page(self):
        """
        Tests whether results of example training are correct.
        Can be also used to simulate a user that is training models.
        """
        # Load example data and go to Modify & Model page
        self.open(config.HOST_URL)
        self.click_partial_link("Sample")
        self.click('p:contains("Use example data")')
        self.click('span:contains("Modify & Model")')

        # click Generate new report button
        self.click('p:contains("Generate new report")')

        # wait for the report to be generated
        self.wait_for_element(
            'p:contains("Done! Now you can go to Assess tab to see the results!")',
            timeout=config.MODIFY_MODEL_PAGE_MAXIMUM_WAIT_TIME,
        )

        # go to Assess page
        self.click_partial_link("Assess")

        # assert that there is Download data button
        self.assert_element('p:contains("Download data")')

        if config.DOWNLOAD_REPORTS_FROM_ASSESS_PAGE:
            self.click('p:contains("Download data")')
