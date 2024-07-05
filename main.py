import os
import json
import flet as ft
from g4f.client import Client

client = Client()

MODELS = [
    "gpt-4", "gpt-4-turbo", "gpt-4o"
]

THEMES = {
    "Dark": ft.ThemeMode.DARK,
    "Light": ft.ThemeMode.LIGHT
}

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "chat_app_config.json")

class ChatApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.load_config()
        
        self.page.title = "ChatGPT Application"
        self.page.theme_mode = THEMES.get(self.config.get("theme", "Dark"))
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.messages_container = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)
        self.chat_history = []

        self.selected_model = ft.Dropdown(
            width=200,
            options=[ft.dropdown.Option(model) for model in MODELS],
            value=self.config.get("model", "gpt-4-turbo"),
            on_change=self.change_model
        )

        self.selected_theme = ft.Dropdown(
            width=200,
            options=[ft.dropdown.Option(theme) for theme in THEMES],
            value=self.config.get("theme", "Dark"),
            on_change=self.change_theme
        )

        self.user_input = ft.TextField(hint_text="Enter your message", expand=True)
        self.send_button = ft.ElevatedButton(text="Send", on_click=self.send_message)
        self.clear_button = ft.ElevatedButton(text="Clear History", on_click=self.clear_history)
        self.settings_button = ft.ElevatedButton(text="Settings", on_click=self.open_settings)

        self.settings_dialog = self.create_settings_dialog()

        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("ChatGPT Application", style="headlineMedium", color=ft.colors.CYAN),
                                    ft.Text("Author: ItsJesewe", style="bodyMedium", color=ft.colors.GREY)
                                ]
                            ),
                            ft.Container(expand=True),
                            self.settings_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.messages_container,
                    ft.Row([self.user_input, self.send_button, self.clear_button], spacing=10)
                ],
                spacing=20,
                expand=True,
            )
        )

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                self.config = json.load(file)
        else:
            self.config = {"theme": "Dark", "model": "gpt-4-turbo"}

    def save_config(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.config, file)

    def get_text_color(self):
        return ft.colors.WHITE if self.page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK

    def change_theme(self, e: ft.ControlEvent):
        selected_theme_value = e.control.value
        self.page.theme_mode = THEMES[selected_theme_value]
        self.config["theme"] = selected_theme_value
        self.save_config()
        self.update_text_colors()

    def change_model(self, e: ft.ControlEvent):
        selected_model_value = e.control.value
        self.config["model"] = selected_model_value
        self.save_config()

    def update_text_colors(self):
        for control in self.messages_container.controls:
            if isinstance(control, ft.Text):
                control.color = self.get_text_color()
        self.page.update()

    def send_message(self, e: ft.ControlEvent):
        user_message = self.user_input.value.strip()
        model = self.selected_model.value
        if user_message:
            self.add_message("User", user_message, self.get_text_color())
            self.user_input.value = ""
            self.page.update()

            bot_message = self.get_bot_response(model, user_message)
            self.add_message("ChatGPT", bot_message, ft.colors.LIGHT_BLUE)
            self.user_input.focus()

    def get_bot_response(self, model, user_message):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.choices[0].message.content
        except Exception as ex:
            return f"Error: {ex}"

    def add_message(self, sender: str, message: str, color: str):
        self.messages_container.controls.append(ft.Text(f"{sender}: {message}", color=color))
        self.chat_history.append((sender, message))
        self.page.update()

    def clear_history(self, e: ft.ControlEvent):
        self.messages_container.controls.clear()
        self.chat_history.clear()
        self.page.update()

    def open_settings(self, e: ft.ControlEvent):
        self.page.dialog = self.settings_dialog
        self.settings_dialog.open = True
        self.page.update()

    def close_settings(self, e: ft.ControlEvent):
        self.settings_dialog.open = False
        self.page.update()

    def create_settings_dialog(self):
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Settings"),
            content=ft.Column(
                [
                    ft.Text("Choose Theme:", style="bodyMedium", color=ft.colors.GREY),
                    self.selected_theme,
                    ft.Text("Choose Model:", style="bodyMedium", color=ft.colors.GREY),
                    self.selected_model,
                ],
                spacing=20
            ),
            actions=[
                ft.TextButton("Close", on_click=self.close_settings)
            ]
        )

def main(page: ft.Page):
    ChatApp(page)

ft.app(target=main)