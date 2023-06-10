import cv2


def assert_identical_images(current_image_path, expected_image_path, diff_image_path):
    """
    Asserts that two images are identical.

    Based on the following article:
    Based on https://blog.streamlit.io/testing-streamlit-apps-using-seleniumbase/.
    """
    # load images
    current = cv2.imread(current_image_path)
    expected = cv2.imread(expected_image_path)

    # check if the size of the pictures are identical
    assert current.shape == expected.shape

    # check if all three BGR channels are identical
    difference = cv2.subtract(current, expected)

    # scale the pixel values to enhance differences
    scaled_diff = cv2.convertScaleAbs(difference)

    # save the difference image
    cv2.imwrite(diff_image_path, scaled_diff)

    # assert that the difference is zero
    b, g, r = cv2.split(difference)
    assert cv2.countNonZero(b) == 0
    assert cv2.countNonZero(g) == 0
    assert cv2.countNonZero(r) == 0
