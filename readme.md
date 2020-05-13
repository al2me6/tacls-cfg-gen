# tac-cfg-gen

An automatic config generator for TAC Life Support

```
$ python3 tacls-cfg-gen.py --help
usage: tacls-cfg-gen.py [-h] -p PART -c CREW -d DAYS [--partial RESOURCE [RESOURCE ...]] [--day-length HOURS] [--for MOD] [-o FILE]

TACLS config generator v0.1.0

optional arguments:
  -h, --help            show this help message and exit
  -p PART               name of part to patch
  -c CREW               number of Kerbals to support
  -d DAYS               number of days (6.0 hours by default) to supply
  --partial RESOURCE [RESOURCE ...]
                        generate configs only for the specified resources; cannot use with -o
  --day-length HOURS    length of a day, in hours
  --for MOD             add a ModuleManager :FOR[] flag
  -o FILE               output config to file in create-or-append mode, print to stdout if omitted

$ python3 tacls-cfg-gen.py -p DummyPart -c 3 -d 5 --day-length=24 --for DummyMod
@PART[DummyPart]:NEEDS[TacLifeSupport]:FOR[DummyMod]
{
    %RESOURCE[Food]
    {
        %amount = 21.9375
        %maxAmount = 21.9375
    }
    %RESOURCE[Water]
    {
        %amount = 14.4998
        %maxAmount = 14.4998
    }
    %RESOURCE[Oxygen]
    {
        %amount = 2220.7446
        %maxAmount = 2220.7446
    }
    %RESOURCE[CarbonDioxide]
    {
        %amount = 0.0000
        %maxAmount = 1918.7868
    }
    %RESOURCE[WasteWater]
    {
        %amount = 0.0000
        %maxAmount = 18.4650
    }
    %RESOURCE[Waste]
    {
        %amount = 0.0000
        %maxAmount = 1.9950
    }
}
```

## Future plans

* Support other life support mods
* Generate other configurations? Suggestions are welcome

---

## License

(C) Al2Me6 2020.

This script is licensed under the GNU General Public License, using either Version 3 or a later version at your choice.
