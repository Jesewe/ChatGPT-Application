# ChatGPT Application

This is a ChatGPT application built using the [Flet](https://flet.dev/) framework for the frontend and [g4f](https://github.com/xtekky/gpt4free) for connecting to the OpenAI GPT-4 models. The application allows users to interact with different GPT-4 models and change the theme of the application between light and dark modes.

## Features

- **Multiple GPT-4 Models**: Users can select from different GPT-4 models (`gpt-4`, `gpt-4-turbo`, `gpt-4o`) to send their messages.
- **Theme Switching**: Users can switch between light and dark themes.
- **Chat History**: Displays the chat history with user and ChatGPT messages.
- **Settings Dialog**: A settings dialog for changing the model and theme.

## Requirements

- Python 3.7+
- `flet` package
- `g4f` package

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Jesewe/ChatGPT-Application.git
    cd ChatGPT-Application
    ```

2. Install the required packages:
    ```bash
    pip install flet g4f
    ```

## Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. Interact with the ChatGPT application by typing your messages and clicking the "Send" button.

3. Open the settings dialog by clicking the "Settings" button. Here you can switch between different models and themes.

## Code Explanation

- The application is built using the Flet framework for the UI components.
- The `g4f` client is used to communicate with the GPT-4 models.
- The main layout consists of a title, a chat messages container, and input fields for sending messages.
- A settings dialog allows users to select the model and theme.
- The theme of the application is dynamically updated based on user selection to ensure readability.

### Main Components

1. **Models and Themes**: Dropdowns to select the desired GPT-4 model and theme.
    ```python
    models = ["gpt-4", "gpt-4-turbo", "gpt-4o"]
    themes = {"Dark": ft.ThemeMode.DARK, "Light": ft.ThemeMode.LIGHT}
    ```

2. **Message Container**: A list view to display chat messages.
    ```python
    messages_container = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)
    ```

3. **Send Message Function**: Handles sending messages and displaying responses.
    ```python
    def send_message(e: ft.ControlEvent):
        ...
    ```

4. **Settings Dialog**: Allows users to change the theme and model.
    ```python
    settings_dialog = ft.AlertDialog(
        ...
    )
    ```

## Contributing

Please feel free to submit a pull request and fork this repository in order to contribute. Any improvements or bug fixes are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.