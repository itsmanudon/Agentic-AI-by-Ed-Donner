# GPT-5 Chat Interface

A modern, feature-rich chat interface powered by GPT-5 with optional cross-session context persistence. Built with Gradio for a clean, responsive user experience.

![GPT-5 Chat Interface](https://img.shields.io/badge/GPT--5-Powered-blue)
![Gradio](https://img.shields.io/badge/Built%20with-Gradio-orange)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 🚀 Features

### Core Functionality
- **🤖 GPT-5 Powered**: Latest OpenAI model for superior responses
- **💬 Real-time Chat**: Instant message processing and response generation
- **🎨 Modern UI**: Clean, responsive Gradio interface with Soft theme
- **📱 Cross-platform**: Works on desktop, tablet, and mobile devices

### Context Persistence
- **🔄 Cross-session Memory**: Optional conversation history between sessions
- **⚙️ User Control**: Toggle context persistence on/off as needed
- **🧹 Smart Cleanup**: Automatic context management (50 exchange limit)
- **💾 Persistent Settings**: Your preferences are remembered

### Advanced Features
- **📊 Error Handling**: Graceful error management and user feedback
- **🔧 Configurable**: Easy to customize and extend
- **📝 Well-documented**: Comprehensive inline documentation
- **🛡️ Secure**: Local data storage, no external dependencies

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Technical Details](#technical-details)
- [File Structure](#file-structure)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Internet connection for GPT-5 API calls

### Setup Steps

1. **Clone or download the project**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd path/to/gpt5-chat-interface
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python GPT-5-Trial.py
   ```

5. **Access the interface**
   Open your browser and go to: `http://localhost:7860`

## 🚀 Quick Start

1. **Start the application**
   ```bash
   python GPT-5-Trial.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:7860`

3. **Start chatting**
   - Type your message in the input box
   - Press Enter or click Send
   - Get instant responses from GPT-5

4. **Configure context persistence**
   - Use the checkbox to enable/disable cross-session memory
   - Clear chat button resets the conversation

## 📖 Usage

### Basic Chatting
- **Send Messages**: Type in the text box and press Enter
- **View History**: All conversations appear in the chat window
- **Clear Chat**: Use the "Clear Chat" button to reset the conversation

### Context Persistence
- **Enable Context**: Check the "Enable Context Persistence" box
  - Conversations are saved between sessions
  - Previous chats load automatically
  - Context is limited to 50 exchanges for efficiency

- **Disable Context**: Uncheck the box
  - Fresh start every session
  - No data is saved
  - Existing context is automatically cleared

### Settings Management
- **Automatic Saving**: Your context preference is saved automatically
- **Persistent Settings**: Your choice is remembered next time
- **Status Feedback**: Toggle changes show confirmation messages

## ⚙️ Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### File Locations
- **Context Data**: `chat_context.json` (created automatically)
- **Settings**: `chat_settings.json` (created automatically)
- **Logs**: Console output for debugging

### Customization Options
You can modify these settings in the code:

```python
# In GPT5Chat.__init__()
self.max_context_length = 50  # Change context limit
self.context_file = "chat_context.json"  # Change file name
self.settings_file = "chat_settings.json"  # Change settings file
```

## 🔧 Technical Details

### Architecture
- **Frontend**: Gradio web interface
- **Backend**: Python with OpenAI API integration
- **Data Storage**: Local JSON files for context and settings
- **State Management**: In-memory conversation history with file persistence

### Context Management
- **Smart Trimming**: Only keeps the last 50 exchanges
- **Token Efficiency**: Prevents context bloat for GPT-5
- **Automatic Cleanup**: Disabled context clears existing data
- **Error Recovery**: Graceful handling of file operations

### API Integration
- **Model**: GPT-5 (latest OpenAI model)
- **Token Limit**: 10,000 completion tokens per response
- **Error Handling**: Comprehensive exception management
- **Rate Limiting**: Built-in API call management

### Data Flow
1. **User Input** → Text processing
2. **Context Loading** → Previous conversations (if enabled)
3. **Message Preparation** → System prompt + history + current message
4. **API Call** → GPT-5 processing
5. **Response Handling** → Extract and display response
6. **Context Saving** → Update local files (if enabled)

## 📁 File Structure

```
gpt5-chat-interface/
├── GPT-5-Trial.py          # Main application file
├── requirements.txt         # Python dependencies
├── read.md                 # This documentation
├── .env                    # Environment variables (create this)
├── chat_context.json       # Conversation history (auto-created)
├── chat_settings.json      # User settings (auto-created)
└── .gitignore             # Git ignore file
```

### Generated Files
- **`chat_context.json`**: Stores conversation history when context is enabled
- **`chat_settings.json`**: Stores user preferences (context toggle state)

## 📚 API Reference

### GPT5Chat Class

#### `__init__()`
Initializes the chat interface with OpenAI client and file paths.

#### `load_settings()`
Loads user settings from the settings file.
- **Returns**: `bool` - True if context persistence is enabled

#### `save_settings(context_enabled)`
Saves user settings to the settings file.
- **Parameters**: `context_enabled (bool)` - Context persistence setting

#### `load_context()`
Loads conversation context from file if context persistence is enabled.
- **Returns**: `list` - List of conversation tuples

#### `save_context(history)`
Saves conversation context to file if context persistence is enabled.
- **Parameters**: `history (list)` - Conversation history

#### `system_prompt()`
Generates the system prompt for GPT-5.
- **Returns**: `str` - System prompt

#### `chat(message, history, context_enabled)`
Main chat function that handles user messages and generates AI responses.
- **Parameters**: 
  - `message (str)` - User's input message
  - `history (list)` - Current conversation history
  - `context_enabled (bool)` - Whether context persistence is enabled
- **Returns**: `tuple` - (updated_history, empty_string)

### UI Functions

#### `create_ui()`
Creates and configures the Gradio user interface.
- **Returns**: `gr.Blocks` - Configured Gradio interface

## 🔍 Troubleshooting

### Common Issues

#### "OpenAI API Key not set"
- **Solution**: Create a `.env` file with your API key
- **Format**: `OPENAI_API_KEY=your_key_here`

#### "This site can't be reached"
- **Solution**: Use `localhost` instead of `0.0.0.0`
- **Alternative**: Try `http://127.0.0.1:7860`

#### "Error: Invalid API key"
- **Solution**: Check your OpenAI API key in the `.env` file
- **Verify**: Ensure the key is valid and has sufficient credits

#### "Port 7860 is already in use"
- **Solution**: Change the port in the launch configuration
- **Code**: Modify `server_port=7860` to another port

#### Context not persisting
- **Check**: Ensure "Enable Context Persistence" is checked
- **Verify**: Check that `chat_context.json` exists and is writable
- **Debug**: Look for error messages in the console

### Performance Tips
- **Context Limit**: The 50-exchange limit helps maintain performance
- **Clear Regularly**: Use "Clear Chat" to reset long conversations
- **Disable Context**: Turn off context persistence for fresh starts

### Debug Mode
Enable detailed error messages by setting `show_error=True` in the launch configuration.

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include inline comments for complex logic
- Update documentation for new features

### Testing
- Test with different context settings
- Verify error handling
- Check cross-platform compatibility
- Validate API integration

## 📄 License

This project is part of the Agentic AI course materials and is provided for educational purposes.

## 🙏 Acknowledgments

- **OpenAI**: For providing the GPT-5 API
- **Gradio**: For the excellent web interface framework
- **Python Community**: For the robust ecosystem

## 📞 Support

For issues, questions, or contributions:
- Check the troubleshooting section above
- Review the inline documentation in the code
- Ensure all dependencies are properly installed
- Verify your OpenAI API key is valid and has credits

---

**Happy Chatting! 🤖💬**

