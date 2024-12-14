import cv2
import pytesseract
import pyautogui
import numpy as np
import time

# Configure Tesseract (make sure Tesseract is installed on your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust for your system

def find_and_click_dice(template_path="roll.png"):
    """
    Detects the red dice button on the screen and clicks it.
    """
    # Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load the dice template
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    # Convert both images to grayscale
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Match template
    result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Threshold for detection
    if max_val > 0.8:
        w, h = template_gray.shape[::-1]
        dice_center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
        pyautogui.click(dice_center)  # Click on the detected location
        print(f"Clicked red dice at {dice_center}")
        return True
    print("Red dice not found on the screen.")
    return False


def is_int_13(region):
    """
    Checks if the screenshot of the specified region contains 'INT 13'.
    """
    # Take a screenshot of the specific region
    screenshot = pyautogui.screenshot(region=(1200,500, 1400, 800))
    screenshot.save("debug_int_region.png")  # Save for debugging purposes
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Perform OCR to extract text
    text = pytesseract.image_to_string(image, config='--psm 6')  # Use page segmentation mode 6 for uniform blocks
    print(f"OCR Text: {text.strip()}")  # Log the extracted text for debugging
    text = text.upper()
    print(text)
    # Check if 'INT 13' is in the extracted text
    return "INT 13" in text


def auto_click_until_int(template_path="red_dice_template.png", int_region=(0, 100, 0, 100)):
    """
    Main loop to click the dice until the text 'INT 13' appears in the specified region.
    """
    # Save initial region preview for debugging
    screenshot = pyautogui.screenshot()
    screenshot.save("int_region_preview.png")
    print("INT region preview saved as 'int_region_preview.png'. Verify this file for accuracy.")

    while True:
        # Check if 'INT 13' is present
        if is_int_13(int_region):
            print("Found 'INT 13'! Stopping.")
            break

        # Click the dice
        clicked = find_and_click_dice(template_path)
        if not clicked:
            print("Red dice not found! Stopping the script.")
            break

        # Small delay to avoid spamming
        time.sleep(0.5)


if __name__ == "__main__":
    # Provide the path to your red dice template and the region where the INT is displayed
    red_dice_template_path = "roll.png"  # Prepare this template in advance
    int_screen_region = (1556, 408, 121, 42)  # Adjusted region based on your screen resolution
    auto_click_until_int(template_path=red_dice_template_path, int_region=int_screen_region)
