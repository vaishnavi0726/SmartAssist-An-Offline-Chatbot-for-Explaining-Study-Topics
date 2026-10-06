# SmartAssist – Intelligent Chatbot Application

SmartAssist is a small, fully offline Flask web application with built-in student-friendly explanations for common study topics and college project ideas. It does not require an API key or send messages to an external service. Conversations are saved in SQLite.

## Features

- Responsive chat page with message timestamps, typing indicator, and Enter-to-send
- Built-in explanations for common topics across computing, science, mathematics, and civics
- College project suggestions
- No API key, paid service, or internet connection required for chat
- Conversation history stored in a local SQLite database
- Clear-chat button and friendly validation/error messages

## Technologies

Python 3, Flask, HTML5, CSS3, JavaScript, and SQLite.

## Project structure

```text
SmartAssist_Chatbot/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── chatbot/
│   ├── __init__.py
│   ├── chatbot_engine.py
│   └── responses.py
├── database/
│   └── chatbot.db       # Created automatically when the app starts
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Installation

Open a terminal in the project folder and create a virtual environment:

```powershell
python -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, either allow scripts for this terminal with
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or use Command Prompt:

```bat
venv\Scripts\activate.bat
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Topic library

SmartAssist works fully offline and does not need an API key. The built-in explanations cover photosynthesis, machine learning, artificial intelligence, Python, the internet, gravity, climate change, DNA, cells, blockchain, databases, SQL, algorithms, binary numbers, cloud computing, cybersecurity, neural networks, renewable energy, democracy, calculus, and electricity. If a topic is not in that built-in list, the chatbot shows the supported topics instead of pretending it knows the answer. More explanations can be added in `chatbot/responses.py`.

## Run the application

From the project folder, with the virtual environment active:

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The database folder and table are created automatically the first time the application starts.

## Test the chatbot

1. Select one of the topic suggestions or type a question such as `Explain photosynthesis` or `What is machine learning?`.
2. Ask `Give me college project ideas` for built-in project suggestions.
3. Send a message with the **Send** button or press **Enter**. No API key or internet connection is required.
4. Ask about an unsupported topic to see the list of topics currently built in.
5. Refresh the page to check that the conversation is restored from SQLite.
6. Select **Clear chat** to remove the saved conversation.
7. Leave the message blank to see the form's required-field validation.

The JSON chat endpoint accepts `POST /chat` with `{"message":"Hello"}`. Send `DELETE /chat` to clear the stored conversation. `GET /history` is used by the page to restore recent messages.

## Common errors and fixes

- **`ModuleNotFoundError`**: Activate the virtual environment and run `python -m pip install -r requirements.txt`.
- **A topic is not recognized**: Check the built-in topic list in `README.md` or add an explanation and aliases in `chatbot/responses.py`. The app intentionally works offline and does not call an AI service.
- **Address already in use**: Another app is using port 5000. Close that process or change the port in the `app.run` line in `app.py`.
- **PowerShell will not activate the virtual environment**: Use the process-scoped execution policy command shown above, or activate from Command Prompt.
- **Database cannot be written**: Make sure the project directory is writable and that no other program has locked `database/chatbot.db`.
