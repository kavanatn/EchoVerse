# 🎵 EchoVerse

**Turn Your Words Into Immersive Audio**

EchoVerse is an AI-powered audiobook generator that transforms text and documents into expressive, tone-adapted speech. Leveraging **IBM Watsonx** for text enhancement and **IBM Cloud Text to Speech** for lifelike audio, EchoVerse allows you to create immersive listening experiences with various voices and emotional tones.

## ✨ Features

- **📝 Multi-Input Support**: Type text directly or upload PDF, TXT, and DOCX files.
- **🎭 Expressive Voices**: Choose from a variety of US, British, and Australian voices, including expressive options that convey emotions.
- **🎯 Tone Adaptation**: Select from tones like Neutral, Suspenseful, Inspiring, Professional, Casual, and Dramatic to match your content.
- **🤖 AI Enhancement**: Uses IBM Watsonx (Granite model) to rewrite and adapt text for the selected tone before conversion.
- **🎧 Interactive Player**: Listen to the generated audio directly within the app.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI/LLM**: IBM Watsonx (`ibm/granite-3-8b-instruct`)
- **Text to Speech**: IBM Cloud Watson TtS
- **Language**: Python

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- An IBM Cloud account with:
  - **Watson Machine Learning** (for Watsonx)
  - **Text to Speech** service

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/EchoVerse.git
    cd EchoVerse
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Create an environment variable for your IBM Cloud API key. This is required for both Watsonx and TTS services.

**Windows (PowerShell):**
```powershell
$env:WATSONX_API_KEY = "your_ibm_cloud_api_key"
```

**Linux/Mac:**
```bash
export WATSONX_API_KEY="your_ibm_cloud_api_key"
```

Alternatively, create a `.env` file (if you add `python-dotenv` to your project) or set it in your IDE configurations.

### Running the App

Run the Streamlit application:

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`.

## 📂 Project Structure

- `main.py`: The main Streamlit application entry point.
- `model.py`: Handles interaction with IBM Watsonx for text rewriting and tone mapping.
- `tts.py`: Manages IBM Text to Speech generation and voice selection.
- `requirements.txt`: Python package dependencies.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[MIT](LICENSE)
