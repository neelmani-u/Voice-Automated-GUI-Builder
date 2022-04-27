import time, sys
import pyautogui as gui
import pywinauto.mouse

from autodesigner.core.core import Core


class DesignerHandler(Core):
    def __init__(self):
        super().__init__()
        self.open_designer()

        # elements definitions
        self.new_btn = self.app.QtDesigner.child_window(title="New", control_type="Button")
        self.designer_close_btn = self.app.QtDesigner.TitleBar2.child_window(title="Close", control_type="Button")
        self.scroll_flag = True
        self.widget_coord = {
            "push_button": (64, 334, 0),
            "tool_button": (64, 361, 0),
            "radio_button": (64, 383, 0),
            "check_box": (64, 408, 0),
            "cmd_button": (64, 430, 0),
            "dialog_button_box": (64, 454, 0),
            "combo_box": (64, 200, 5),
            "line_edit": (64, 248, 5),
            "text_edit": (64, 271, 5),
            "label": (55, 603, 5)
        }
        self.win_region = {
            "top": (454, 134),
            "bottom": (454, 370),
            "left": (310, 230),
            "right": (618, 234),
            "center": (460, 237),
            "top-left": (310, 134),
            "top-right": (618, 134),
            "bottom-left": (310, 370),
            "bottom-right": (618, 370)
        }

    def open_designer(self):
        self.app.start('designer.exe').connect(title="Qt Designer", timeout=10)
        self.app.QtDesigner.set_focus()

    def close_designer(self):
        self.designer_close_btn.wrapper_object().click_input()

    def drag_element_to_window(self, elem_name, pos, x_gap=0, y_gap=0):
        self.wait(1)
        element = self.widget_coord[elem_name]
        region = self.win_region[pos]

        if element[2]:
            if self.scroll_flag:
                gui.moveTo(247, 400, 0.5)
                self.wait(0.5)
                gui.dragTo(247, 765, button='left', duration=0.5)
                self.scroll_flag = False
                self.wait(2)
        else:
            if not self.scroll_flag:
                gui.moveTo(247, 765, 0.5)
                self.wait(0.5)
                gui.dragTo(247, 400, button='left', duration=0.5)
                self.scroll_flag = True
                self.wait(2)

        gui.moveTo(element[0], element[1])
        gui.dragTo(region[0]+x_gap, region[1]+y_gap, button='left', duration=0.5)
        self.wait(1)

    def wait(self, secs):
        time.sleep(secs)

    def rename_element(self, pos, name, x_gap=0, y_gap=0):
        region = self.win_region[pos]
        gui.click(region[0]+x_gap+10, region[1]+y_gap, clicks=2, duration=0.5)
        gui.write(name, interval=0.25)
        gui.press('enter')
        self.wait(1)

    def create_login_form(self):
        self.drag_element_to_window("label", "top")
        self.rename_element("top", "Login")

        self.drag_element_to_window("label", "left")
        self.rename_element("left", "Email :")
        self.drag_element_to_window("line_edit", "center", -50, -11)

        self.drag_element_to_window("label", "left", 0, 50)
        self.rename_element("left", "Password :", 0, 50)
        self.drag_element_to_window("line_edit", "center", -50, 39)

        self.drag_element_to_window("push_button", "bottom", -50)
        self.rename_element("bottom", "Log In", -15)

    def create_signup_form(self):
        self.drag_element_to_window("label", "top")
        self.rename_element("top", "Sign Up")

        self.drag_element_to_window("label", "left", 0, -30)
        self.rename_element("left", "First Name :", 0, -30)
        self.drag_element_to_window("line_edit", "center", -50, -32)

        self.drag_element_to_window("label", "left")
        self.rename_element("left", "Last Name :")
        self.drag_element_to_window("line_edit", "center", -50, -2)

        self.drag_element_to_window("label", "left", 0, 30)
        self.rename_element("left", "Email :", 0, 30)
        self.drag_element_to_window("line_edit", "center", -50, 28)

        self.drag_element_to_window("label", "left", 0, 60)
        self.rename_element("left", "Password :", 0, 60)
        self.drag_element_to_window("line_edit", "center", -50, 58)

        self.drag_element_to_window("label", "left", 0, 90)
        self.rename_element("left", "ReEnter Password :", 0, 90)
        self.drag_element_to_window("line_edit", "center", -50, 88)

        self.drag_element_to_window("push_button", "bottom", -50)
        self.rename_element("bottom", "Sign Up", -5)
