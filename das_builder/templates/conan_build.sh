#!/bin/bash

conan install . -if build/{{ image_name }}
conan build . -bf build/{{ image_name }}
