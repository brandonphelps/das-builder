#!/bin/bash

conan install . -if build/{{ image_name }}
conan build . -bf build/{{ image_name }}

chown -R {{ uid }}:{{ gid }} build/
sleep 5
