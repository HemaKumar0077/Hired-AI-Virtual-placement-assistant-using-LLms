# HiredAI

# Resume Verification

This project is designed to verify resumes using a Streamlit application.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/resume_verification.git
    cd resume_verification
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Register for a GROQ API key and add it to the `.env` file:
    - Visit [GROQ API registration](https://console.groq.com/docs/quickstart) to get your API key.
    - Add the API key to the `.env` file:
        ```
        GROQ_API_KEY=your_api_key_here
        ```

## Running the Application

1. Ensure you are in the project directory and the virtual environment is activated.

2. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

3. Open your web browser and go to `http://localhost:8501` to view the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

> **Note:** If you encounter any missing libraries, you can install them individually using `pip install <library-name>`.
