gemini-vertex-dynamic-grounding
Dynamic LLM Deployment with Gemini AI and Vertex AI Grounding

This repository provides a simple yet effective implementation of Gemini AI, complemented by Vertex AI for real-time data grounding. It dynamically detects when Gemini lacks real-time data by identifying specific phrases and then calls Vertex AI to supply accurate, grounded information. The setup is designed for ease of deployment, and the repository includes everything necessary to build and package the project into a Docker image.

## Clone the repository and set up the environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/gemini_dynamic_grounding.git
cd gemini_dynamic_grounding

# Install dependencies
pip install -r requirements.txt

# Set up your Google API credentials
export google_api_key="YOUR_GOOGLE_API_KEY"

# Set up Vertex AI credentials
export vertex_project_name="YOUR_VERTEX_PROJECT_NAME"

# Run the FastAPI server
uvicorn fastAPI_for_vertex:app --reload
