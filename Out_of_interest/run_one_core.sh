#!/bin/sh
#$ -V
#$ -cwd
#$ -S /bin/bash
#$ -N Py_1_core
#$ -o $JOB_NAME.o$JOB_ID
#$ -e $JOB_NAME.e$JOB_ID
#$ -q omni
#$ -pe sm 1
#$ -P quanah

python run_file.py > result_one_core.txt