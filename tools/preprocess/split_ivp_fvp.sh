#!/bin/sh

head -n 1 $1 > initial_visits.csv
grep "initial_visit" $1 >> initial_visits.csv
head -n 1 $1 > followup_visits.csv
grep "followup_visit" $1 >> followup_visits.csv