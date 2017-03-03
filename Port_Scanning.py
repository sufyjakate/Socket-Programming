import socket
import urllib
import re
import csv
import os
import smtplib
import multiprocessing
from time import sleep
# Function for retrieving IP address
def ip_retrieve():
    url = 'http://www2.mpdl.mpg.de/seco_irmapubl/expoipra_all?style=expo00'
    print  'Retrieving', url
    open_url = urllib.urlopen(url)
    data = open_url.read()
    data = re.sub('\ipra_asterix', '', data)
    data = data.strip()
    count = 0

    for p in data.split('\n'):
        # print p
        ip = p.split('.')

        # print ip
        for i, a in enumerate(ip):
            # print ip[i]
            if a.find('-') != -1:
                ip[i] = [j for j in range(int(a.split('-')[0]), int(a.split('-')[1]) + 1)]
            elif a.find('*') != -1:
                ip[i] = [j for j in range(0, 256)]
            else:
                ip[i] = [int(ip[i])]
        # print ip
        for a in ip[0]:
            for b in ip[1]:
                for c in ip[2]:
                    for d in ip[3]:
                        ip_address = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)
                        # print ip_address
                        count = count + 1
                        print count
                        checkport(ip_address)

#def worker_thread((inputs, times)):
#    print 'Process %s are waiting from %s secs' % (inputs, times)
#    time.sleep(int(times))


# Function for Port Scanning
def checkport(ip_address):
    smtp = smtplib.SMTP()
    status =smtp.connect(ip_address,25)
    #print status
    #print type(status)
    if status[0] == 220:
        port_status = "Port is Open."
    else:
        port_status = "Port is Closed."
    output_file = open('status_test.csv', 'ab')
    out_writer = csv.writer(output_file)
    out_writer.writerow([repr(ip_address) + ',' + repr(port_status)])
    # print count
    output_file.close()
    # return port_status

def thread_handler():
    proc2 = multiprocessing.Pool(4)
    proc2.map(checkport(ip_retrieve()))

if __name__ == '__main__':
    thread_handler()