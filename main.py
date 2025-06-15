from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import json, os
from vault_utils import encrypt_data, decrypt_data
from config_utils import load_secret_code, save_secret_code

VAULT_FILE = "vault_data.json"

class CalculatorApp(App):
    def build(self):
        self.secret_code = load_secret_code()
        self.operand = ""
        self.layout = GridLayout(cols=4)
        self.display = TextInput(text="", multiline=False, readonly=True)
        self.layout.add_widget(self.display)
        self.layout.add_widget(Label())
        self.layout.add_widget(Label())
        self.layout.add_widget(Button(text="C", on_press=self.clear))

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        for b in buttons:
            self.layout.add_widget(Button(text=b, on_press=self.on_button_press))

        return self.layout

    def clear(self, instance):
        self.display.text = ""

    def on_button_press(self, instance):
        text = instance.text

        if text == "=":
            if self.display.text == self.secret_code:
                self.show_vault()
            else:
                try:
                    self.display.text = str(eval(self.display.text))
                except:
                    self.display.text = "Error"
        else:
            self.display.text += text

    def show_vault(self):
        self.layout.clear_widgets()
        self.display.text = ""
        self.vault_input = TextInput(hint_text="Enter secret note")
        self.layout.add_widget(self.vault_input)

        self.layout.add_widget(Button(text="Save", on_press=self.save_note))
        self.layout.add_widget(Button(text="View", on_press=self.view_notes))
        self.layout.add_widget(Button(text="Back", on_press=self.rebuild_calc))
        self.layout.add_widget(Button(text="Change Password", on_press=self.change_password))
        self.layout.add_widget(Button(text="[Panic] Wipe Vault", on_press=self.panic_wipe, background_color=(1, 0, 0, 1)))

    def save_note(self, instance):
        note = self.vault_input.text
        if note:
            encrypted = encrypt_data([note])
            with open(VAULT_FILE, "wb") as f:
                f.write(encrypted)
            self.vault_input.text = "Saved."

    def view_notes(self, instance):
        if os.path.exists(VAULT_FILE):
            with open(VAULT_FILE, "rb") as f:
                data = f.read()
                notes = decrypt_data(data)
                self.vault_input.text = "\n".join(notes) if notes else "Empty vault."
        else:
            self.vault_input.text = "No data."

    def panic_wipe(self, instance):
        if os.path.exists(VAULT_FILE):
            os.remove(VAULT_FILE)
        if os.path.exists("secret.key"):
            os.remove("secret.key")
        self.vault_input.text = "Vault wiped!"
        self.display.text = ""

    def change_password(self, instance):
        self.layout.clear_widgets()
        self.new_pass_input = TextInput(hint_text="Enter New Password")
        self.layout.add_widget(self.new_pass_input)
        self.layout.add_widget(Button(text="Save New Password", on_press=self.save_new_password))
        self.layout.add_widget(Button(text="Back", on_press=self.show_vault))

    def save_new_password(self, instance):
        new_pass = self.new_pass_input.text.strip()
        if new_pass:
            save_secret_code(new_pass)
            self.secret_code = new_pass
            self.new_pass_input.text = "Password changed!"
        else:
            self.new_pass_input.text = "Enter a valid password"

    def rebuild_calc(self, instance):
        self.layout.clear_widgets()
        self.build()

if __name__ == "__main__":
    CalculatorApp().run()
