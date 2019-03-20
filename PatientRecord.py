import csv
import time
import datetime
import os
import glob

class Patient:
  def fetchDocuments(self):
    column_names = []
    documents = []
    f = open( "RG2/Case_Documents.csv" , "r" )
    csvFile = csv.reader( f )
    for row in csvFile:
      if len( column_names ) == 0:
        column_names = row
        continue
      if int(row[0]) == int(self.caseID):
        documents.append( {
          'CaseId' : int( row[0] ) ,
          'DocName' : row[1] ,
          'DocType' : row[2] ,
          'DateOfService' : datetime.datetime.strptime( row[3] , "%Y-%m-%d %H:%M:%S" )
        } )

    f.close()

    return documents
  
  def combineDocuments(self):
    ret = ""
    for item in self.documents:
      ret = ret + str( item['DocType'] ) + " "
      f = open( "./Raw_Texts/temp/"+item['DocName'] , "r" )
      rd = f.read()
      rd = rd.split("\n")
      ret = ret + ( " ".join( rd ) ).strip() + " "
      f.close()
    return ret

  def combineDocumentsModified(self):
    ret = ""
    iden = str( self.documents[0]['DocName'] )[:6]
    files = []
    for file in glob.glob("./Raw_Texts/temp/*.*"):
      if iden in file:
        files.append( file )
    for file in files:
      print( file )
      f = open( file , "r" )
      rd = f.read()
      rd = rd.split("\n")
      ret = ret + " ".join( rd ) + " "
    return ret.strip()
  
  def fetchDocTypes(self):
    ret = set()
    for doc in self.documents:
      ret.add( doc['DocType'].lower() )
    return ret

  def __init__(self, caseID, dob, gender, dateOfAdmission, dateOfDischarge, patientClass, serviceLine, dischargeDisposition):
    self.caseID = caseID
    self.dob = dob
    self.gender = gender
    self.dateOfAdmission = dateOfAdmission
    self.dateOfDischarge = dateOfDischarge
    self.patientClass = patientClass
    self.serviceLine = serviceLine
    self.dischargeDisposition = dischargeDisposition
    self.documents = self.fetchDocuments()
    self.age = int( ( self.dob - self.dateOfAdmission ).days / 365.25 )
    self.duration = int( ( self.dateOfDischarge - self.dateOfAdmission ).days )