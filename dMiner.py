#!/usr/bin/env python

from random import randint, sample
from scapy.all import *
import argparse as argp
import sys, socket


FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80
g_max_try = 20
g_ini_parts = 5

def chopReq(iReq, n):
  if len(iReq) < 2:
    print 'Atomic chunk:', iReq
    return iReq
  if n < 0:
    return chopReq(iReq, randint(2, len(iReq)))
  # if n > len(iReq):
  #   return None
  # if n < 2:
  #   return iReq
  elif n > len(iReq):
    return chopReq(iReq, len(iReq))
  else:
    print 'Choping', iReq, 'into', n, 'partitions.'
    rs = sorted(sample(range(1, len(iReq)), n-1), key = int)
    reqs = []
    for idx, r in enumerate(rs):
      if idx == 0:
        reqs.append(iReq[:r])
        # elif idx == len(rs)-1:
        #   reqs.append(iReq[r:])
      else:
        reqs.append(iReq[rs[idx-1]:r])
    reqs.append(iReq[rs[len(rs)-1]:])
    return reqs
      
  # reqp = iReq[:r]
  # reqc = iReq[r:]
  # return reqp, reqc

def dMin(iReq, trg, maxTry):
  if maxTry < 0:
    print 'Maxed out on number of attempts to minimize', iReq
    return iReq
  
  print 'Minimizing', iReq
  miniReqs = iReq
  
  chunks = chopReq(iReq, -1)
  if chunks is iReq:
    return iReq
  
  else:
    print 'Attempting minimization with', chunks
    for idx, c in enumerate(chunks):
      c_p = [i for i in [e for chk in chunks for e in chk] if i not in c] # c prime
      # if tryReq(c, trg) == 1:
      #   # minimize c
      #   miniReqs = c
      #   dMin(c, trg, g_max_try)

      # elif tryReq(c_p, trg) == 1:
      #   # minimize c_p
      #   miniReqs = c_p
      #   dMin(c_p, trg, g_max_try)

      # elif idx == len(chunks-1):
      #   dMin(iReq, trg, maxTry-1)


      if tryReq(c, trg) == 1:
        # minimize c
        miniReqs = c
        break
        
      elif tryReq(c_p, trg) == 1:
        # minimize c_p
        miniReqs = c_p
        break
        
    if miniReqs is iReq:
      return dMin(miniReqs, trg, maxTry-1)
    else:
      return dMin(miniReqs, trg, g_max_try)
      
        
  
#   if len(iReq) > 1 :
#     reqp, reqc = splitReq(iReq)
#   else:
#     reqp = iReq
#     reqc = []
#   print 'Minimizing', iReq, 'by breaking into', reqp, 'and', reqc

#   if maxTry > 0 and tryReq(reqp, trg) == 1:
#     dMin(reqp, trg, maxTry-1)
#   elif maxTry > 0 and tryReq(reqc, trg) == 1:
#     dMin(reqc, trg, maxTry-1)
#   elif maxTry > 0:
#     print 'Retrying:', iReq
#     dMin(iReq, trg, maxTry-1)
#   else:
#     print 'Minimum set is:', iReq
#     return iReq

def tryDlg(dialogue, trgPacks): 
  trgLoad = []
  # for p in trgPacks:
  #   trgLoad.append(p[Raw].load)


  #test case for target
  trgLoad = ['Content-Type: application/zip']
  
  resp = []
  for t in range(32):
    resp.append(''.join(reqReplay(dialogue)))
  print resp

  # f = open('test_out', 'w')
  # for r in resp:
  #   f.write(r)
  
  # for o in resp:
  #   print o, '\nand then\n'

  strResp = ''.join(resp)
  
  res = 1
  for tl in trgLoad:
    # print 'comparing for:\n', tl
    if tl in strResp:
      res = res & 1
    else:
      res = res & 0
  return res


def reqReplay(dialogue):

  resp = []
  for conn, reqs in dialogue.iteritems():
    addr = conn.split()[3].split(':')[0]
    port = int(conn.split()[3].split(':')[1])
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servAddr = (addr, port)
    print >>sys.stderr, 'starting up on %s port %s' % servAddr
    try:
      sock.connect(servAddr)
      print >>sys.stderr, 'connection established. Sending data.'
    except socket.error as e:
      print e
      # sys.exit()

    for r in reqs:
      rawLoad = r[Raw].load
      try:
        # print 'Sending:', rawLoad
        sock.sendall(rawLoad)
        resp.append(sock.recv(4096))
      except socket.error as e:
        print e
        # sys.exit()
    
  return resp

  # resp = [r*2 for r in iReq]
  # # record responses to the requests made
  # return resp
 

# def reqReplay(iReqs):
#   for req in iReqs:
#     pass


def preProcPacket(opax):

  cliAddr = '127.0.0.1'
  cliPort = randint(1024,65535)
  srvAddr = '127.0.0.1'
  srvPort = 80
  synFound = False
  conn = {'cli': [cliAddr, cliPort], 'srv': [srvAddr, srvPort]}
  req_sess = {}

  for p in opax:
    if p['TCP'].flags == SYN:
      synFound = True
      conn['cli'][0] = p['IP'].src
      conn['cli'][1] = p['TCP'].sport
      conn['srv'][0] = p['IP'].dst
      conn['srv'][1] = p['TCP'].dport
      break

  if synFound:
    for key, sess in opax.sessions().iteritems():
      if key.split()[1].split(':')[0] == conn['cli'][0]:
        for p in opax.sessions()[key]: 
          if ( p['TCP'].flags != SYN and
               p['TCP'].flags != ACK and
               p['TCP'].flags != FIN and
               p['TCP'].flags != SYN+ACK and
               p['TCP'].flags != FIN+ACK):
            if key in req_sess.keys():
              req_sess[key].append(p)
            else:
              req_sess[key] = [p]

  # for conn, pl in req_sess.iteritems():
  #   print conn
  #   for p in pl:
  #     print p[Raw].load

  return req_sess



def main():

  ap = argp.ArgumentParser(description = 'Network Dialogue Minimizer.' )
  ap.add_argument('op', help = 'Original Pcap file to be minimized.')
  ap.add_argument('tp', help = 'Target Pcap file as minimization target')
  ap.add_argument('ts', help = 'Target Server for querying')

  args = ap.parse_args()

  opax = rdpcap(args.op)
  tpax = rdpcap(args.tp)
  tServ = args.ts.split(':')

  reqs = preProcPacket(opax)

  print tryDlg(reqs, tpax)
  
  # data = reqs['TCP 192.168.56.130:37356 > 192.168.56.129:4000'][0][Raw].load

  # resp = reqReplay(reqs)
  # for r in resp:
  #   print r
  
  # print chopReq([1,2,3,4,5,6,7,8,9,11,22,33,44,55,66,77,88,99], 20)
  # print chopReq([1], 4)
  # print dMin([0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9], [4,0,10], g_max_try)


if __name__ == '__main__':
  main()
