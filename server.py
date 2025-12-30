import os
import subprocess
from fastmcp import FastMCP

mcp = FastMCP("arjun-mcp")

@mcp.tool()
def do_arjun(
    url: str = "",
    textFile: str = "",
    wordlist: str = "",
    method: str = "",
    rateLimit: int | None = None,
    chunkSize: int | None = None,
) -> str:
    """
    Run Arjun to discover hidden HTTP parameters.

    Args:
        url: Target URL to scan for hidden parameters (required if textFile not provided).
        textFile: Path to file containing multiple URLs (optional, exclusive with url).
        wordlist: Path to custom wordlist file.
        method: HTTP method to use (GET, POST, JSON, HEADERS).
        rateLimit: Maximum requests per second.
        chunkSize: Number of parameters to send at once.
    """

    if not url and not textFile:
        raise ValueError("Either 'url' or 'textFile' must be provided")

    cmd = ["arjun"]
    if url:
        cmd += ["-u", url]
    if textFile:
        cmd += ["-f", textFile]
    if wordlist:
        cmd += ["-w", wordlist]
    if method:
        cmd += ["-m", method]
    if rateLimit is not None:
        cmd += ["--ratelimit", str(rateLimit)]
    if chunkSize is not None:
        cmd += ["-c", str(chunkSize)]

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=600,
        )
    except FileNotFoundError as e:
        raise RuntimeError("Arjun binary not found in container PATH") from e

    output = (completed.stdout or "") + (completed.stderr or "")

    if completed.returncode != 0:
        raise RuntimeError(f"Arjun exited with code {completed.returncode}: {output.strip()}")

    return output.strip()


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        path="/mcp",
    )
