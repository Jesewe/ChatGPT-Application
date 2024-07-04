import flet as ft
from g4f.client import Client

client = Client()

def main(page: ft.Page):
    page.title = "ChatGPT Application"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    models = [
        "gpt-4", "gpt-4-turbo", "gpt-4o"
    ]

    themes = {
        "Dark": ft.ThemeMode.DARK,
        "Light": ft.ThemeMode.LIGHT
    }

    selected_model = ft.Dropdown(
        width=200,
        options=[ft.dropdown.Option(model) for model in models],
        value="gpt-4-turbo"
    )

    selected_theme = ft.Dropdown(
        width=200,
        options=[ft.dropdown.Option(theme) for theme in themes],
        value="Dark",
        on_change=lambda e: change_theme(e)
    )

    messages_container = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)
    chat_history = []

    def get_text_color():
        if page.theme_mode == ft.ThemeMode.DARK:
            return ft.colors.WHITE
        elif page.theme_mode == ft.ThemeMode.LIGHT:
            return ft.colors.BLACK
        else:
            return ft.colors.WHITE if page.platform == 'dark' else ft.colors.BLACK

    def change_theme(e: ft.ControlEvent):
        selected_theme_value = e.control.value
        page.theme_mode = themes[selected_theme_value]
        update_text_colors()
        page.update()

    def update_text_colors():
        for control in messages_container.controls:
            if isinstance(control, ft.Text):
                control.color = get_text_color()
        page.update()

    def send_message(e: ft.ControlEvent):
        user_message = user_input.value.strip()
        model = selected_model.value
        if user_message:
            add_message("User", user_message, get_text_color())
            user_input.value = ""
            page.update()

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": user_message}],
                )
                bot_message = response.choices[0].message.content
            except Exception as ex:
                bot_message = f"Error: {ex}"

            add_message("ChatGPT", bot_message, ft.colors.LIGHT_BLUE)
            user_input.focus()

    def add_message(sender: str, message: str, color: str):
        messages_container.controls.append(ft.Text(f"{sender}: {message}", color=color))
        chat_history.append((sender, message))
        page.update()

    def clear_history(e: ft.ControlEvent):
        messages_container.controls.clear()
        chat_history.clear()
        page.update()

    def open_settings(e: ft.ControlEvent):
        page.dialog = settings_dialog
        settings_dialog.open = True
        page.update()

    user_input = ft.TextField(hint_text="Enter your message", expand=True)
    send_button = ft.ElevatedButton(text="Send", on_click=send_message)
    clear_button = ft.ElevatedButton(text="Clear History", on_click=clear_history)
    settings_button = ft.ElevatedButton(text="Settings", on_click=open_settings)

    settings_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Settings"),
        content=ft.Column(
            [
                ft.Text("Choose Theme:", style="bodyMedium", color=ft.colors.GREY),
                selected_theme,
                ft.Text("Choose Model:", style="bodyMedium", color=ft.colors.GREY),
                selected_model,
            ],
            spacing=20
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_settings())
        ]
    )

    def close_settings():
        settings_dialog.open = False
        page.update()

    page.add(
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
                        settings_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                messages_container,
                ft.Row([user_input, send_button, clear_button], spacing=10)
            ],
            spacing=20,
            expand=True,
        )
    )

ft.app(target=main)