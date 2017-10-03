DATE=`date +%Y-%m-%d`
RUNPATH=run_$DATE
NACCPATH=./nacc/redcap2nacc.py

echo "Reading config...." >&2
source filters_config.cfg

mkdir $RUNPATH
curl -v -d token=$token -d content=$content -d format=$format -d type=$type $redcap_server > $RUNPATH/input.csv
echo "--------------Removing subjects already in current--------------------"
PYTHONPATH=. $NACCPATH -f cleanPtid -meta current-db-subjects.csv < $RUNPATH/input.csv > $RUNPATH/clean.csv
echo "--------------Replacing drug IDs--------------------"
PYTHONPATH=. $NACCPATH -f replaceDrugId < $RUNPATH/clean.csv > $RUNPATH/drugs.csv
echo "--------------Fixing C1S in files--------------------"
PYTHONPATH=. $NACCPATH -f fixC1S < $RUNPATH/drugs.csv > $RUNPATH/c1s.csv
echo "--------------Filling in Defaults--------------------"
PYTHONPATH=. $NACCPATH -f fillDefault < $RUNPATH/c1s.csv > $RUNPATH/default.csv
echo "--------------Updating fields------------------------"
PYTHONPATH=. $NACCPATH -f updateField < $RUNPATH/default.csv > $RUNPATH/finalUpdate.csv
# TODO Remove Gainesville People (excel) and NueroPath, IVP
#TODO Put all follow ups in a directory, nueropath in a file, ivp in a file.

