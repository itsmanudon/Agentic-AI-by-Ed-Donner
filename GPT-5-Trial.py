"""
GPT-5 Chat Interface with Context Persistence

A Gradio-based chat interface powered by GPT-5 with optional cross-session context persistence.
Users can toggle context persistence on/off and control whether conversations are saved between sessions.

Features:
- GPT-5 powered chat interface
- Optional cross-session context persistence
- User-controlled context toggle
- Smart context management (50 exchange limit)
- Settings persistence
- Clean, modern Gradio UI

Author: AI Assistant
Date: 2025
"""

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Validate OpenAI API key availability
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")

class GPT5Chat:
    """
    Main chat interface class that handles GPT-5 interactions and context persistence.
    
    This class manages:
    - OpenAI API interactions
    - Context persistence (optional)
    - Settings management
    - Conversation history handling
    """
    
    def __init__(self):
        """Initialize the chat interface with OpenAI client and file paths."""
        self.openai = OpenAI()
        
        # File paths for data persistence
        self.context_file = "chat_context.json"  # Stores conversation history
        self.settings_file = "chat_settings.json"  # Stores user preferences
        
        # Context management settings
        self.max_context_length = 50  # Keep only last 50 exchanges to prevent context bloat
        # This limit helps manage token usage and prevents the context from becoming too large
        # for GPT-5 to process efficiently while maintaining recent conversation relevance

    def load_settings(self):
        """
        Load user settings from the settings file.
        
        Returns:
            bool: True if context persistence is enabled, False otherwise.
                 Defaults to True if no settings file exists.
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('context_enabled', True)
            return True  # Default to enabled for better user experience
        except Exception as e:
            print(f"Error loading settings: {e}")
            return True

    def save_settings(self, context_enabled):
        """
        Save user settings to the settings file.
        
        Args:
            context_enabled (bool): Whether context persistence should be enabled
        """
        try:
            data = {
                'context_enabled': context_enabled,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_context(self):
        """
        Load conversation context from file if context persistence is enabled.
        
        Returns:
            list: List of conversation tuples (user_msg, assistant_msg).
                 Empty list if context is disabled or file doesn't exist.
        """
        # Only load context if the feature is enabled
        if not self.load_settings():
            return []
        
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('history', [])
            return []
        except Exception as e:
            print(f"Error loading context: {e}")
            return []

    def save_context(self, history):
        """
        Save conversation context to file if context persistence is enabled.
        
        This method implements smart context management:
        - Only saves if context persistence is enabled
        - Keeps only the last 50 exchanges to prevent context bloat
        - Includes timestamp for debugging purposes
        
        Args:
            history (list): List of conversation tuples (user_msg, assistant_msg)
        """
        # Only save context if the feature is enabled
        if not self.load_settings():
            return
        
        try:
            data = {
                'history': history[-self.max_context_length:],  # Keep only recent history
                'last_updated': datetime.now().isoformat()
            }
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving context: {e}")

    def system_prompt(self):
        """
        Generate the system prompt for GPT-5.
        
        This prompt defines the AI assistant's behavior and capabilities.
        The prompt is generic and doesn't include any specific persona or context.
        
        Returns:
            str: System prompt for GPT-5
        """
        system_prompt = """You are a helpful AI assistant powered by GPT-5. You can help with a wide variety of tasks including:
        
- Answering questions and providing information
- Helping with writing, analysis, and problem-solving
- Engaging in thoughtful conversations
- Providing creative and analytical insights

Be helpful, accurate, and engaging in your responses. If you don't know something, be honest about it."""
        return system_prompt
    
    def chat(self, message, history, context_enabled):
        """
        Main chat function that handles user messages and generates AI responses.
        
        This method:
        1. Updates user settings based on the context toggle
        2. Prepares the conversation history for GPT-5
        3. Sends the request to GPT-5
        4. Saves context if persistence is enabled
        5. Returns the updated conversation history
        
        Args:
            message (str): User's input message
            history (list): Current conversation history
            context_enabled (bool): Whether context persistence is enabled
            
        Returns:
            tuple: (updated_history, empty_string) for Gradio interface
        """
        # Handle empty messages
        if not message.strip():
            return history, ""
        
        # Update settings if the context toggle has changed
        self.save_settings(context_enabled)
        
        # Prepare messages for GPT-5 API call
        messages = [{"role": "system", "content": self.system_prompt()}]
        
        # Add conversation history to provide context for the AI
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        # Add the current user message
        messages.append({"role": "user", "content": message})
        
        try:
            # Call GPT-5 API for response generation
            response = self.openai.chat.completions.create(
                model="gpt-5",  # Using the latest GPT-5 model
                messages=messages,
                max_completion_tokens=10000,  # Allow substantial responses
            )
            
            # Extract the AI's response
            assistant_response = response.choices[0].message.content
            
            # Update the conversation history
            history.append((message, assistant_response))
            
            # Save context after each exchange (only if enabled)
            if context_enabled:
                self.save_context(history)
            
            return history, ""
            
        except Exception as e:
            # Handle API errors gracefully
            error_msg = f"Error: {str(e)}"
            history.append((message, error_msg))
            return history, ""

def create_ui():
    """
    Create and configure the Gradio user interface.
    
    This function sets up:
    - The main chat interface
    - Context persistence toggle
    - Clear chat functionality
    - Message input handling
    - Settings management
    
    Returns:
        gr.Blocks: Configured Gradio interface
    """
    chat_bot = GPT5Chat()
    
    # Load existing context and settings for session initialization
    initial_history = chat_bot.load_context()
    initial_context_enabled = chat_bot.load_settings()
    
    # Create the main Gradio interface
    with gr.Blocks(title="GPT-5 Chat Interface", theme=gr.themes.Soft()) as demo:
        # Header with feature description
        gr.Markdown("""
        # 🤖 GPT-5 Chat Interface
        
        Welcome! This is a chat interface powered by GPT-5. You can ask questions, have conversations, and get help with various tasks.
        
        **Features:**
        - Powered by the latest GPT-5 model
        - Clean and intuitive interface
        - Optional cross-session conversation history
        - Toggle context persistence on/off
        """)
        
        # Settings row with context toggle and clear button
        with gr.Row():
            context_toggle = gr.Checkbox(
                label="Enable Context Persistence",
                value=initial_context_enabled,
                info="Keep conversation history between sessions"
            )
            
            clear = gr.Button("Clear Chat", variant="secondary")
        
        # Main chat interface
        chatbot = gr.Chatbot(
            label="Chat History",
            height=500,
            show_label=True,
            container=True,
            bubble_full_width=False,
            value=initial_history  # Initialize with existing context
        )
        
        # Message input area
        msg = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here...",
            lines=2,
            max_lines=5
        )
        
        # Handle message submission
        def respond(message, history, context_enabled):
            """Process user message and generate AI response."""
            return chat_bot.chat(message, history, context_enabled)
        
        # Connect message input to response function
        msg.submit(respond, [msg, chatbot, context_toggle], [chatbot, msg])
        
        # Handle clear chat functionality
        def clear_chat(context_enabled):
            """
            Clear the current chat and optionally the saved context.
            
            Args:
                context_enabled (bool): Whether context persistence is enabled
                
            Returns:
                tuple: (empty_history, empty_string) to reset the interface
            """
            # Clear the context file if context is enabled
            if context_enabled:
                try:
                    if os.path.exists(chat_bot.context_file):
                        os.remove(chat_bot.context_file)
                except Exception as e:
                    print(f"Error clearing context file: {e}")
            return [], ""
        
        # Connect clear button to clear function
        clear.click(clear_chat, inputs=[context_toggle], outputs=[chatbot, msg])
        
        # Handle context toggle changes
        def on_context_toggle(context_enabled):
            """
            Handle context persistence toggle changes.
            
            When disabled, this automatically clears existing context files
            to ensure a truly fresh start.
            
            Args:
                context_enabled (bool): New context persistence setting
                
            Returns:
                str: Status message confirming the change
            """
            chat_bot.save_settings(context_enabled)
            if not context_enabled:
                # If disabling context, clear the context file for a fresh start
                try:
                    if os.path.exists(chat_bot.context_file):
                        os.remove(chat_bot.context_file)
                except Exception as e:
                    print(f"Error clearing context file: {e}")
            return f"Context persistence {'enabled' if context_enabled else 'disabled'}"
        
        # Connect context toggle to status update
        context_toggle.change(on_context_toggle, inputs=[context_toggle], outputs=[gr.Textbox(label="Status", interactive=False)])
        
        # Footer with additional information
        gr.Markdown("""
        ---
        **About this interface:**
        - Powered by GPT-5
        - Generic AI assistant
        - Optional cross-session context persistence
        - Built with Gradio for easy interaction
        - Toggle context on/off as needed
        """)
    
    return demo

if __name__ == "__main__":
    """
    Main entry point for the application.
    
    Creates the Gradio interface and launches it on localhost:7860.
    The interface will be accessible at http://localhost:7860
    """
    # Create and launch the interface
    demo = create_ui()
    demo.launch(
        server_name="localhost",  # Use localhost for reliable local access
        server_port=7860,         # Standard Gradio port
        share=False,              # Don't create public share link
        show_error=True           # Show detailed error messages
    )