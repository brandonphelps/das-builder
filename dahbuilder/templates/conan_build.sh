#!/bin/bash

conan install . -if build/docker
conan build . -bf build/docker


