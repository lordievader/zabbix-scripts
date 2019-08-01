# Collection of Zabbix scripts
This is a collection of Zabbix scripts. Mostly Python scripts to do discovery.
But at times also scripts to perform a specific monitoring task.
I typically clone this repo into `/usr/lib/zabbix/external_scripts`.

This repository part of my Zabbix collection: [zabbix][1]

## Discovery of ssl endpoints
The `discover_ssl.py` script reads `/etc/zabbix/urls.txt` for the SSL enpoints
(URLs and PORT) and returns this as a json which Zabbix can use.
I use two `UserParameter`s with this:

```
UserParameter=discovery.ssl,/usr/lib/zabbix/externalscripts/discover_ssl.py
UserParameter=ssl_valid[*],date +%s -d "$(echo Q |timeout 5 openssl s_client -connect tide-project.nl:443 2>/dev/null|openssl x509 -noout -enddate|sed 's,notAfter=,,')"
```

The `discovery.ssl` returns endpoints in the format of:
```
{
    "{#PORT}": "443",
    "{#URL}": "example.com",
}
```

This can then be used to fill the `ssl_valid[{#URL},{#PORT}]` parameters.
The `ssl_valid` key returns a UNIX timestamp. When you create a calculated item
which subtracts `system.localtime[utc]` from the `ssl_valid` time you get the
years/months/days of validity left. On which we have triggers.

## Discovery of systemd services
`discover_systemd.py` discovers systemd services. It produces two macros
`{#NAME}` and `{#SERVICENAME}`. The `{#NAME}` variable is as it is outputted by
systemd. `{#SERVICENAME}` is a modified version thereof where illegal
characters are removed. Hence in Zabbix items you want to use `{#SERVICENAME}`
as the argument. The script `systemd.py`, which checks if a service is active,
does the reverse operation before feeding it to `systemctl`.

[1]: https://github.com/lordievader/zabbix
