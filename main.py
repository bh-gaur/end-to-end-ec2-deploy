# pyrefly: ignore [missing-import]
import streamlit as st
import csv

# Define the path to the CSV file
CSV_FILE = "tasks.csv"


def load_tasks():
    """
    Load the tasks from the CSV file.
    """
    try:
        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            task_list = []
            for row in reader:
                if row:
                    task_name = row[0]
                    # Default status is 'Pending' if not specified
                    status = row[1] if len(row) > 1 else "Pending"
                    task_list.append({"task": task_name, "status": status})
            return task_list
    except FileNotFoundError:
        return []


def save_tasks(task_list):
    """
    Save the tasks to the CSV file.
    """
    with open(CSV_FILE, "w", newline="") as f:
        f.truncate(0)
        writer = csv.writer(f)
        writer.writerows([[t["task"], t["status"]] for t in task_list])


# Callbacks for managing state cleanly without manual reruns
def toggle_task(idx):
    tasks = load_tasks()
    if idx < len(tasks):
        current_status = tasks[idx]["status"]
        tasks[idx]["status"] = "Completed" if current_status == "Pending" else "Pending"
        save_tasks(tasks)


def delete_task(idx):
    tasks = load_tasks()
    if idx < len(tasks):
        tasks.pop(idx)
        save_tasks(tasks)


def add_task():
    if "new_task_input" in st.session_state:
        task_text = st.session_state.new_task_input.strip()
        if task_text != "":
            tasks = load_tasks()
            task_count = sum(1 for t in tasks if t["task"] == task_text)
            if task_count >= 4:
                st.session_state.add_task_error = f"Cannot add '{task_text}'. You cannot have the same task more than 4 times."
            else:
                tasks.append({"task": task_text, "status": "Pending"})
                save_tasks(tasks)
                if "add_task_error" in st.session_state:
                    del st.session_state.add_task_error


def clear_tasks():
    save_tasks([])


# Define the main function
def main():
    # Set page configuration as the first Streamlit command
    st.set_page_config(page_title="To-Do List", page_icon="📝", layout="centered")

    # Set custom premium glassmorphic styling
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.pexels.com/photos/2387793/pexels-photo-2387793.jpeg?cs=srgb&dl=pexels-adrien-olichon-2387793.jpg&fm=jpg");
            background-attachment: fixed;
            background-size: cover;
        }
        /* Style text for better readability on dark background */
        h1, h2, h3, p, span, label, div {
            color: #ffffff !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
        }
        /* Style text input */
        input {
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }
        /* Style checked items style */
        .stMarkdown p del {
            color: rgba(255, 255, 255, 0.5) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Set the title of the web app
    st.title("📝 Modern To-Do List")

    # Load the tasks from the CSV file
    task_list = load_tasks()

    # Progress bar and stats
    total_tasks = len(task_list)
    if total_tasks > 0:
        completed_tasks = sum(1 for t in task_list if t["status"] == "Completed")
        st.subheader("Progress Tracker")
        col_progress, col_text = st.columns([0.85, 0.15])
        col_progress.progress(completed_tasks / total_tasks)
        col_text.write(f"**{completed_tasks}/{total_tasks}**")

    # Display current tasks
    st.subheader("Current Tasks")
    if len(task_list) == 0:
        st.info("No tasks added yet. Add a task below to get started!")
    else:
        for i, task_item in enumerate(task_list):
            cols = st.columns([0.08, 0.77, 0.15])

            # Checkbox for completion
            is_completed = task_item["status"] == "Completed"
            cols[0].checkbox(
                "Complete task",
                value=is_completed,
                key=f"check_{i}",
                label_visibility="collapsed",
                on_change=toggle_task,
                args=(i,),
            )

            # Task text rendering
            task_name = task_item["task"]
            if is_completed:
                cols[1].markdown(f"~~{task_name}~~")
            else:
                cols[1].markdown(f"**{task_name}**")

            # Handle task delete button via callback
            cols[2].button("🗑️", key=f"delete_{i}", on_click=delete_task, args=(i,))

    # Display errors if any from callback
    if "add_task_error" in st.session_state:
        st.error(st.session_state.add_task_error)
        # Clear the error from state after showing it once so it goes away if user corrects it
        del st.session_state.add_task_error

    st.write("")
    st.subheader("Add New Task")
    # Add a form to input new tasks (automatically clears input on submit)
    with st.form(key="add_task_form", clear_on_submit=True):
        col_input, col_submit = st.columns([0.8, 0.2])
        col_input.text_input(
            "Add a new task:",
            placeholder="Type your task here...",
            label_visibility="collapsed",
            key="new_task_input",
        )
        st.form_submit_button("Add Task", on_click=add_task)

    # Add a button to clear the task list
    if len(task_list) > 0:
        st.write("---")
        st.button("🧹 Clear all tasks", on_click=clear_tasks)


# Run the app
if __name__ == "__main__":
    main()
