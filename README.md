# ChatGPT Application

The ChatGPT Application is a user-friendly interface built with Flet that allows users to interact with the ChatGPT models provided by the `g4f.client` library. The application features a customizable interface with support for different themes and models, making it a versatile tool for various use cases.

## Features

- **Model Selection:** Choose from multiple ChatGPT models, including "gpt-4," "gpt-4-turbo," and "gpt-4o."
- **Theme Customization:** Switch between Dark and Light themes for a better visual experience.
- **Persistent Settings:** Save and load user preferences (theme and model) between sessions.
- **Message History:** View and manage chat history with the ability to clear previous messages.
- **Settings Dialog:** Easily configure application settings through a user-friendly dialog.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Jesewe/chatgpt-application.git
   cd chatgpt-application
   ```

2. **Install the required dependencies:**

   ```bash
   pip install flet g4f
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

## Configuration

The application saves user preferences (selected theme and model) to a configuration file located at `~/Documents/chat_app_config.json`. This ensures that your settings are retained between sessions.

## Usage

1. **Starting the Application:** Run the `main.py` script to start the application. The main window will open, displaying the chat interface.
2. **Sending Messages:** Enter your message in the input field and click the "Send" button. The message will be sent to the selected ChatGPT model, and the response will be displayed in the chat history.
3. **Changing Settings:** Click the "Settings" button to open the settings dialog. Here, you can change the theme and model. Your changes will be saved automatically.
4. **Clearing History:** Click the "Clear History" button to clear the chat history.

## Contributing

Please feel free to submit a pull request and fork this repository in order to contribute. Any improvements or bug fixes are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.