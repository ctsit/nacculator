DATE=`date +%Y-%m-%d`
RUNPATH=run_$DATE
NACCPATH=./nacc/redcap2nacc.py

echo "Reading config...." >&2
source filters_config.cfg

mkdir $RUNPATH
curl -v -d token=$token -d content=$content -d format=$format -d type=$type $redcap_server > $RUNPATH/input.csv
# echo "--------------Removing subjects already in current--------------------"
# PYTHONPATH=. $NACCPATH -f cleanPtid -meta current-db-subjects.csv < $RUNPATH/input.csv > $RUNPATH/clean.csv
echo "--------------Replacing drug IDs--------------------"
PYTHONPATH=. $NACCPATH -f replaceDrugId < $RUNPATH/input.csv > $RUNPATH/drugs.csv
echo "--------------Fixing C1S in files--------------------"
PYTHONPATH=. $NACCPATH -f fixC1S < $RUNPATH/drugs.csv > $RUNPATH/c1s.csv
echo "--------------Fixing FVP in files--------------------"
PYTHONPATH=. $NACCPATH -f fixFVP < $RUNPATH/c1s.csv > $RUNPATH/fixed_fvp.csv
echo "--------------Filling in Defaults--------------------"
PYTHONPATH=. $NACCPATH -f fillDefault < $RUNPATH/fixed_fvp.csv > $RUNPATH/default.csv
echo "--------------Updating fields------------------------"
PYTHONPATH=. $NACCPATH -f updateField < $RUNPATH/default.csv > $RUNPATH/Update.csv
echo "--------------Removing Unnecessary Records------------------------"
PYTHONPATH=. $NACCPATH -f removePtid < $RUNPATH/Update.csv > $RUNPATH/CleanedPtid_Update.csv
echo "--------------Removing Records without VisitDate------------------------"
PYTHONPATH=. $NACCPATH -f removeDateRecord < $RUNPATH/CleanedPtid_Update.csv > $RUNPATH/fixedDate_Update.csv
echo "--------------Removing subjects already in current Intial Visit--------------------"
PYTHONPATH=. $NACCPATH -f_ivp cleanPtid -meta current-db-subjects.csv < $RUNPATH/fixedDate_Update.csv > $RUNPATH/ivp_clean.csv
echo "--------------Removing events other than Intial Visit--------------------"
PYTHONPATH=. $NACCPATH -f_ivp removeRedCapEvent < $RUNPATH/ivp_clean.csv > $RUNPATH/Final_Update_ivp.csv
# echo "--------------Removing subjects already in current Followup Visit--------------------"
# PYTHONPATH=. $NACCPATH -f_fvp cleanPtid -meta current-db-subjects.csv < $RUNPATH/fixedDate_Update.csv > $RUNPATH/fvp_clean.csv
echo "--------------Removing events other than Followup Visit--------------------"
PYTHONPATH=. $NACCPATH -f_fvp removeRedCapEvent < $RUNPATH/ivp_clean.csv > $RUNPATH/Final_Update_fvp.csv

# TODO Remove Gainesville People (excel) and NueroPath, IVP
#TODO Put all follow ups in a directory, nueropath in a file, ivp in a file.
