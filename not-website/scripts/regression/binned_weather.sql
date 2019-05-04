SELECT br.bin_time AS bin_time,
       br.company AS company,
       br.date_time AS unix_time,
       bw.sunny AS sunny,
       bw.windy AS windy,
       bw.rainy AS rainy,
       bw.cloudy AS cloudy,
       bw.temperature AS temp,
       bw.dew_point AS dew_point,
       bw.uv_index AS uv_index,
       bw.precip_intensity AS precip_intensity,
       bw.wind_speed AS wind_speed,
       bw.cloud_cover AS cloud_cover,
       bw.apparent_temperature
FROM binned_rides AS br, binned_weather AS bw
WHERE br.bin_time = bw.bin_time;
