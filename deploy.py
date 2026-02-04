import os
import json
import dtlpy as dl

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars

# Replace placeholder in dataloop.json with actual value
bot_username = os.getenv('BOT_USERNAME', None)
original_content = None

try:
    if bot_username:
        # Read original content
        with open('./dataloop.json', 'r') as f:
            original_content = f.read()
        
        # Replace the placeholder
        content = original_content.replace('${BOT_USERNAME}', bot_username)
        
        with open('./dataloop.json', 'w') as f:
            f.write(content)

    dl.setenv('rc')
    # dl.login()
    p = dl.projects.get(project_id='f8a4b8ce-5ff3-4386-84dc-1bda3a5bc92a')
    d = p.dpks.publish()

finally:
    # Always restore placeholder after deployment (even if it fails)
    if original_content and bot_username:
        with open('./dataloop.json', 'w') as f:
            f.write(original_content)