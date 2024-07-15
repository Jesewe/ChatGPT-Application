import os
import json
import flet as ft
from g4f.client import Client
from datetime import datetime
import requests
from packaging import version

client = Client()

MODELS = [
    "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"
]

THEMES = {
    "Dark": ft.ThemeMode.DARK,
    "Light": ft.ThemeMode.LIGHT
}

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "chat_app_config.json")
VERSION = "v1.0.3"
GITHUB_REPO_URL = "https://api.github.com/repos/Jesewe/ChatGPT-Application/tags"
GITHUB_PROJECT_URL = "https://github.com/Jesewe/ChatGPT-Application"

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

        self.selected_model = self.create_dropdown(MODELS, self.config.get("model", "gpt-4-turbo"), self.change_model)
        self.selected_theme = self.create_dropdown(list(THEMES.keys()), self.config.get("theme", "Dark"), self.change_theme)

        self.user_input = ft.TextField(hint_text="Enter your message", expand=True)
        self.send_button = ft.ElevatedButton(text="Send", icon=ft.icons.SEND, on_click=self.send_message)
        self.clear_button = ft.ElevatedButton(text="Clear History", icon=ft.icons.DELETE, on_click=self.clear_history)
        self.settings_button = ft.IconButton(icon=ft.icons.SETTINGS, on_click=self.open_settings)

        self.settings_dialog = self.create_settings_dialog()
        self.page.overlay.append(self.settings_dialog)

        self.setup_ui()

    def setup_ui(self):
        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(name=ft.icons.CHAT, color=ft.colors.CYAN, size=40),
                                            ft.Text("ChatGPT Application", style="headlineMedium", color=ft.colors.CYAN),
                                        ],
                                        spacing=10,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    ft.Text("Author: ItsJesewe", style="bodyMedium", color=ft.colors.GREY)
                                ]
                            ),
                            ft.Container(expand=True),
                            self.settings_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=ft.colors.GREY),
                    self.messages_container,
                    ft.Divider(color=ft.colors.GREY),
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

    def create_dropdown(self, options, default_value, on_change):
        return ft.Dropdown(
            width=200,
            options=[ft.dropdown.Option(option) for option in options],
            value=default_value,
            on_change=on_change
        )

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

            self.add_message("System", "ChatGPT is typing...", ft.colors.GREY, copy_button=False)
            self.page.update()

            bot_message = self.get_bot_response(model, user_message)
            self.messages_container.controls.pop()
            self.add_message("ChatGPT", bot_message, ft.colors.LIGHT_BLUE, copy_button=True)
            self.user_input.focus()

    def get_bot_response(self, model, user_message):
        try:
            prompt = f"""
            You are a helpful and knowledgeable assistant. Here is the context of the conversation so far:
            {self.format_chat_history()}
            
            Respond to the user's new message thoughtfully and informatively:
            User: {user_message}
            """
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as ex:
            return f"Error: Unable to get response from ChatGPT ({ex})"

    def format_chat_history(self):
        return "\n".join(f"{sender}: {message}" for sender, message in self.chat_history)

    def add_message(self, sender: str, message: str, color: str, copy_button: bool = False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_control = ft.Container(
            content=ft.Text(f"[{timestamp}] {sender}: {message}", color=color),
            width=1000
        )
        controls = [message_control]
        if copy_button:
            copy_button_control = ft.IconButton(icon=ft.icons.COPY, on_click=lambda e: self.copy_to_clipboard(message))
            controls.append(copy_button_control)
        self.messages_container.controls.append(ft.Row(controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        self.chat_history.append((sender, message))
        self.page.update()

    def copy_to_clipboard(self, message: str):
        self.page.set_clipboard(message)
        self.page.open(ft.SnackBar(content=ft.Text("Text copied to clipboard!")))

    def clear_history(self, e: ft.ControlEvent):
        self.messages_container.controls.clear()
        self.chat_history.clear()
        self.page.update()

    def open_settings(self, e: ft.ControlEvent):
        self.settings_dialog.open = True
        self.page.update()

    def close_settings(self, e: ft.ControlEvent):
        self.settings_dialog.open = False
        self.page.update()

    def create_settings_dialog(self):
        return ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(name=ft.icons.SETTINGS, color=ft.colors.GREY, size=30),
                    ft.Text("Settings", style="headlineMedium", color=ft.colors.GREY),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            content=ft.Column(
                [
                    ft.Text("Choose Theme:", style="bodyMedium", color=ft.colors.GREY),
                    self.selected_theme,
                    ft.Text("Choose Model:", style="bodyMedium", color=ft.colors.GREY),
                    self.selected_model,
                    ft.Text(f"Version: {VERSION}", style="bodyMedium", color=ft.colors.GREY),
                    ft.ElevatedButton(text="Check for Updates", icon=ft.icons.UPDATE, on_click=self.check_for_updates),
                    ft.TextButton("GitHub Project", icon=ft.icons.LINK, url=GITHUB_PROJECT_URL),
                ],
                spacing=20
            ),
            actions=[
                ft.TextButton("Close", on_click=self.close_settings)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def check_for_updates(self, e: ft.ControlEvent):
        try:
            response = requests.get(GITHUB_REPO_URL)
            response.raise_for_status()
            latest_version = response.json()[0]["name"]
            if version.parse(latest_version) > version.parse(VERSION):
                self.page.open(ft.SnackBar(content=ft.Text(f"New version available: {latest_version}")))
            else:
                self.page.open(ft.SnackBar(content=ft.Text("You are using the latest version")))
        except requests.RequestException as ex:
            self.page.open(ft.SnackBar(content=ft.Text(f"Error checking for updates: {ex}")))

def main(page: ft.Page):
    ChatApp(page)

ft.app(target=main)