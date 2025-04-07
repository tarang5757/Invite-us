## Project Overview

The **Real-Time Collaborative Code Editor** is a web-based platform that enables multiple users to collaboratively write, edit, and execute code in real-time. This project leverages the power of **React.js**, **Next.js**, and **Flask** to deliver a seamless and interactive coding environment, perfect for pair programming, coding interviews, team debugging, and hackathons.

With its real-time collaboration capabilities, users can work on the same file simultaneously, with changes reflected instantly across all users. The platform also supports multi-user rooms, allowing for a more organized collaborative experience.

## Features

### ✅ Real-Time Collaboration

- Users can write, edit, and execute code in real time, ensuring that all participants are instantly aware of any changes made to the code.
- Each participant sees the changes as soon as they are made, enhancing collaboration and reducing misunderstandings during coding sessions.

### ✅ Multi-User Rooms

- Users can create and join unique rooms, which serve as isolated environments for coding sessions.
- Each room allows multiple users to collaborate on the same project, making it ideal for team projects, interviews, or online coding workshops.

### ✅ WebSocket Integration

- Powered by **Flask-SocketIO**, the platform ensures that all updates, code changes, and messages are transmitted in real-time to all connected users.
- WebSocket-based communication ensures low latency and a responsive experience.

### ✅ Code Execution Support

- The platform supports the execution of code in multiple programming languages, allowing users to compile and run their code directly within the editor.
- This feature allows users to test and debug their code without leaving the platform.

### ✅ Syntax Highlighting

- **CodeMirror**, an embedded text editor, is used to provide syntax-aware editing, enhancing code readability.
- The editor automatically highlights code based on its language, making it easier for users to spot errors and understand the code structure.

### ✅ File Management

- Users can create, delete, and rename files directly within the platform, allowing for flexible project management.
- The file management system makes it easy to organize coding sessions and keep track of different project files.

## Tech Stack

### Frontend

- **React.js**: Used to build a dynamic and responsive user interface for the code editor.
- **Next.js**: Provides server-side rendering and improved performance for the frontend, along with easy routing for different components.
- **CodeMirror**: A powerful text editor that supports syntax highlighting for multiple programming languages and integrates smoothly into the platform.

### Backend

- **Flask**: The backend framework responsible for handling user requests, managing sessions, and serving the API.
- **Flask-SocketIO**: A Flask extension used to enable WebSocket-based real-time communication, ensuring that updates are reflected instantly across all users in a session.

### Code Execution

- The backend includes APIs for running code in different languages, providing a seamless experience for users to test their code within the platform.

## Setup Instructions

### Prerequisites

- **Python 3.x**: Ensure you have Python 3.x installed on your machine.
- **Node.js**: Required for running the frontend.
- **npm** or **yarn**: Package managers for the frontend dependencies.

### Installation

1. **Clone the repository:**
   ```bash
   https://github.com/tarang5757/Invite-us.git
   cd Invite-us
   ```

Setup the backend:

2. **Navigate to the backend directory:**
   `cd backend`

- **Install the required Python dependencies:**

```
pip install -r requirements.txt
Run the Flask server:

python app.py
```

**Setup the frontend:**

Navigate to the frontend directory:

````
cd frontend
```bash
- **Install the required Node.js dependencies**:
```bash
npm install
````

- **Start the React application:**

```bash
npm run dev
```

- **Open your browser and navigate to http://localhost:3000 to start using the collaborative code editor.**
