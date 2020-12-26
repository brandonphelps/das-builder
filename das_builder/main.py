
import docker
import os
from  jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))



def main():
    current_dir = os.path.abspath(os.getcwd())
    client = docker.from_env()
    print("Current dir: {}", current_dir)

    j2_env = Environment(loader=FileSystemLoader(os.path.join(THIS_DIR, 'templates')),
                         trim_blocks=True)

    with open(os.path.join(current_dir, 'docker_builder.sh'), 'w') as writer:
        writer.write(j2_env.get_template('conan_build.sh').render())

    print("Running container")
    cont = client.containers.run("conanio/gcc7", command=["bash", "docker_builder.sh"], volumes={current_dir: {"bind": "/work_dir", "mode" : "rw"}}, working_dir="/work_dir", detach=True)
    
    print(cont.logs())
