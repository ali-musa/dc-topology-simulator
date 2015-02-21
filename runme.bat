@ECHO OFF
ECHO staring runs...

FOR /L %%G IN (1,1,20) DO (
	start /wait main.py -topology NACRE -backups 0 -requests 3000 -backupstrategy END_TO_END -stopafterrejects 1
	ECHO %%G
)
ECHO run 1 complete

REM FOR /L %%G IN (1,1,1) DO (
	REM ECHO %%G
	REM start /wait main.py -topology NACRE -backups 0 -requests 1000 -stopafteraccepts 500 -backupstrategy END_TO_END
REM )
REM ECHO run 2 complete

REM FOR /L %%G IN (1,1,1) DO (
	REM ECHO %%G
	REM start /wait main.py -topology JELLYFISH  -backups 0 -requests 1000 -stopafteraccepts 500
REM )
REM ECHO run 3 complete

set /p DUMMY=All done! Hit ENTER to continue...


