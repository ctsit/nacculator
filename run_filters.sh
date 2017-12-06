DATE=`date +%Y-%m-%d`
RUNPATH=run_$DATE
NACCPATH=./nacc/redcap2nacc.py

echo "Reading config...." >&2
source filters_config.cfg

mkdir $RUNPATH
curl -v -d token=$token -d content=$content -d format=$format -d type=$type $redcap_server > $RUNPATH/input.csv
echo "--------------Removing subjects already in current--------------------"
PYTHONPATH=. $NACCPATH -f cleanPtid -meta nacculator_cfg.ini < $RUNPATH/input.csv > $RUNPATH/clean.csv
echo "--------------Replacing drug IDs--------------------"
PYTHONPATH=. $NACCPATH -f replaceDrugId < $RUNPATH/clean.csv > $RUNPATH/drugs.csv
echo "--------------Fixing C1S in files--------------------"
PYTHONPATH=. $NACCPATH -f fixHeaders -meta nacculator_cfg.ini < $RUNPATH/drugs.csv > $RUNPATH/fixed_headers.csv
echo "--------------Filling in Defaults--------------------"
PYTHONPATH=. $NACCPATH -f fillDefault < $RUNPATH/fixed_headers.csv > $RUNPATH/default.csv
echo "--------------Updating fields------------------------"
PYTHONPATH=. $NACCPATH -f updateField < $RUNPATH/default.csv > $RUNPATH/Update.csv
echo "--------------Removing Unnecessary Records------------------------"
PYTHONPATH=. $NACCPATH -f removePtid -meta nacculator_cfg.ini < $RUNPATH/Update.csv > $RUNPATH/CleanedPtid_Update.csv
echo "--------------Removing Records without VisitDate------------------------"
PYTHONPATH=. $NACCPATH -f removeDateRecord < $RUNPATH/CleanedPtid_Update.csv > $RUNPATH/final_Update.csv

# TODO Remove Gainesville People (excel) and NueroPath, IVP
#TODO Put all follow ups in a directory, nueropath in a file, ivp in a file.
