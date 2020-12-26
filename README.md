
Just a small python app for interfacing with docker and a folder directory and running commands with expected output to be in the same directory. 

Attempting to help move some build system and steps into docker contains then produce output into the root directory of where they are ran. 

Some templates are provided to help with specific common setups. 


config file. 
placing a file named das_builder.toml at the root of your project will allow for a 
searching upwards to find the root directory to which the docker container will be launched at that dir, the directory will be copied into the docker container and ran produce output as specified. 



# schema

[das-builder]
command = "conan_build"
