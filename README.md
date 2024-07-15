# ChatGPT Application

This is a ChatGPT Application built using the Flet framework in Python. The application provides a user-friendly interface for interacting with OpenAI's ChatGPT models, allowing users to send messages and receive responses in real-time. The app also includes features like theme selection, model selection, and checking for updates.

## Features

- **Send and receive messages**: Interact with ChatGPT models by sending messages and receiving responses.
- **Theme selection**: Choose between a dark or light theme for the application.
- **Model selection**: Select from different GPT models (gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o).
- **Clear chat history**: Clear the chat history with a single click.
- **Settings dialog**: Access settings to change the theme, model, check for updates, and view the GitHub project link.
- **Copy to clipboard**: Copy messages to the clipboard easily.
- **Version check**: Check for the latest version of the application from the GitHub repository.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Jesewe/ChatGPT-Application.git
    cd ChatGPT-Application
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    python main.py
    ```

## Usage

1. **Send a Message**: Enter your message in the text field and click the "Send" button.
2. **Clear History**: Click the "Clear History" button to clear all messages.
3. **Settings**: Click the settings icon to open the settings dialog where you can change the theme, select a model, check for updates, and view the GitHub project link.
4. **Copy to Clipboard**: Click the copy icon next to a message to copy it to the clipboard.

## Configuration

The application saves its configuration in a JSON file located in the user's Documents folder (`chat_app_config.json`). This file stores the selected theme and model.

## Update Check

The application includes a feature to check for updates from the GitHub repository. To check for updates, open the settings dialog and click the "Check for Updates" button. If a new version is available, a notification will appear.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements and new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.