#!/bin/bash

echo "starting"
sleep 20
echo "Installing"
conan install . -if build/{{ image_name }}
sleep 20
echo "Building"
conan build . -bf build/{{ image_name }}
sleep 10

chown -R {{ uid }}:{{ gid }} build/

