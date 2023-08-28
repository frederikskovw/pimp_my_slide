**Pimp My Slide README**

**I. Downloading and Extracting the Project**

1. Navigate to the Pimp My Slide project on GitHub: [Pimp My Slide GitHub Repo](https://github.com/frederikskovw/pimp_my_slide/tree/local).
2. Ensure you are on the "local" branch. If not, select it from the branch dropdown menu.
3. On the top right, find the green button labeled Code and click on it.
4. From the dropdown menu, select Download ZIP.
5. Save the ZIP file to your computer, preferably on the Desktop for easy access.
6. Go to where you saved the ZIP file.
7. Right-click on the Pimp My Slide.zip file.
8. Choose 'Extract All...' or an equivalent option based on your operating system.
9. A folder named Pimp My Slide will appear. This is referred to as the "root directory" of the app.

**II. Setting Up the Application**

Ensure you have the following prerequisites installed:
- Python: A popular programming language. Used for the backend of Pimp My Slide.
- Node.js: A JavaScript runtime built on Chrome's V8 JavaScript engine. Required to run the frontend.
- pip: A package installer for Python. Helps in installing necessary Python libraries.
- npm: Node Package Manager. Used to manage and install frontend dependencies.
Follow the setup instructions based on your operating system:

**III. Running the Application**

**III.A For macOS:**
Currently only supported directly from IDE
1. Setup
- setup backend: cd backend > pip install -r requirements
- setup frontend: cd frontend > npm install
2. Run
- start backend: python backend\app\main.py
- start frontend: cd frontend > npm run serve

**III.B For Windows systems:**
1. Setup (only need to do this once, after download): Double-click _app_setup.bat_ file in the root directory of app
2. Run
- Double-click _start_backend.bat_
- Double-click _start_frontend.bat_ > go to url _localhost:8080_ in your default webbrowser

**IV. Additional Information**

Ports: The backend uses port 5000 and the frontend uses port 8080 by default. Ensure these ports are available on your computer.
