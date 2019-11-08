# elastic-practice

Commands to run the containers:

```shell script
sudo sysctl -w vm.max_map_count=262144
docker-compose up
```

The first line may not be necessary, but in my case the ES containers crash if I don't change this setting.
It'll be reset to its previous value on system reboot,
but you can also set it permanently in the `/etc/sysctl.conf` file.

More details e.g. here:  
https://stackoverflow.com/a/51448773/4744341,  
https://github.com/docker-library/elasticsearch/issues/111
