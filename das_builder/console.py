import docker
import time
import os
from jinja2 import Environment, FileSystemLoader
import argparse
from das_builder.utils import search_for_root, load_config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# todo: move this to shared module for utils.
CONFIG_FILE_NAME = "das_builder.toml"


def main():
    current_dir = search_for_root(os.getcwd())
    config = load_config(os.path.join(current_dir, CONFIG_FILE_NAME))

    image_name = config["das-builder"]["image"]

    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(THIS_DIR, "templates")), trim_blocks=True
    )

    os.makedirs(os.path.join(current_dir, ".das_builder"), exist_ok=True)

    with open(
        os.path.join(current_dir, ".das_builder", "docker_builder.sh"), "w"
    ) as writer:
        writer.write(
            j2_env.get_template("conan_build.sh").render(
                image_name=image_name, uid=os.getuid(), gid=os.getgid()
            )
        )

    client = docker.from_env()
    cmd = ["/bin/bash", os.path.join(".das_builder", "docker_builder.sh")]

    cont = client.containers.run(
        image_name,
        # todo: allow user direct command pass through?
        # path join generates host system file paths not guest system.
        command=cmd,
        volumes={current_dir: {"bind": "/work_dir", "mode": "rw"}},
        working_dir="/work_dir",
        detach=True,
    )

    for log_line in cont.logs(stream=True):
        print(log_line.decode("utf-8").strip())
