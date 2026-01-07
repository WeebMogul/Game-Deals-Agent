# Game Deal Agent

## Introduction

An agent built with the purpose of finding your favourite video games on discount across different stores such as Steam, Epic Games Stores, Fanatical etc. This project uses Google's Agent Development kit and the CheapShark API (for finding game deals) as the backend, with Streamlit acting as the frontend.

## Features

- **Finding game discounts across different stores**: Outputs a list of games on discount from different stores 
- **Specific game discount**: Got a game you want to find a discount for ? That can do it too.
- **Responsive Design**: Works across desktop and mobile devices

## Limitations

- **API Rate Limits**: Subject to Google Cloud API quotas and CheapShark API rate limiting
- **Internet Dependency**: Requires active internet connection for API calls
- **Latency**: Response times depend on network speed and API processing time
- **Agent Capabilities**: Limited to the specific capabilities of the configured ADK agents
- **Concurrent Users**: Streamlit Community Cloud has limitations on concurrent users for free tier
- **Memory**: Agent memory persists only within the session; no long-term storage by default

## How to Activate

### Prerequisites

- Python 3.8 or higher
- Google Cloud account with ADK access
- API credentials for Google's Agent Development Kit

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone hhttps://github.com/WeebMogul/Game-Deals-Agent.git
   cd Game-Deals-Agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r reqs.txt
   ```

4. **Set up Google Cloud credentials**
   - Create a key in Google AI Studio on the API Keys page.
     
5. **Configure the application**
   - Create a .env file
   - Update configuration values:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=0
     GOOGLE_API_KEY=your-google-api-key-from-google-ai-studio
     ```

6. **Activate the API**
   You can do this by running 
   ```bash
   adk api_server
   ```
   and
   ```bash
   streamlit run app.py
   ```
   in different terminal windows or run it via docker
   ```bash
   docker-compose up
   ```

   You can view the streamlit application

For issues, questions, or contributions, please open an issue on the project repository.