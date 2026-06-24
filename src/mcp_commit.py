import os, sys, asyncio
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

GITHUB_PAT = os.environ["GITHUB_PAT"]
MCP_URL = "https://api.githubcopilot.com/mcp/"
OWNER = "hanishalikose"
REPO = "lesson-deliverable-agent"
BRANCH = "main"

async def commit_file(repo_path: str, content: str, message: str):
    headers = {"Authorization": f"Bearer {GITHUB_PAT}"}
    async with streamablehttp_client(MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "create_or_update_file",
                {
                    "owner": OWNER,
                    "repo": REPO,
                    "branch": BRANCH,
                    "path": repo_path,
                    "content": content,
                    "message": message,
                },
            )
            return result

if __name__ == "__main__":
    local_path = sys.argv[1]
    with open(local_path) as f:
        content = f.read()
    repo_path = "deliverables/" + os.path.basename(local_path)
    result = asyncio.run(
        commit_file(repo_path, content, f"Add deliverable: {os.path.basename(local_path)}")
    )
    print(result)