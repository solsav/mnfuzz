#!/usr/bin/env python

from random import randint, sample

g_max_try = 20
g_ini_parts = 5

def chopReq(iReq, n):
  if n == -1:
    n = randint(0, len(iReq)/2)
  # if n > len(iReq):
  #   return None
  if n < 2:
    return iReq
  else:
    rs = sorted(sample(range(1, len(iReq)), n-1), key = int)
    print rs
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

  miniReqs = iReq
  
  chunks = splitReq(iReq, g_ini_parts)
  if chunks is iReq:
    return iReq
  else:
    for c in chunks:
      c_p = [i for i in [e for chk in chunks for e in chk] if i not in c] # c prime
      if tryReq(c, trg) == 1:
        # minimize c
        pass
      elif tryReq(c_p, trg) == 1:
        # minimize c_p
        
  
  
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

# def tryReq(iReq, trg):
#   res = 1
#   for t in trg:
#     if t in iReq:
#       res = res & 1
#     else:
#       res = res & 0
#   return res



def main():
  
  # print splitReq([1,2,3,4,5,6,7,8,9,11,22,33,44,55,66,77,88,99], 3)
  # print dMin([0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9], [5,6,8], g_max_try)
  pass

if __name__ == '__main__':
  main()
