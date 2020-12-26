
import docker
import os
from  jinja2 import Environment, FileSystemLoader
import argparse


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE_NAME = "das_builder.toml"

class RunnerArgs:
    pass

def search_for_root(search_start=os.getcwd(), file_search=CONFIG_FILE_NAME):
    """
    return the path containing the configuration file to read from for loading up and running. 
    """

    current_dir = os.path.abspath(search_start)
    if os.path.exists(os.path.join(current_dir, file_search)):
        return current_dir
    prev_p = current_dir
    next_p = os.path.dirname(current_dir)
    while next_p != prev_p and not os.path.exists(os.path.join(next_p, file_search)):
        print(f"N: {next_p}")
        print(f"P: {prev_p}")
        prev_p = next_p
        next_p = os.path.dirname(prev_p)
    if os.path.exists(os.path.join(next_p, file_search)):
        return next_p
    else:
        return None

    
def extract_args(config_file):
    """
    Read from the config file and pull out the intresting arguments to pass to the execu line
    """
    




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help="name of docker image to use")

    args = parser.parse_args()

    current_dir = search_for_root(os.getcwd())
    client = docker.from_env()
    j2_env = Environment(loader=FileSystemLoader(os.path.join(THIS_DIR, 'templates')),
                         trim_blocks=True)

    with open(os.path.join(current_dir, 'docker_builder.sh'), 'w') as writer:
        writer.write(j2_env.get_template('conan_build.sh').render())

    # todo remove images after they finish. 
    cont = client.containers.run(args.image,
                                 command=["bash", "docker_builder.sh"],
                                 volumes={current_dir: {"bind": "/work_dir",
                                                        "mode" : "rw"}},
                                 working_dir="/work_dir", detach=True)

    # todo: have option to produce output 
    for i in cont.output:
        print(i)

