import re
import datetime
import time 

def convertToMillisec(strDate):
  if(strDate):
    sec = time.mktime(datetime.datetime.strptime(strDate, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
    t = re.search(r'.+\.(\d{3})$', strDate)
    millisec = "%.0f" % sec + t.group(1)
    return millisec
  return '-'

jobs = dict()
# /var/log/slurm-llnl/slurmctld.log
with open("/var/log/slurm-llnl/slurmctld.log") as f:
  for line in f:
    str = line.rstrip()
    m = re.search(r'\[([0-9:\.\-T]+)\] _slurm_rpc_submit_batch_job JobId=(\d+) usec=(\d+)', str)
    if(m):
      # print(m.group(1), m.group(2), m.group(3))
      # sec = time.mktime(datetime.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%f").timetuple())
      # t = re.search(r'.+\.(\d{3})$', m.group(1))
      # millisec = "%.0f" % sec + t.group(1)
      jobs[m.group(2)] = {'submitted': convertToMillisec(m.group(1)), 'usec': m.group(3)}

    m = re.search(r'\[([0-9:\.\-T]+)\] sched: Allocate JobID=(\d+) .+', str)
    if(m):
      # print(m.group(1), m.group(2))
      # sec = time.mktime(datetime.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%f").timetuple())
      # t = re.search(r'.+\.(\d{3})$', m.group(1))
      # millisec = "%.0f" % sec + t.group(1)      
      jobs[m.group(2)].update({'allocate': convertToMillisec(m.group(1))})

    m = re.search(r'\[([0-9:\.\-T]+)\] job_complete: JobID=(\d+) State=0x1 .+', str)
    if(m):
      # print(m.group(1), m.group(2))
      # sec = time.mktime(datetime.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%f").timetuple())
      # t = re.search(r'.+\.(\d{3})$', m.group(1))
      # millisec = "%.0f" % sec + t.group(1)
      jobs[m.group(2)].update({'complete_0x1': convertToMillisec(m.group(1))})

    m = re.search(r'\[([0-9:\.\-T]+)\] job_complete: JobID=(\d+) State=0x8003 .+', str)
    if(m):
      # print(m.group(1), m.group(2))
      jobs[m.group(2)].update({'complete_0x8003': convertToMillisec(m.group(1))})


out = []
i = 0
e = 5
n = 1
freq = 1.2
ops = [50000,100000,500000,1000000,5000000]
k = 0
# with open('your_file.txt', 'w') as f:
  # f.write("JobID,n,ops,freq,1 submitted,2 allocate,3 complete 0x1,4 complete 0x8003,usec\n")
for z in range(1,20):
    # print(jobs[key])
    # print("\n\n")
  i = i + 1
    # print("%d" % n)
    # print(key+","+n.__str__()+","+ops[k].__str__()+","+freq.__str__()+","+jobs[key]['submitted']+","+jobs[key]['allocate']+","+jobs[key]['complete 0x1']+","+jobs[key]['complete 0x8003']+","+jobs[key]['usec']+"\n")
    # print(i%5)
  if (i%5 == 0):
    print("here")
    if(n == 1):
      n = 2
    else:
      n = 1
    # if (i*2 % 10 == 0):
    #   k = k + 1
    # if (i == len(ops) * 2 * e):
    #   f = 2.6
    # print("%s,%d,%d,%.1f,%s,%s,%s,%s,%s\n" % (key,n,ops[k],freq,jobs[key]['submitted'],jobs[key]['allocate'],jobs[key]['complete 0x1'],jobs[key]['complete 0x8003'],jobs[key]['usec']))
    # f.write(key+","+n.__str__()+","+ops[k].__str__()+","+freq.__str__()+","+jobs[key]['submitted']+","+jobs[key]['allocate']+","+jobs[key]['complete 0x1']+","+jobs[key]['complete 0x8003']+","+jobs[key]['usec']+"\n")
    # out.append(jobs[key])


for key, value in jobs.items():
  value.update({'JobID': key})
  out.append(value)

import csv

keys = out[0].keys()
with open('out.csv', 'w')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(out)
