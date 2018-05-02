#!/usr/bin/env python

from random import randint, sample

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

def tryReq(iReq, trg):
  res = 1
  for t in trg:
    if t in iReq:
      res = res & 1
    else:
      res = res & 0
  return res

 

def main():
  
  # print chopReq([1,2,3,4,5,6,7,8,9,11,22,33,44,55,66,77,88,99], 20)
  # print chopReq([1], 4)
  print dMin([0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9], [5,0,2], g_max_try)
  pass

if __name__ == '__main__':
  main()
