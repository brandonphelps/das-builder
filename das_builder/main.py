
import docker
import os
from  jinja2 import Environment, FileSystemLoader
import argparse


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class RunnerArgs:
    pass

def search_for_root():
    """
    return the path containing the configuration file to read from for loading up and running. 
    """
    
def extract_args(config_file):
    """
    Read from the config file and pull out the intresting arguments to pass to the execu line
    """
    




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help="name of docker image to use")

    args = parser.parse_args()

    
    

    current_dir = os.path.abspath(os.getcwd())
    client = docker.from_env()
    j2_env = Environment(loader=FileSystemLoader(os.path.join(THIS_DIR, 'templates')),
                         trim_blocks=True)

    with open(os.path.join(current_dir, 'docker_builder.sh'), 'w') as writer:
        writer.write(j2_env.get_template('conan_build.sh').render())

    cont = client.containers.run(args.image,
                                 command=["bash", "docker_builder.sh"],
                                 volumes={current_dir: {"bind": "/work_dir",
                                                        "mode" : "rw"}},
                                 working_dir="/work_dir", detach=True)
    for i in cont.output:
        print(i)

