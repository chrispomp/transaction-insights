Follow these steps in your terminal from the root transaction-insights directory.

A. Set Up Environment
Create a Virtual Environment (Recommended):

Bash

python3 -m venv .venv
source .venv/bin/activate
Install Dependencies:

Bash

pip install google-adk "google-cloud-aiplatform[adk,agent_engines]"
Authenticate with Google Cloud:
This command will open a browser window for you to log in. This allows the ADK to access your GCP resources like BigQuery and Vertex AI.

Bash

gcloud auth application-default login
B. Run Locally for Testing
Use the adk web command via our main.py script to start a local web interface where you can chat with your agent.

Bash

python3 main.py local
This will start a server, usually at http://127.0.0.1:8000. Open this URL in your browser to interact with the txn_insights_agent.

C. Deploy to Agent Engine
When you are ready to deploy your agent to a scalable, production-ready environment, run the following command:

Bash

python3 main.py deploy