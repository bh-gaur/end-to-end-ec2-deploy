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



# Requirements for Deployment

This document outlines the prerequisites, secrets, pipeline stages, and infrastructure requirements for deploying the **Streamlit To-Do List Application** to AWS EC2 using GitHub Actions and Docker Hub.

---

## 🔐 1. Required GitHub Secrets

To allow GitHub Actions to build and push the container image to Docker Hub and ssh to the ec2 server, configure the following repository secrets under **Settings > Secrets and variables > Actions**:

| Secret Name | Description | Example |
| :--- | :--- | :--- |
| `DOCKER_USERNAME` | Your Docker Hub account username. | `johndoe` |
| `DOCKER_PASSWORD` | Docker Hub Access Token or Password. | `dckr_pat_xxx` |
| `EC2_HOST` | Your EC2 instance IP address. | `[IP_ADDRESS]` |
| `EC2_USER` | Your EC2 instance username. | `ubuntu` |
| `EC2_SSH_KEY` | Your EC2 instance SSH private key. | `-----BEGIN RSA PRIVATE KEY-----` |

---

## 🛠️ 2. CI/CD Pipeline Architecture

The deployment pipeline is defined in [deploy.yml](file:///Users/vishnu/learning/b_github/end-to-end-ec2-deploy/.github/workflows/deploy.yml) and consists of the following automated stages:

```mermaid
graph TD
    A[Push to master branch / Manual Trigger] --> B[Job: simple-test]
    B -->|Lint & Type Check| C[Job: Testing-complete]
    C --> D[Job: Build-scan-and-push-image]
    D --> E[Login to Docker Hub]
    E --> F[Build Docker Image]
    F --> G[Run Trivy Security Scan]
    G -->|Passes Critical/High Check| H[Push Image to Docker Hub]
    H --> I[Job: deploy]
    I --> J[SSH into EC2]
    J --> K[Pull Docker Image]
    K --> L[Run Docker Compose]
```

### Pipeline Jobs Details

1. **`simple-test`**:
   - Runs linting and formatting via `ruff`.
   - Performs static type checking via `mypy`.
   - Tests across Python versions `3.10`, `3.11`, and `3.12`.

2. **`Testing-complete`**:
   - Verification gate confirming all quality and lint checks passed.

3. **`Build-scan-and-push-image`**:
   - **Docker Login**: Authenticates against Docker Hub using secrets.
   - **Image Build**: Builds `todo-streamlit-app:${{ github.sha }}` locally on the runner with `TestEnv=Dev`.
   - **Trivy Vulnerability Scan**: Scans the built container for `CRITICAL` or `HIGH` vulnerabilities. Fails the workflow if any are detected.
   - **Push to Registry**: Pushes the verified image directly to Docker Hub.

---

## 🚀 3. EC2 Target Environment Setup

To run the Streamlit container on an AWS EC2 instance:

1. **EC2 Prerequisites**:
   - Ubuntu 22.04 LTS or 24.04 LTS instance.
   - Security Group rule allowing inbound traffic on port `8501` (or port `80`/`443` if using a reverse proxy like Nginx).

2. **Server Package Installation**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io
   sudo systemctl enable --now docker
   ```

3. **Running the Application**:
   ```bash
   # Pull the latest image built by GitHub Actions
   docker pull <YOUR_DOCKER_USERNAME>/todo-streamlit-app:<IMAGE_TAG>

   # Run container in detached mode exposing Streamlit on port 8501
   docker run -d \
     --name streamlit-todo \
     -p 8501:8501 \
     -v $(pwd)/tasks.csv:/app/tasks.csv \
     <YOUR_DOCKER_USERNAME>/todo-streamlit-app:<IMAGE_TAG>
   ```

---

## 📋 4. Application Dependencies

The application relies on the following key dependencies configured in `requirements.txt`:

- **Streamlit (`>=1.38.0`)**: Web UI framework.
- **Setuptools (`>=83.0.0`)**: Setuptools framework providing updated vendored packages.
- **Jaraco.context (`>=6.1.0`) & Wheel (`>=0.46.2`)**: Explicitly pinned to ensure zero container security vulnerabilities.
