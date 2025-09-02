# main.py

import argparse
import os
import sys
import logging

# Add the agent package to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "txn_insights_agent"))

from txn_insights_agent.agent import root_agent

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_locally():
    """Starts the local ADK web development server."""
    logger.info("Starting ADK web server for local development...")
    from google.adk import web
    web.main(args=["--agent_path=txn_insights_agent/agent.py", "--"])


def deploy_to_agent_engine():
    """Deploys the agent to Vertex AI Agent Engine."""
    logger.info("Starting deployment to Vertex AI Agent Engine...")

    try:
        import vertexai
        from vertexai.preview import reasoning_engines
    except ImportError:
        logger.error("Vertex AI SDK not found. Please install it with: pip install 'google-cloud-aiplatform[adk,agent_engines]'")
        return

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    staging_bucket = os.getenv("STAGING_BUCKET")

    if not all([project_id, location, staging_bucket]):
        logger.error("Missing required environment variables: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, STAGING_BUCKET")
        return

    logger.info(f"Initializing Vertex AI for project '{project_id}' in '{location}'...")
    vertexai.init(project=project_id, location=location, staging_bucket=staging_bucket)

    # Wrap the ADK agent in an AdkApp object to make it deployable
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    logger.info("Creating and deploying the agent engine... This may take several minutes.")
    remote_app = reasoning_engines.create(
        reasoning_engine=app,
        requirements=["google-cloud-aiplatform[adk,agent_engines]"],
        display_name="TXN Insights Agent",
        description="Agent for analyzing financial transaction data."
    )

    logger.info(f"✅ Agent deployed successfully!")
    logger.info(f"Resource Name: {remote_app.resource_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run or deploy the TXN Insights ADK Agent.")
    parser.add_argument(
        "command",
        choices=["local", "deploy"],
        help="Choose 'local' to run the dev server or 'deploy' to deploy to Agent Engine."
    )
    args = parser.parse_args()

    if args.command == "local":
        run_locally()
    elif args.command == "deploy":
        deploy_to_agent_engine()