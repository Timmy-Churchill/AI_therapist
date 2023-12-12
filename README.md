# ChatBot with Emotion Pentagon Chart

This project integrates a ChatBot , allowing users to interact with a basic chat interface while visualizing the emotional content of their messages in a radar chart.

## Setup

### Prerequisites

- Python (version X.X or above)
- Flask
- OpenAI GPT-3 API key
- Node.js
- NPM

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project root and add your OpenAI GPT-3 API key:**

    ```
    OPENAI_API_KEY=your-api-key
    ```

    **Note:** Ensure that the `.env` file is added to the `.gitignore` file to avoid exposing sensitive information.

### Usage

1. **Start the Flask backend:**

    ```bash
    python app.py
    ```

    The backend will run on `http://localhost:8080`.

2. **Open a new terminal and start the frontend development server:**

    ```bash
    npm start
    ```

    The frontend will be available at `http://localhost:8080`.

3. **Open your web browser and navigate to `http://localhost:8080` to access the ChatBot interface**

**Important:**

- The `indexTEST.html` file serves as a testing interface for the backend logic.
- The `index.html` file is the working frontend that communicates with the backend.
- Make sure to adjust the 'Frontend path' variable in app.py according to which one you want to see

## Contributing

Feel free to contribute to this project by submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
