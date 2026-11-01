import time
import serial
import pyautogui

# Arduino connection
arduino = serial.Serial("COM6", 9600, timeout=1)
time.sleep(2)
arduino.reset_input_buffer()

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# Cursor settings
SENSITIVITY = 400
MAX_SPEED = 35

# Button settings
motion_enabled = True
previous_toggle = 1
last_toggle_time = 0

click_held = False
click_start = 0
drag_started = False

print("MotionSync ready!")
print("Button 1: Short press = Click")
print("Button 1: Long press = Drag")
print("Button 2: Motion ON/OFF")
print("Move cursor to top-left corner for failsafe.")

try:
    while True:

        line = arduino.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        try:
            ax, ay, click_state, toggle_state = map(
                int, line.split(",")
            )
        except (ValueError, TypeError):
            continue

        now = time.monotonic()

        # BUTTON 2: Motion ON/OFF
        if (
            toggle_state == 0
            and previous_toggle == 1
            and now - last_toggle_time > 0.3
        ):
            motion_enabled = not motion_enabled
            last_toggle_time = now

            print(
                "Motion:",
                "ON" if motion_enabled else "OFF"
            )

        previous_toggle = toggle_state

        # BUTTON 1: Short click / Long press drag

        # Button pressed
        if click_state == 0 and not click_held:
            click_held = True
            click_start = now
            drag_started = False

        # Long press: begin dragging
        if click_state == 0 and click_held and not drag_started:
            if now - click_start >= 0.5:
                pyautogui.mouseDown(button="left")
                drag_started = True

        # Button released
        elif click_state == 1 and click_held:

            if drag_started:
                pyautogui.mouseUp(button="left")

            else:
                pyautogui.click(button="left")

            click_held = False
            drag_started = False

        # CURSOR MOVEMENT
        if motion_enabled:

            dx = int(ax / SENSITIVITY)
            dy = int(ay / SENSITIVITY)

            dx = max(-MAX_SPEED, min(MAX_SPEED, dx))
            dy = max(-MAX_SPEED, min(MAX_SPEED, dy))

            if dx or dy:

                x, y = pyautogui.position()
                width, height = pyautogui.size()

                new_x = max(10, min(width - 10, x + dx))
                new_y = max(10, min(height - 10, y - dy))

                pyautogui.moveTo(
                    new_x, new_y, duration=0
                )

except KeyboardInterrupt:
    print("MotionSync stopped.")

finally:
    if drag_started:
        pyautogui.mouseUp(button="left")

    arduino.close()