import os
import shutil
import subprocess


def deploy_app() -> None:
    docker_exec = shutil.which("docker")
    if docker_exec is None:
        print("Docker not found")
        exit(1)

    os.chdir("../..")
    subprocess.call(["chmod", "+x", "./deploy.sh"])
    subprocess.call(["sh", "-c", "./deploy.sh"])
    os.chdir("./webhooks/github")
