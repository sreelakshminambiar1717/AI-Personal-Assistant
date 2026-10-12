 AI Personal Assistant

- About the Project

AI Personal Assistant is a locally running AI chatbot developed using Python, Streamlit, and Ollama. It allows users to ask questions and receive AI-generated responses through a simple, interactive web interface.

This project was independently developed to explore local AI integration, chatbot development, and Python application development.

- Features

- Interactive chatbot interface.
- AI-powered responses using the Llama 3.2 model.
- Simple and user-friendly interface built with Streamlit.
- Local AI inference using Ollama.
- Runs on a local machine without requiring a paid AI API.
- Easy to set up and extend with additional features.

- Technologies Used

- Python – Application logic.
- Streamlit – Web interface.
- Ollama – Local AI model runtime.
- Llama 3.2 – Language model.
- Visual Studio Code – Development environment.
- Git and GitHub – Version control and project hosting.

- Project Structure

AI-Personal-Assistant/
│
├── app.py
├── README.md
└── requirements.txt

- Installation and Setup

- Prerequisites

- Python installed on your computer.
- Ollama installed.
- Git installed (optional).

Step 1: Clone the Repository

git clone YOUR_REPOSITORY_URL
cd AI-Personal-Assistant

Step 2: Install Dependencies

python -m pip install streamlit ollama

Step 3: Download the AI Model

ollama pull llama3.2

Step 4: Run the Application

python -m streamlit run app.py

The application will open in your browser at the local address displayed in the terminal.
 
- How It Works

1. The user enters a question in the Streamlit interface.
2. The application sends the question to Ollama.
3. Ollama processes the input using the Llama 3.2 model.
4. The generated response is displayed to the user.

- Learning Outcomes

- Understanding how to integrate a local language model into a Python application.
- Building an interactive web application with Streamlit.
- Connecting Python code to Ollama.
- Learning the basics of AI chatbot development.
- Managing and documenting a software project with GitHub.

- Future Enhancements

- Chat history and conversational memory.
- User profile and personalized greetings.
- Email input and optional email-related features.
- Voice input and text-to-speech.
- Improved error handling and response formatting.

- Author

Sreelakshmi Nambiar

GitHub: "sreelakshminambiar1717" (https://github.com/sreelakshminambiar1717)
