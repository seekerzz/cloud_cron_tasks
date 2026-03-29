import subprocess
import os

def run():
    env = os.environ.copy()
    env.pop("http_proxy", None)
    env.pop("https_proxy", None)

    token = env.get("GITHUB_TOKEN")
    user = "h0muraaa"
    repo = "daily-report"

    remote_url = f"https://{token}@github.com/{user}/{repo}.git"

    os.chdir("output")

    cmd = ["git", "push", remote_url, "main", "--force"]
    print(f"Running: git push to {user}/{repo}")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

if __name__ == "__main__":
    run()
