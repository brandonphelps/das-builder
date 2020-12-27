import docker
import os
from jinja2 import Environment, FileSystemLoader
import argparse
from das_builder.utils import search_for_root, load_config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# move this to shared module for utils.

CONFIG_FILE_NAME = "das_builder.toml"


def run_build(client, image, command):
    pass


def chown_dir(root_path, uid, gid):
    print(root_path)
    for root, dirs, files in os.walk(root_path):
        print(dirs)
        print(files)
        for d in dirs:
            os.chown(os.path.join(root, d), uid=uid, gid=gid)

        for f in files:
            os.chown(os.path.join(root, f), uid=uid, gid=gid)


def main():
    current_dir = search_for_root(os.getcwd())
    config = load_config(os.path.join(current_dir, CONFIG_FILE_NAME))

    image_name = config["das-builder"]["image"]

    client = docker.from_env()
    j2_env = Environment(
        loader=FileSystemLoader(os.path.join(THIS_DIR, "templates")), trim_blocks=True
    )

    os.makedirs(os.path.join(current_dir, ".das_builder"), exists_ok=True)

    with open(
        os.path.join(current_dir, ".das_builder", "docker_builder.sh"), "w"
    ) as writer:
        writer.write(
            j2_env.get_template("conan_build.sh").render(image_name=image_name,
                                                         uid=os.getuid(),
                                                         gid=os.getgid())
        )

    cont = client.containers.run(
        image_name,
        # todo: should be a config option?
        auto_remove=True,
        # todo: allow user direct command pass through?
        # path join generates host system file paths not guest system.
        command=["/bin/bash", os.path.join(".das_builder", "docker_builder.sh")],
        volumes={current_dir: {"bind": "/work_dir", "mode": "rw"}},
        working_dir="/work_dir",
        detach=True,
    )
    cont.wait()
    print(cont.logs().decode("utf-8"))

    # todo: need to obtain the output directory from the build process
    # chown_dir(f"build/{image_name}", uid=os.getuid(), gid=os.getgid())
