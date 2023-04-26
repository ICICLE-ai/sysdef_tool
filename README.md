# System Definition Tool

## Description

This repository contains a tool that can used to generate a system definition file for use with Tapis. Run this script on the system that you are trying to add to Tapis and use the resulting `json` file when creating the system in [Tapis](https://tapis-project.org).

## How-To

Begin my logging into the system which you want to add to Tapis. The script can be run in either interactive or batch mode.

Once the script has completed, a file called `system_def.json` is created. This can be passed to the Python API of Tapis with: 

```
import json
from tapipy.tapis import Tapis
t = Tapis(base_url='https://tacc.tapis.io', username='<userid>', password='************')
with open('system_def.json', 'r') as openfile:
    my_storage_system = json.load(openfile)
t.systems.createSystem(**my_storage_system)
```

See Tapis's documentation [here](https://tapis.readthedocs.io/en/latest/technical/systems.html) for more information about creating Systems in Tapis.

### Interactive Mode

To run in interactive mode, run:

```
./sysdef_tool.py -i
```

In this mode, the tool will fill in all system information that it can determine. For any information that the tool cannot determine, it will request that the user provide the correct value. Unless otherwise specified, the user can press enter to leave the value empty.

Here is a sample execution of the script:

```
$ ./sysdef_tool.py -i
(required) Enter value of "id" [pitzer-skhuvis]: pitzer-test
Enter value of "description": Test of sysdef tool
Enter value of "systemType" [LINUX]:
Enter value of "owner":
Enter value of "host" [pitzer]:
Enter value of "enabled" [True]:
Enter value of "effectiveUserId" [${apiUserId}]:
Enter value of "defaultAuthnMethod" [PKI_KEYS]:
Enter value of "authnCredential":
Enter value of "rootDir" [/]:
Enter value of "port" [22]:
Enter value of "jobRuntimes" [SINGULARITY]:
Enter value of "jobWorkingDir" [HOST_EVAL($HOME)/jobs/${JobUUID}]:
Enter value of "jobMaxJobs":
Enter value of "jobMaxJobsPerUser": 2000
Enter value of "batchDefaultLogicalQueue" [batch]: serial
Enter value of "tags":
Enter value of "notes":
System definition created in system_def.json
```


### Batch mode

To run in batch mode, execute:

```
./sysdef_tool.py -b
```

In this mode, the tool will fill in all system information that it can determine. For values that are required, it will leave the value as `MISSING`. If a value could not be determined and is not required, then the field is removed from the output file.

Here is part of a sample json file produced by the tool:

```
{
    "id": "pitzer-skhuvis",
    "systemType": "LINUX",
    "host": "pitzer",
    "enabled": true,
    "effectiveUserId": "${apiUserId}",
    "defaultAuthnMethod": "PKI_KEYS",
    "isDtn": false,
    "rootDir": "/",
    "port": 22,
    "canExec": true,
    "canRunBatch": true,
    "jobRuntimes": [
        {
            "runtimeType": "SINGULARITY"
        }
    ],
    "jobWorkingDir": "HOST_EVAL($HOME)/jobs/${JobUUID}",
    "batchScheduler": "SLURM",
    "batchDefaultLogicalQueue": "batch",
    "batchLogicalQueues": [
        {
            "name": "batch",
            "hpcQueueName": "batch",
            "minNodeCount": 0,
            "minCoresPerNode": 1,
            "maxCoresPerNode": 45,
            "minMemoryMB": 0,
            "minMinutes": 0,
            "maxMinutes": 10080
        }
    ]
}
```

## Acknowledgements

Parts of this tool were taken from the [IPF tool](https://github.com/XSEDE/ipf) from XSEDE. The following classes were taken from IPF:

1. `Data`
2. `Entity`
3. `Share`
4. `ComputingShare`
5. `Step`
6. `GlueStep`
7. `ResourceName`
8. `ComputingActivities`
9. `ComputingShares`
10. `computing_share_ComputingSharesStep`
11. `ComputingSharesStep`

