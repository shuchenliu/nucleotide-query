#!/bin/bash

input_file="$1"

sort -n -u "$input_file" > unique-"$input_file"