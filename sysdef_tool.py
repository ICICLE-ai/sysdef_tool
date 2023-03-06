#!/usr/bin/env python3

import multiprocessing
import logging
import subprocess
import datetime
import re

# From IPF
class Data(object):
    def __init__(self, id=None):
        self.id = id         # an identifier for the content of the document - may be used when publishing
        self.source = None   # set by the engine - an identifier for the source of a document to help route it

    def __str__(self):
        return "data %s of type %s.%s" % (self.id,self.__module__,self.__class__.__name__)
    
    def getRepresentation(self, representation_name):
        pass

class Entity(Data):
    def __init__(self):
        Data.__init__(self)

        #self.CreationTime = datetime.datetime.now(tzoffset(0))
        self.CreationTime = datetime.datetime.now() #TMP ^^^
        self.Validity = None
        self.ID = "urn:ogf:glue2:xsede.org:Unknown:unknown"   # string (uri)
        self.Name = None                        # string
        self.OtherInfo = []                     # list of string
        self.Extension = {}                     # (key,value) strings

class Share(Entity):
    def __init__(self):
        Entity.__init__(self)

        self.Description = None                       # string
        self.EndpointID = []                          # list of string (uri)
        self.ResourceID = []                          # list of string (uri)
        self.EnvironmentID = []                          # list of string (uri)
        self.ServiceID = "urn:ogf:glue2:xsede.org:Service:unknown"  # string (uri)
        self.ActivityID = []                          # list of string (uri)
        self.MappingPolicyID = []                     # list of string (uri)

class ComputingShare(Share):
    def __init__(self):
        Share.__init__(self)

        self.MappingQueue = None                # string
        self.MaxWallTime =  None                # integer (s)
        self.MaxMultiSlotWallTime = None        # integer (s)
        self.MinWallTime = None                 # integer (s)
        self.DefaultWallTime = None             # integer (s)
        self.MaxCPUTime = None                  # integer (s)
        self.MaxTotalCPUTime = None             # integer (s)
        self.MinCPUTime = None                  # integer (s)
        self.DefaultCPUTime = None              # integer (s)
        self.MaxTotalJobs = None                # integer
        self.MaxRunningJobs = None              # integer
        self.MaxWaitingJobs = None              # integer
        self.MaxPreLRMSWaitingJobs = None       # integer
        self.MaxUserRunningJobs = None          # integer
        self.MinSlotsPerJob = None              # integer
        self.MaxSlotsPerJob = None              # integer
        self.MaxStageInStreams = None           # integer
        self.MaxStageOutStreams =  None         # integer
        self.SchedulingPolicy = None            # string?
        self.MaxMainMemory = None               # integer (MB)
        self.GuaranteedMainMemory =  None       # integer (MB)
        self.MaxVirtualMemory = None            # integer (MB)
        self.GuaranteedVirtualMemory = None     # integer (MB)
        self.MaxDiskSpace = None                # integer (GB)
        self.DefaultStorageService = None       # string - uri
        self.Preemption = None                  # boolean
        self.ServingState = "production"        # string
        self.TotalJobs = None                   # integer
        self.RunningJobs = None                 # integer
        self.LocalRunningJobs = None            # integer
        self.WaitingJobs = None                 # integer
        self.LocalWaitingJobs = None            # integer
        self.SuspendedJobs = None               # integer
        self.LocalSuspendedJobs = None          # integer
        self.StagingJobs = None                 # integer
        self.PreLRMSWaitingJobs = None          # integer
        self.EstimatedAverageWaitingTime = None # integer 
        self.EstimatedWorstWaitingTime = None   # integer
        self.FreeSlots = None                   # integer
        self.FreeSlotsWithDuration = None       # string 
        self.UsedSlots = None                   # integer
        self.UsedAcceleratorSlots = None        # integer
        self.RequestedSlots = None              # integer
        self.ReservationPolicy = None           # string
        self.ComputingShareAccelInfoID = ""     # string
        self.Tag = []                           # list of string
        self.EnvironmentID = []                 # list of string
        ### Extra
        self.MaxCPUsPerNode = None              # integer
        # use Endpoint, Resource, Service, Activity from Share
        #   instead of ComputingEndpoint, ExecutionEnvironment, ComputingService, ComputingActivity

        # LSF has Priority
        # LSF has MaxSlotsPerUser
        # LSF has access control
        # LSF has queue status
    def __str__(self):
        out = ''
        out += f'{self.MappingQueue=}\n'
        out += f'{self.MaxWallTime=}\n'
        out += f'{self.MaxMultiSlotWallTime=}\n'
        out += f'{self.MinWallTime=}\n'
        out += f'{self.DefaultWallTime=}\n'
        out += f'{self.MaxCPUTime=}\n'
        out += f'{self.MaxTotalCPUTime=}\n'
        out += f'{self.MinCPUTime=}\n'
        out += f'{self.DefaultCPUTime=}\n'
        out += f'{self.MaxTotalJobs=}\n'
        out += f'{self.MaxRunningJobs=}\n'
        out += f'{self.MaxWaitingJobs=}\n'
        out += f'{self.MaxPreLRMSWaitingJobs=}\n'
        out += f'{self.MaxUserRunningJobs=}\n'
        out += f'{self.MaxSlotsPerJob=}\n'
        out += f'{self.MaxStageInStreams=}\n'
        out += f'{self.MaxStageOutStreams=}\n'
        out += f'{self.SchedulingPolicy=}\n'
        out += f'{self.MaxMainMemory=}\n'
        out += f'{self.GuaranteedMainMemory=}\n'
        out += f'{self.MaxVirtualMemory=}\n'
        out += f'{self.GuaranteedVirtualMemory=}\n'
        out += f'{self.MaxDiskSpace=}\n'
        out += f'{self.DefaultStorageService=}\n'
        out += f'{self.Preemption=}\n'
        out += f'{self.ServingState=}\n'
        out += f'{self.TotalJobs=}\n'
        out += f'{self.RunningJobs=}\n'
        out += f'{self.LocalRunningJobs=}\n'
        out += f'{self.WaitingJobs=}\n'
        out += f'{self.LocalWaitingJobs=}\n'
        out += f'{self.SuspendedJobs=}\n'
        out += f'{self.LocalSuspendedJobs=}\n'
        out += f'{self.StagingJobs=}\n'
        out += f'{self.PreLRMSWaitingJobs=}\n'
        out += f'{self.EstimatedAverageWaitingTime=}\n'
        out += f'{self.EstimatedWorstWaitingTime=}\n'
        out += f'{self.FreeSlots=}\n'
        out += f'{self.FreeSlotsWithDuration=}\n'
        out += f'{self.UsedSlots=}\n'
        out += f'{self.UsedAcceleratorSlots=}\n'
        out += f'{self.RequestedSlots=}\n'
        out += f'{self.ReservationPolicy=}\n'
        out += f'{self.ComputingShareAccelInfoID=}\n'
        out += f'{self.Tag=}\n'
        out += f'{self.EnvironmentID=}\n'
        out += f'{self.MaxCPUsPerNode=}\n'
        return out
    

class Step(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)

        self.id = None        # a unique id for the step in a workflow
        self.description = None
        self.time_out = None
        self.params = {}
        self.requires = []    # Data or Representation that this step requires
        self.produces = []    # Data that this step produces

        self.accepts_params = {}
        self._acceptParameter("id","an identifier for this step",False)
        self._acceptParameter("requires","list of additional types this step requires",False)
        self._acceptParameter("outputs","list of ids for steps that output should be sent to (typically not needed)",
                              False)
        
        self.input_queue = multiprocessing.Queue()
        self.inputs = []  # input data received from input_queue, but not yet wanted
        self.no_more_inputs = False

        self.outputs = {}  # steps to send outputs to. keys are data.name, values are lists of steps

        self.logger = logging.getLogger(self._logName())
    def _acceptParameter(self, name, description, required):
        self.accepts_params[name] = (description,required)
    def _logName(self):
        return self.__module__ + "." + self.__class__.__name__
    def debug(self, msg, *args, **kwargs):
        args2 = (self.id,)+args
        self.logger.debug("%s - "+msg,*args2,**kwargs)


class GlueStep(Step):
    def __init__(self):
        Step.__init__(self)
    def _includeQueue(self, queue_name, no_queue_name_return=False):
        if queue_name == None:
            return no_queue_name_return
        if queue_name == "":
            return no_queue_name_return

        try:
            expression = self.params["queues"]
        except KeyError:
            return True

        toks = expression.split()
        goodSoFar = False
        for tok in toks:
            if tok[0] == '+':
                queue = tok[1:]
                if (queue == "*") or (queue == queue_name):
                    goodSoFar = True
            elif tok[0] == '-':
                queue = tok[1:]
                if (queue == "*") or (queue == queue_name):
                    goodSoFar = False
            else:
                self.warning("can't parse part of Queues expression: "+tok)
        return goodSoFar


class ResourceName(Data):
    def __init__(self, resource_name):
        Data.__init__(self,resource_name)
        self.resource_name = resource_name

class ComputingActivities(Data):
    def __init__(self, id, activities):
        Data.__init__(self,id)
        self.activities = activities
    
class ComputingShares(Data):
    def __init__(self, id, shares):
        Data.__init__(self,id)
        self.shares = shares



class computing_share_ComputingSharesStep(GlueStep):
    def __init__(self):
        GlueStep.__init__(self)

        self.description = "produces a document containing one or more GLUE 2 ComputingShare"
        #self.time_out = 30
        self.time_out = 120
        #self.requires = [ResourceName,ComputingActivities,ComputingShareAcceleratorInfo]
        self.requires = [ResourceName,ComputingActivities]
        self.produces = [ComputingShares]
        self._acceptParameter("queues",
                              "An expression describing the queues to include (optional). The syntax is a series of +<queue> and -<queue> where <queue> is either a queue name or a '*'. '+' means include '-' means exclude. the expression is processed in order and the value for a queue at the end determines if it is shown.",
                              False)

        self.resource_name = None
        self.activities = None

class ComputingSharesStep(computing_share_ComputingSharesStep):

    def __init__(self):
        computing_share_ComputingSharesStep.__init__(self)

        self._acceptParameter("scontrol","the path to the SLURM scontrol program (default 'scontrol')",False)
        self._acceptParameter("PartitionName","Regular Expression to parse PartitionName (default 'PartitionName=(\S+)')",False)
        self._acceptParameter("MaxNodes","Regular Expression to parse MaxNodes (default 'MaxNodes=(\S+)')",False)
        self._acceptParameter("MaxMemPerNode","Regular Expression to parse MaxMemPerNode (default 'MaxMemPerNode=(\S+)')",False)
        self._acceptParameter("DefaultTime","Regular Expression to parse DefaultTime (default 'DefaultTime=(\S+)')",False)
        self._acceptParameter("MaxTime","Regular Expression to parse MaxTime (default 'MaxTime=(\S+)')",False)
        self._acceptParameter("PreemptMode","Regular Expression to parse PreemptMode (default 'PreemptMode=(\S+)')",False)
        self._acceptParameter("State","Regular Expression to parse State (default 'State=(\S+)')",False)
        self._acceptParameter("ReservationName","Regular Expression to parse ReservationName (default 'ReservationName=(\S+)')",False)
        self._acceptParameter("NodCnt","Regular Expression to parse NodCnt (default 'NodCnt=(\S+)')",False)
        self._acceptParameter("State","Regular Expression to parse State (default 'State=(\S+)')",False)

    def _run(self):
        # create shares for partitions
        scontrol = self.params.get("scontrol","scontrol")
        PartitionName = self.params.get("PartitionName","PartitionName=(\S+)")
        MaxNodes = self.params.get("MaxNodes","MaxNodes=(\S+)")
        MaxMemPerNode = self.params.get("MaxMemPerNode","MaxMemPerNode=(\S+)")
        DefaultTime = self.params.get("DefaultTime","DefaultTime=(\S+)")
        MaxTime = self.params.get("MaxTime","MaxTime=(\S+)")
        State = self.params.get("State","State=(\S+)")
        ReservationName = self.params.get("ReservationName","ReservationName=(\S+)")
        NodCnt = self.params.get("NodCnt","NodCnt=(\S+)")
        State = self.params.get("State","State=(\S+)")

        cmd = scontrol + " show partition"
        self.debug("running "+cmd)
        status, output = subprocess.getstatusoutput(cmd)
        if status != 0:
            raise StepError("scontrol failed: "+output+"\n")
        partition_strs = output.split("\n\n")
        #print(partition_strs) # TMP
        partitions = [share for share in map(self._getShare,partition_strs) if self._includeQueue(share.Name)]
        print(partitions[0])

        # create shares for reservations
        scontrol = self.params.get("scontrol","scontrol")
        cmd = scontrol + " show reservation"
        self.debug("running "+cmd)
        status, output = subprocess.getstatusoutput(cmd)
        if status != 0:
            raise StepError("scontrol failed: "+output+"\n")
        reservation_strs = output.split("\n\n")
        try:
            reservations = [self.includeQueue(share.PartitionName) for share in list(map(self._getReservation,reservation_strs))]
        except:
            reservations = []

        self.debug("returning "+ str(partitions + reservations))
        return partitions + reservations

    def _getShare(self, partition_str):
        share = ComputingShare()
        PartitionName = self.params.get("PartitionName","PartitionName=(\S+)")
        MinNodes = self.params.get("MinNodes","MinNodes=(\S+)")
        MaxNodes = self.params.get("MaxNodes","MaxNodes=(\S+)")
        MaxMemPerNode = self.params.get("MaxMemPerNode","MaxMemPerNode=(\S+)")
        DefaultTime = self.params.get("DefaultTime","DefaultTime=(\S+)")
        MaxTime = self.params.get("MaxTime","MaxTime=(\S+)")
        State = self.params.get("State","State=(\S+)")
        ReservationName = self.params.get("ReservationName","ReservationName=(\S+)")
        NodCnt = self.params.get("NodCnt","NodCnt=(\S+)")
        State = self.params.get("State","State=(\S+)")
        PreemptMode = self.params.get("PreemptMode","PreemptMode=(\S+)")
        MaxCPUsPerNode = self.params.get("MaxCPUsPerNode", "MaxCPUsPerNode=(\S+)")
        #Tres = self.param.gets("Tres", "Tres=(\S+=)")

        m = re.search(PartitionName,partition_str)
        if m is not None:
            share.Name = m.group(1)
            share.MappingQueue = share.Name
        m = re.search(MaxNodes,partition_str)
        if m is not None and m.group(1) != "UNLIMITED":
            share.MaxSlotsPerJob = int(m.group(1))
        m = re.search(MinNodes,partition_str)
        if m is not None and m.group(1) != "UNLIMITED":
            share.MinSlotsPerJob = int(m.group(1))
        m = re.search(MaxMemPerNode,partition_str)
        if m is not None and m.group(1) != "UNLIMITED":
            share.MaxMainMemory = int(m.group(1))
        m = re.search(DefaultTime,partition_str)
        if m is not None and m.group(1) != "NONE":
            share.DefaultWallTime = _getDuration(m.group(1))
        m = re.search(MaxTime,partition_str)
        if m is not None and m.group(1) != "UNLIMITED":
            share.MaxWallTime = _getDuration(m.group(1))
        m = re.search(MaxCPUsPerNode, partition_str)
        if m is not None and m.group(1) != "UNLIMITED":
            share.MaxCPUsPerNode = int(m.group(1))
        #m = re.search(Tres, partition_str)
        #if m is not None:
        #    print(Tres)

        m = re.search(PreemptMode,partition_str)
        if m is not None:
            if m.group(1) == "OFF":
                self.Preemption = False
            else:
                self.Preemption = True

        m = re.search(State,partition_str)
        if m is not None:
            if m.group(1) == "UP":
                share.ServingState = "production"
            else:
                share.ServingState = "closed"

        share.EnvironmentID = ["urn:ogf:glue2:xsede.org:ExecutionEnvironment:%s.%s" % (share.Name,self.resource_name)]
        return share

    def _getReservation(self, rsrv_str):
        share = ComputingShare()
        share.Extension["Reservation"] = True

        m = re.search(ReservationName,rsrv_str)
        if m is None:
            raise StepError("didn't find 'ReservationName'")
        share.Name = m.group(1)
        share.EnvironmentID = ["urn:ogf:glue2:xsede.org:ExecutionEnvironment:%s.%s" % (share.Name,self.resource_name)]
        m = re.search(PartitionName,rsrv_str)
        if m is not None:                                                                                              
            share.MappingQueue = m.group(1)
        m = re.search(NodCnt,rsrv_str)
        if m is not None:
            share.MaxSlotsPerJob = int(m.group(1))

        m = re.search(State,rsrv_str)
        if m is not None:
            if m.group(1) == "ACTIVE":
                share.ServingState = "production"
            elif m.group(1) == "INACTIVE":
                m = re.search(StartTime,rsrv_str)
                if m is not None:
                    start_time = _getDateTime(m.group(1))
                    #now = datetime.datetime.now(ipf.dt.localtzoffset())
                    now = datetime.datetime.now() # TMP ^^^
                    if start_time > now:
                        share.ServingState = "queueing"
                    else:
                        share.ServingState = "closed"
        return share

def _getDuration(dstr):
    m = re.search("(\d+)-(\d+):(\d+):(\d+)",dstr)
    if m is not None:
        return int(m.group(4)) + 60 * (int(m.group(3)) + 60 * (int(m.group(2)) + 24 * int(m.group(1))))
    m = re.search("(\d+):(\d+):(\d+)",dstr)
    if m is not None:
        return int(m.group(3)) + 60 * (int(m.group(2)) + 60 * int(m.group(1)))
    raise StepError("failed to parse duration: %s" % dstr)

def convert_to_d(p):
    d = {}
    # List of needed queue information
    print(p.MappingQueue)
    #print(p.MaxSlotsPerJob)
    d['name'] = p.MappingQueue
    d['hpcQueueName'] = p.MappingQueue
    #d['maxJobs'] =
    #d['maxJobsPerUser'] =
    d['minNodeCount'] = p.MinSlotsPerJob
    d['maxNodeCount'] = p.MaxSlotsPerJob
    d['minCoresPerNode'] = 1
    d['maxCoresPerNode'] = p.MaxCPUsPerNode
    d['minMemoryMB'] = 0
    d['maxMemoryMB'] = p.MaxMainMemory
    d['minMinutes'] = int(p.MinWallTime/60.0) if p.MinWallTime else 0
    d['maxMinutes'] = int(p.MaxWallTime/60.0)
    print(d)
    import sys
    sys.exit()
    return d

if __name__ == '__main__':
    step = ComputingSharesStep()
    partitions = step._run()
    for p in partitions:
        if p.MappingQueue != 'parallel':
            continue
        d = convert_to_d(p)
        print(d)