[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/riYMmZC8)

# CKD Risk Prediction and Information Web Application
 Deployment on Render - https://group-project-2024c-isys2101-3395-team-8.onrender.com
## Authors

Phyu Phyu Shinn Thant (Zyra) - s4022136
Bui Quoc Huy (Huy) - s3979446
Tak Minwoo (Minwoo) – s3818058

## License

This project is not currently distributed under an open-source license. All rights reserved.

## Overview

This web application is designed to enhance public awareness and facilitate potential early detection of severe Chronic Kidney Disease (CKD). It provides users with three key functionalities:

- **CKD Risk Prediction:** Users can input lifestyle and health information to receive a predicted likelihood of developing severe CKD based on a machine learning model. The results are presented with data visualizations to aid understanding.
- **AI-Powered Chatbot:** An interactive chatbot, powered by the **Mistral-7B-Instruct-v0.3** model from Hugging Face, provides users with evidence-based information and resources related to CKD management and prevention. It maintains a short conversational history for context.
- **Recommendations and Treatment Information:** A dedicated page offers detailed guidance, including FAQs, on preventing CKD and managing its progression through various treatment options, grounded in certified medical research.

## Technologies Used

- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn
- **Natural Language Processing:** Hugging Face Transformers, **Mistral-7B-Instruct-v0.3** model
- **Data Visualization (Backend):** Pandas, NumPy (for data handling), potentially Matplotlib/Seaborn (for generating visualization data)
- **Deployment:** (Specify your deployment platform if applicable, e.g., Heroku, AWS, Render)

## Setup and Installation

To run this application locally, please follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/RMIT-Vietnam-Teaching/group-project-2024c-isys2101-3395-team-8-renalyze.git
    cd group-project-2024c-isys2101-3395-team-8-renalyze
    ```

2.  **Install Dependencies:**
    Ensure you have Python installed on your system. Then, install the required Python libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Hugging Face Access and Environment Variables:**

    - **Obtain Your Hugging Face Access Token:**
      You will need a Hugging Face Access Token to interact with the models. If you don't have one, you can create one in your Hugging Face account settings ([https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)).

    - **Access the Mistral-7B-Instruct-v0.3 Model:**
      The AI-powered chatbot utilizes the **Mistral-7B-Instruct-v0.3** model hosted on Hugging Face. After you have created a token, you need to visit the model page: [mistralai/Mistral-7B-Instruct-v0.3 · Hugging Face](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) and follow the instructions on the page to request access to the model if required.

    - **Create `.env` File:**
      Create a `.env` file in the root directory of the project and store your access token there:

      ```
      HUGGINGFACE_ACCESS_TOKEN=your_huggingface_access_token
      ```

      Replace `your_huggingface_access_token` with the actual token you obtained from Hugging Face.

    **Important Security Note:** The `.env` file should **never** be committed to your Git repository. Ensure it is added to your `.gitignore` file to prevent accidental exposure of your access token.

4.  **Running the Application:**
    Navigate to the project directory in your terminal and run the Flask application:

    ```bash
    python app.py
    ```

    This will typically start the Flask development server. You should see an output indicating the server address (usually `http://127.0.0.1:5000/`). Open this address in your web browser to access the application.

## Environment Variables

The following environment variables need to be configured in the `.env` file:

- `HUGGINGFACE_ACCESS_TOKEN`: Your personal access token from Hugging Face. This is required to access and utilize the **Mistral-7B-Instruct-v0.3** model for the AI-powered chatbot. You can obtain this token from your Hugging Face account settings after requesting access to the model on its page.

## Requirements

The `requirements.txt` file lists all the necessary Python libraries and their versions required to run the backend of this application. Ensure you install these dependencies using `pip install -r requirements.txt` before running the application. Key dependencies include:

- Flask: A micro web framework for Python.
- transformers: The Hugging Face library for working with transformer models, including **Mistral-7B-Instruct-v0.3**.
- scikit-learn: A machine learning library for Python (used for the CKD prediction model).
- pandas: A data analysis and manipulation library.
- numpy: A library for numerical computing.
- python-dotenv: For loading environment variables from the `.env` file.
- (Potentially) Matplotlib and/or Seaborn: For generating data visualizations (if the visualization logic is handled in the backend).

## Usage

Once the application is running in your web browser, you can:

- Navigate to the prediction module to input your health and lifestyle information and receive a CKD risk assessment.
- Interact with the AI-powered chatbot by typing your questions related to CKD.
- Browse the recommendations and treatment information page to learn more about preventing and managing CKD.
