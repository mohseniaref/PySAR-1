#! /usr/bin/env python
############################################################
# Program is part of PySAR v1.0                            #
# Copyright(c) 2013, Heresh Fattahi                        #
# Author:  Heresh Fattahi                                  #
############################################################
#
# Add 'coherence' option, Yunjun, Jul 2015
#

import sys
import os
from numpy import std
#import matplotlib.pyplot as plt
import h5py
import datetime
import time
def Usage():
  print '''
***************************************************************
***************************************************************
Displayes the general information of the PySAR product h5 file.
 
   Usage:
          info.py file.h5
  
   example:
           
          info.py timeseries.h5
          info.py velocity_demCor_masked.h5
          info.py temporal_coherence.h5
          info.py Loaded_igrams.h5
          info.py Loaded_igrams.h5 3
          info.py Coherence_KyushuT424AlosA.h5

***************************************************************
***************************************************************
'''

def main(argv):

  try:
    File=argv[0]
  except:
    Usage();sys.exit(1)


  h5file=h5py.File(File,'r')
  k=h5file.keys()
  print '******************************************'
  print '******************************************'
  print 'PySAR'
  print '**********************'
  print 'File contains: '+ k[0]
  print '**********************'
  
  if len(k)==1 and k[0] in ('velocity','temporal_coherence','rmse','mask'):
     try:
        h5file[k[0]].attrs['X_FIRST']
        print 'coordinates : GEO'
     except:
        print 'coordinates : radar'
     print '**********************'
     print 'Attributes:'
     print''
     for key , value in h5file[k[0]].attrs.iteritems():
         print key + ' : ' + str(value)       
     
      
  elif 'timeseries' in k:

     try:
        h5file[k[0]].attrs['X_FIRST']
        print 'coordinates : GEO'
     except:
        print 'coordinates : radar'
     print '**********************'
     dateList = h5file['timeseries'].keys()
     print 'Number of epochs: '+str(len(dateList))
     print 'Start Date: '+dateList[0]
     print 'End Date: '+dateList[-1]
     print '**********************'
     print 'List of the dates:'
     print dateList
     print '**********************'
     print 'List of the dates in years'
     t=[]
     for i in range(len(dateList)):
        ti=(datetime.datetime(*time.strptime(dateList[i],"%Y%m%d")[0:5]))
        tt = ti.timetuple()
        ty=tt.tm_year + (tt.tm_mon-1)/12.0 + tt.tm_mday/365.0
        t.append(ty)
     print t
     
     print '*****************************************'
     print 'Standard deviation of aquisition times :'
     print str(std(t)) + ' years'
     print '**********************'
     print 'Attributes:'
     print''
     for key,value in h5file['timeseries'].attrs.iteritems():
         print key + ' : ' + str(value)
     print '*****************************************'
     print 'All groups in this file:'
     print k


  elif 'interferograms' in k:
     ifgramList = h5file['interferograms'].keys()

     try:
        h5file['interferograms'][ifgramList[0]].attrs['X_FIRST']
        print 'coordinates : GEO'
     except:
        print 'coordinates : radar'
     print '**********************'

     try: 
        igramNumber=int(argv[1])
        print ifgramList[igramNumber-1]
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        for key, value in h5file['interferograms'][ifgramList[igramNumber-1]].attrs.iteritems():
            print key, value
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        print ifgramList[igramNumber-1]

     except: 

        print 'Number of interferograms: '+str(len(ifgramList)) 
        print '**********************'
        print 'List of the interferogram: 			eNum'
	eNum=0
        for ifg in ifgramList:
          print ifg + '	' + str(eNum)
	  eNum=eNum+1
     
        print '**********************'
        print 'File contains: '+ k[0]
        print 'Number of interferograms: '+str(len(ifgramList))
        print 'All groups in this file:'
        print k

     for key, value in h5file['interferograms'].attrs.iteritems():
        print key, value


  elif k[0] in ('coherence','wrapped'):
     corList = h5file[k[0]].keys()

     try:
        h5file[k[0]][corList[0]].attrs['X_FIRST']
        print 'coordinates : GEO'
     except:
        print 'coordinates : radar'
     print '**********************'

     try:
        corNumber=int(argv[1])
        print corList[corNumber-1]
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        for key, value in h5file[k[0]][corList[corNumber-1]].attrs.iteritems():
            print key, value
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        print corList[corNumber-1]
     except:
        print 'Number of '+k[0]+': '+str(len(corList))
        print '**********************'
        print 'List of the '+k[0]+':                       eNum'
        eNum=0
        for cor in corList:
          print cor + ' 		' + str(eNum)
          eNum=eNum+1
        print '**********************'
        print 'File contains: '+ k[0]
        print 'Number of '+k[0]+': '+str(len(corList))
        print 'All groups in this file:'
        print k

     for key, value in h5file[k[0]].attrs.iteritems():
        print key, value
 
  print '******************************************'
  print '******************************************'

  h5file.close()


if __name__ == '__main__':

  main(sys.argv[1:])



