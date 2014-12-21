@ECHO OFF
ECHO staring runs...

FOR /L %%G IN (1,1,1) DO start /wait main.py -topology FATTREE -backups 0 -requests 4000
ECHO run 1 complete

FOR /L %%G IN (1,1,1) DO start /wait main.py -topology NACRE -backups 0 -requests 4000
ECHO run 2 complete

FOR /L %%G IN (1,1,1) DO start /wait main.py -topology JELLYFISH -backups 0 -requests 4000
ECHO run 3 complete

set /p DUMMY=All done! Hit ENTER to continue...
