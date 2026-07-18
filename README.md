# 📝 Modern Streamlit To-Do List Application

A polished, premium To-Do List web application built using **Streamlit** and **Python**. The app features a stunning glassmorphic UI, real-time persistence using a CSV backend, clean event-driven state management, progress tracking, and validation rules.

---

## ✨ Features

- **Premium UI Design**: A glassmorphic card interface featuring custom CSS styling and background imagery with high text readability.
- **Task Progress Tracker**: A visual progress bar updating in real-time as tasks are added, completed, or removed.
- **CSV Data Persistence**: Keeps your tasks saved automatically in `tasks.csv` across restarts, storing both the task description and status (`Pending` / `Completed`).
- **Callback-Driven Architecture**: Uses native Streamlit widget callbacks (`on_change` and `on_click`) to handle user actions gracefully, avoiding uncaught `RerunException` tracebacks.
- **Automatic Form Clearing**: Utilizes Streamlit forms with `clear_on_submit` to reset the input box instantly upon adding a task.
- **Duplicate Prevention Limit**: Restricts adding the same task name more than 4 times to prevent list bloat.
- **Action Controls**: Delete individual tasks with one click or clear the entire task list.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.8+** installed on your system.

### Installation

1. Navigate to the project directory:
   ```bash
   cd end-to-end-ec2-deploy
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Start the Streamlit local development server:
```bash
streamlit run main.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 📁 File Structure

- `main.py`: The entry point containing application layout, custom CSS, state callbacks, and utility functions.
- `requirements.txt`: Project dependencies (Streamlit package).
- `tasks.csv`: Comma-separated file storing your task list dynamically.
