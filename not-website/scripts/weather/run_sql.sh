 #!/bin/bash
 `Make sure to import core_brooklyn_only_binned.db in the current directory`

sqlite3 -header -csv core_all_2014_citi_brooklyn.db < binned_2014_weather.sql > 2014_brooklyn_weather.csv
