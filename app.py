import streamlit as st
import ollama
import json
import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess
import re
import requests
import psutil
import platform


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# FILE NAMES
# =========================================================

MEMORY_FILE = "memory.json"
NOTES_FILE = "notes.json"
CHAT_HISTORY_FILE = "chat_history.json"


# =========================================================
# DEFAULT MEMORY
# =========================================================

DEFAULT_MEMORY = {
    "name": "",
    "course": "",
    "year": "",
    "skills": "",
    "location": ""
}


# =========================================================
# MEMORY
# =========================================================

def load_memory():

    if os.path.exists(MEMORY_FILE):

        try:
            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for key in DEFAULT_MEMORY:

                if key not in data:
                    data[key] = ""

            return data

        except Exception:
            pass

    return DEFAULT_MEMORY.copy()


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


memory = load_memory()


# =========================================================
# NOTES
# =========================================================

def load_notes():

    if os.path.exists(NOTES_FILE):

        try:
            with open(
                NOTES_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:
            pass

    return []


def save_notes(notes):

    with open(
        NOTES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            notes,
            file,
            indent=4,
            ensure_ascii=False
        )


notes = load_notes()


# =========================================================
# CHAT HISTORY
# =========================================================

def load_chat_history():

    if os.path.exists(CHAT_HISTORY_FILE):

        try:
            with open(
                CHAT_HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

        except Exception:
            pass

    return []


def save_chat_history(messages):

    with open(
        CHAT_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# VOICE INPUT
# =========================================================

def listen():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            st.info(
                "🎤 Listening... Speak now!"
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(
            audio
        )

        return text

    except sr.WaitTimeoutError:

        st.warning(
            "⏱️ No speech detected."
        )

        return ""

    except sr.UnknownValueError:

        st.warning(
            "❌ I couldn't understand you."
        )

        return ""

    except sr.RequestError:

        st.error(
            "🌐 Speech recognition requires internet."
        )

        return ""

    except Exception as e:

        st.error(
            f"🎤 Microphone error: {e}"
        )

        return ""


# =========================================================
# VOICE OUTPUT
# =========================================================

def speak(text):

    try:

        engine = pyttsx3.init()

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        st.error(
            f"🔊 Voice error: {e}"
        )


# =========================================================
# CALCULATOR
# =========================================================

def calculate_expression(command):

    expression = command.lower().strip()

    expression = expression.replace(
        "calculate",
        ""
    )

    expression = expression.replace(
        "the answer to",
        ""
    )

    expression = expression.replace(
        "multiplied by",
        "*"
    )

    expression = expression.replace(
        "multiply by",
        "*"
    )

    expression = expression.replace(
        "divided by",
        "/"
    )

    expression = expression.replace(
        "divide by",
        "/"
    )

    expression = expression.replace(
        "plus",
        "+"
    )

    expression = expression.replace(
        "minus",
        "-"
    )

    expression = expression.replace(
        "×",
        "*"
    )

    expression = re.sub(
        r"\s+x\s+",
        "*",
        expression
    )

    expression = expression.strip()

    if expression.endswith(
        ("+", "-", "*", "/")
    ):

        return (
            "🤔 Your calculation is incomplete."
        )

    if not expression:
        return None

    allowed = "0123456789+-*/().% "

    if not all(
        char in allowed
        for char in expression
    ):

        return None

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"🧮 The answer is {result}."

    except Exception:

        return "❌ I couldn't calculate that."


# =========================================================
# WEATHER
# =========================================================

def get_weather(city):

    try:

        url = (
            "https://wttr.in/"
            + city.replace(" ", "+")
            + "?format=j1"
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            return "❌ I couldn't get the weather."

        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]

        description = current[
            "weatherDesc"
        ][0]["value"]

        return (
            f"🌦️ Weather in {city.title()}\n\n"
            f"🌡️ Temperature: {temperature}°C\n"
            f"🤗 Feels like: {feels_like}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"☁️ Condition: {description}"
        )

    except Exception:

        return "❌ Weather service is unavailable."


# =========================================================
# SYSTEM INFORMATION
# =========================================================

def system_information():

    try:

        cpu = psutil.cpu_percent(
            interval=1
        )

        ram = psutil.virtual_memory()

        disk = psutil.disk_usage(
            os.path.abspath(os.sep)
        )

        return (
            "🖥️ System Information\n\n"
            f"💻 OS: {platform.system()}\n"
            f"⚙️ Processor: {platform.processor()}\n"
            f"🧠 CPU Usage: {cpu}%\n"
            f"💾 RAM Usage: {ram.percent}%\n"
            f"💿 Disk Usage: {disk.percent}%"
        )

    except Exception as e:

        return (
            f"❌ Could not get system information: {e}"
        )


# =========================================================
# OPEN FOLDER
# =========================================================

def open_folder(folder):

    try:

        path = os.path.expanduser(folder)

        if os.path.exists(path):

            os.startfile(path)

            return f"📂 Opening {path}"

        return f"❌ Folder not found: {path}"

    except Exception as e:

        return f"❌ Could not open folder: {e}"


# =========================================================
# NOTES
# =========================================================

def add_note(note_text):

    global notes

    timestamp = datetime.datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    notes.append(
        {
            "text": note_text,
            "time": timestamp
        }
    )

    save_notes(notes)

    return (
        f"📝 Note saved:\n\n{note_text}"
    )


def show_notes():

    if not notes:

        return "📝 You don't have any saved notes."

    result = "📝 Your Notes\n\n"

    for index, note in enumerate(
        notes,
        start=1
    ):

        result += (
            f"{index}. {note['text']}\n"
            f"   🕐 {note['time']}\n\n"
        )

    return result


# =========================================================
# GOOGLE SEARCH
# =========================================================

def google_search(query):

    if not query:

        return (
            "❌ Please tell me what you want to search."
        )

    url = (
        "https://www.google.com/search?q="
        + requests.utils.quote(query)
    )

    webbrowser.open(url)

    return f"🔎 Searching Google for: {query}"


# =========================================================
# COMMAND ROUTER
# =========================================================

def execute_command(command):

    command_lower = command.lower().strip()


    # GOOGLE
    if command_lower == "open google":

        webbrowser.open(
            "https://www.google.com"
        )

        return "🌐 Opening Google."


    # YOUTUBE
    if command_lower == "open youtube":

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "▶️ Opening YouTube."


    # GITHUB
    if command_lower == "open github":

        webbrowser.open(
            "https://github.com"
        )

        return "💻 Opening GitHub."


    # LINKEDIN
    if command_lower == "open linkedin":

        webbrowser.open(
            "https://www.linkedin.com"
        )

        return "💼 Opening LinkedIn."


    # VS CODE
    if (
        "open vs code" in command_lower
        or
        "open visual studio code" in command_lower
    ):

        try:

            subprocess.Popen(
                "code",
                shell=True
            )

            return "💻 Opening Visual Studio Code."

        except Exception:

            return (
                "❌ I couldn't open Visual Studio Code."
            )


    # TIME
    if (
        "what time" in command_lower
        or
        "current time" in command_lower
        or
        "tell me the time" in command_lower
    ):

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"🕐 The current time is {current_time}."
        )


    # DATE
    if (
        "what date" in command_lower
        or
        "today's date" in command_lower
        or
        "current date" in command_lower
        or
        "today date" in command_lower
    ):

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        return (
            f"📅 Today's date is {current_date}."
        )


    # SYSTEM INFORMATION
    if (
        "system information" in command_lower
        or
        "system info" in command_lower
        or
        "computer information" in command_lower
        or
        "computer specs" in command_lower
        or
        "system status" in command_lower
    ):

        return system_information()


    # WEATHER IN CITY
    if "weather in" in command_lower:

        parts = command_lower.split(
            "weather in",
            1
        )

        if len(parts) > 1:

            city = parts[1].strip()

            if city:

                return get_weather(city)

        return "🌦️ Please tell me the city."


    # WEATHER USING SAVED LOCATION
    if command_lower == "weather":

        if memory["location"]:

            return get_weather(
                memory["location"]
            )

        return (
            "🌦️ Tell me your city, "
            "for example: weather in Pune."
        )


    # GOOGLE SEARCH
    if (
        command_lower.startswith("search ")
        or
        command_lower.startswith("search for ")
        or
        command_lower.startswith("google ")
    ):

        if command_lower.startswith(
            "search for "
        ):

            query = command_lower[
                len("search for "):
            ]

        elif command_lower.startswith(
            "search "
        ):

            query = command_lower[
                len("search "):
            ]

        else:

            query = command_lower[
                len("google "):
            ]

        return google_search(
            query.strip()
        )


    # NOTES
    prefixes = [
        "take a note ",
        "save a note ",
        "remember this "
    ]

    for prefix in prefixes:

        if command_lower.startswith(prefix):

            note = command[
                len(prefix):
            ].strip()

            if note:

                return add_note(note)

            return (
                "📝 What would you like me to save?"
            )


    # SHOW NOTES
    if (
        command_lower == "show my notes"
        or
        command_lower == "show notes"
        or
        command_lower == "my notes"
    ):

        return show_notes()


    # DOWNLOADS
    if (
        "open downloads" in command_lower
        or
        "open download folder" in command_lower
    ):

        return open_folder(
            "~/Downloads"
        )


    # DOCUMENTS
    if (
        "open documents" in command_lower
        or
        "open documents folder" in command_lower
    ):

        return open_folder(
            "~/Documents"
        )


    # DESKTOP
    if "open desktop" in command_lower:

        return open_folder(
            "~/Desktop"
        )


    # CALCULATOR
    calculation_keywords = [
        "calculate ",
        "plus ",
        "minus ",
        "multiplied by ",
        "multiply by ",
        "divided by ",
        "divide by "
    ]

    is_calculation = any(
        keyword in command_lower
        for keyword in calculation_keywords
    )

    if re.search(
        r"\d+\s*[\+\-\*/%x×]\s*\d+",
        command_lower
    ):

        is_calculation = True

    if is_calculation:

        result = calculate_expression(
            command_lower
        )

        if result:

            return result

        return (
            "❌ I couldn't understand the calculation."
        )


    return None


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = (
        load_chat_history()
    )


if "voice_input" not in st.session_state:

    st.session_state.voice_input = ""


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "🤖 AI Personal Assistant"
)

st.sidebar.caption(
    "Version 2.0"
)


voice_mode = st.sidebar.toggle(
    "🎤 Voice Mode",
    value=False
)


st.sidebar.divider()


# =========================================================
# MEMORY DISPLAY
# =========================================================

st.sidebar.header(
    "🧠 My Memory"
)

st.sidebar.write(
    f"👤 **Name:** "
    f"{memory['name'] or 'Not saved'}"
)

st.sidebar.write(
    f"🎓 **Course:** "
    f"{memory['course'] or 'Not saved'}"
)

st.sidebar.write(
    f"📚 **Year:** "
    f"{memory['year'] or 'Not saved'}"
)

st.sidebar.write(
    f"💻 **Skills:** "
    f"{memory['skills'] or 'Not saved'}"
)

st.sidebar.write(
    f"📍 **Location:** "
    f"{memory['location'] or 'Not saved'}"
)


st.sidebar.divider()


# =========================================================
# QUICK ACTIONS
# =========================================================

st.sidebar.header(
    "⚡ Quick Actions"
)


if st.sidebar.button(
    "🌐 Open Google"
):

    webbrowser.open(
        "https://www.google.com"
    )


if st.sidebar.button(
    "▶️ Open YouTube"
):

    webbrowser.open(
        "https://www.youtube.com"
    )


if st.sidebar.button(
    "💻 Open GitHub"
):

    webbrowser.open(
        "https://github.com"
    )


# =========================================================
# CLEAR MEMORY
# =========================================================

if st.sidebar.button(
    "🧹 Clear Memory"
):

    memory = DEFAULT_MEMORY.copy()

    save_memory(
        memory
    )

    st.sidebar.success(
        "Memory cleared!"
    )

    st.rerun()


# =========================================================
# CLEAR CHAT
# =========================================================

if st.sidebar.button(
    "🗑️ Clear Chat"
):

    st.session_state.messages = []

    save_chat_history([])

    st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

st.title(
    "🤖 AI Personal Assistant"
)

st.write(
    "Your intelligent personal assistant "
    "powered by Python + Ollama."
)


# =========================================================
# DASHBOARD
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🧠 Memory",
        "ON"
    )


with col2:

    st.metric(
        "🎤 Voice",
        "ON" if voice_mode else "OFF"
    )


with col3:

    st.metric(
        "🤖 AI Model",
        "Llama 3.2"
    )


with col4:

    st.metric(
        "⚡ Running",
        "Local"
    )


st.divider()


# =========================================================
# DISPLAY OLD CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# =========================================================
# VOICE MODE
# =========================================================

if voice_mode:

    st.info(
        "🎤 Voice Mode is ON"
    )


    if st.button(
        "🎙️ Talk to Assistant",
        use_container_width=True
    ):

        spoken_text = listen()

        if spoken_text:

            st.session_state.voice_input = (
                spoken_text
            )

            st.rerun()


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Ask me anything..."
)


# =========================================================
# VOICE MESSAGE
# =========================================================

if st.session_state.voice_input:

    user_message = (
        st.session_state.voice_input
    )

    st.session_state.voice_input = ""


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_message:

    # -----------------------------------------------------
    # SHOW USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.write(
            user_message
        )


    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    save_chat_history(
        st.session_state.messages
    )


    text = user_message.lower().strip()


    # =====================================================
    # MEMORY - NAME
    # =====================================================

    name_match = re.search(
        r"\bmy name is\s+(.+)",
        user_message,
        re.IGNORECASE
    )

    if name_match:

        name = name_match.group(1).strip()

        if name:

            memory["name"] = name.title()

            save_memory(memory)


    # =====================================================
    # MEMORY - COURSE
    # =====================================================

    course_match = re.search(
        r"\bi am studying\s+(.+)",
        user_message,
        re.IGNORECASE
    )


    if not course_match:

        course_match = re.search(
            r"\bi study\s+(.+)",
            user_message,
            re.IGNORECASE
        )


    # Handle:
    # "I am a BSc 3rd year Computer Science student"

    if not course_match:

        combined_match = re.search(
            r"\bi am (?:a|an)\s+(.+?)\s+(?:student|student\.?)$",
            user_message,
            re.IGNORECASE
        )

        if combined_match:

            combined_text = (
                combined_match.group(1).strip()
            )

            # Extract course
            if "computer science" in combined_text.lower():

                memory["course"] = (
                    "BSc Computer Science"
                )

            elif "bsc" in combined_text.lower():

                memory["course"] = "BSc"

            # Extract year
            year_match = re.search(
                r"(1st|2nd|3rd|4th|\d+(?:st|nd|rd|th))\s*year",
                combined_text,
                re.IGNORECASE
            )

            if year_match:

                memory["year"] = (
                    year_match.group(1).title()
                    + " Year"
                )

            save_memory(memory)


    if course_match:

        course = course_match.group(1).strip()

        if course:

            memory["course"] = course.title()

            save_memory(memory)


    # =====================================================
    # MEMORY - YEAR
    # =====================================================

    year_match = re.search(
        r"\b(?:i am|i'm)\s+(?:a\s+)?"
        r"(1st|2nd|3rd|4th|\d+(?:st|nd|rd|th))"
        r"\s*year\b",
        user_message,
        re.IGNORECASE
    )


    if year_match:

        year = year_match.group(1).strip()

        memory["year"] = (
            year.title()
            + " Year"
        )

        save_memory(memory)


    # =====================================================
    # MEMORY - SKILLS
    # =====================================================

    skills_match = re.search(
        r"\bmy skills are\s+(.+)",
        user_message,
        re.IGNORECASE
    )


    if skills_match:

        skills = skills_match.group(1).strip()

        if skills:

            memory["skills"] = skills

            save_memory(memory)


    # =====================================================
    # MEMORY - LOCATION
    # =====================================================

    location_match = re.search(
        r"\bi live in\s+(.+)",
        user_message,
        re.IGNORECASE
    )


    if location_match:

        location = location_match.group(1).strip()

        if location:

            memory["location"] = location.title()

            save_memory(memory)


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_message = f"""
You are an intelligent AI Personal Assistant.

You run locally using Ollama and Llama 3.2.

USER INFORMATION:

Name: {memory["name"]}
Course: {memory["course"]}
Year: {memory["year"]}
Skills: {memory["skills"]}
Location: {memory["location"]}

IMPORTANT:

If the user asks:
"What am I studying?"
use the Course information.

If the user asks:
"What year am I in?"
use the Year information.

If the user asks:
"What are my skills?"
use the Skills information.

If the user asks:
"What is my name?"
use the Name information.

If the user asks:
"Tell me about myself"
summarize the stored information.

Never invent personal information.

Be friendly, concise and helpful.
"""


    # =====================================================
    # PREPARE MESSAGES FOR OLLAMA
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": system_message
        }
    ]


    messages.extend(
        st.session_state.messages
    )


    # =====================================================
    # COMMAND ROUTER
    # =====================================================

    command_response = execute_command(
        user_message
    )


    # =====================================================
    # GENERATE ANSWER
    # =====================================================

    if command_response:

        answer = command_response

    else:

        try:

            response = ollama.chat(
                model="llama3.2",
                messages=messages
            )

            answer = response[
                "message"
            ][
                "content"
            ]

        except Exception as e:

            answer = (
                "❌ I couldn't connect to Ollama.\n\n"
                f"Error: {e}"
            )


    # =====================================================
    # SHOW ASSISTANT ANSWER
    # =====================================================

    with st.chat_message(
        "assistant"
    ):

        st.write(
            answer
        )


    # =====================================================
    # SAVE ASSISTANT ANSWER
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    save_chat_history(
        st.session_state.messages
    )


    # =====================================================
    # VOICE OUTPUT
    # =====================================================

    if voice_mode:

        speak(
            answer
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🤖 AI Personal Assistant | "
    "Python + Streamlit + Ollama + Llama 3.2"
)