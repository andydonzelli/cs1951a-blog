 #!/bin/bash
 `Make sure to import core_brooklyn_only_binned.db in the current directory`

 sqlite3 -header -csv core_brooklyn_only_binned.db < binned_weather.sql > brooklyn_weather.csv
