from ..designer import DesignerHandler
from pywinauto.controls.win32_controls import ButtonWrapper
import pywinauto


class PyNewFormHandler(DesignerHandler):
    def __init__(self):
        super().__init__()

        # elements definitions
        self.startup_dialog = self.app.QtDesigner.child_window(title="New Form", control_type="Window")
        self.checkbox = self.app.QtDesigner.child_window(title="Show this Dialog on Startup", control_type="CheckBox")
        self.forms_dropdown = self.app.QtDesigner.window(title="templates\\forms")
        self.widgets_dropdown = self.app.QtDesigner.window(title="Widgets")
        self.forms = {
            "bottom_btn_dialog": self.app.QtDesigner.window(title="Dialog with Buttons Bottom"),
            "right_btn_dialog": self.app.QtDesigner.window(title="Dialog with Buttons Right"),
            "no_btn_dialog": self.app.QtDesigner.window(title="Dialog without Buttons"),
            "main_window": self.app.QtDesigner.window(title="Main Window"),
            "widget": self.app.QtDesigner.window(title="Widget")
        }
        self.widgets = {
            "dock_widget": self.app.QtDesigner.window(title="QDockWidget"),
            "frame": self.app.QtDesigner.window(title="QFrame"),
            "group_box": self.app.QtDesigner.window(title="QGroupBox"),
            "scroll_area": self.app.QtDesigner.window(title="QScrollArea"),
            "mdi_area": self.app.QtDesigner.window(title="QMdiArea"),
            "tab_widget": self.app.QtDesigner.window(title="QTabWidget"),
            "tool_box": self.app.QtDesigner.window(title="QToolBox"),
            "stacked_widget": self.app.QtDesigner.window(title="QStackedWidget"),
            "wizard": self.app.QtDesigner.window(title="QWizard"),
            "wizard_page": self.app.QtDesigner.window(title="QWizardPage")
        }
        self.form_create_btn = self.app.QtDesigner.child_window(title="Create", control_type="Button")
        self.form_open_btn = self.app.QtDesigner.child_window(title="Open...", control_type="Button")
        self.form_recent_btn = self.app.QtDesigner.child_window(title="Recent", control_type="Button")
        self.form_close_btn = self.app.QtDesigner.child_window(title="Close", control_type="Button")

    def toggle_startup_dialog(self, state):
        if self.checkbox.exists(timeout=2):
            if state == self.checkbox.get_toggle_state():
                return
            cb_wrapper = self.checkbox.wrapper_object()
            cb_wrapper.click_input()
        else:
            self.check_startup_dialog()
            self.toggle_startup_dialog(state)

    def check_startup_dialog(self):
        if not self.startup_dialog.exists():
            new_btn = self.app.QtDesigner.NewButton2.wrapper_object()
            new_btn.click_input()
            self.wait(2)

    def create_from_templates(self, name):
        try:
            self.check_startup_dialog()
            self.forms[name].wrapper_object().click_input()
            self.form_create_btn.wrapper_object().click_input()
        except pywinauto.findwindows.ElementNotFoundError:
            self.forms_dropdown.click_input()
            self.create_from_templates(name)

    def create_from_widgets(self, name):
        try:
            self.check_startup_dialog()
            self.widgets[name].wrapper_object().click_input()
            self.form_create_btn.wrapper_object().click_input()
        except pywinauto.findwindows.ElementNotFoundError:
            self.widgets_dropdown.click_input()
            self.create_from_widgets(name)

    def open_file(self):
        self.form_open_btn.wrapper_object().click_input()

    def select_from_recent(self):
        self.form_recent_btn.wrapper_object().click_input()

    def close_new_form_dialog(self):
        self.form_close_btn.wrapper_object().click_input()


