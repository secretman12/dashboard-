from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask import Flask, flash, request, redirect, url_for
import pandas as pd
from sqlalchemy import create_engine, types





app = Flask(__name__)
api = Api(app)





mydb = create_engine("mysql://user:pass@db:3306/test_db")
    

connection = mydb.raw_connection()
cursor = connection.cursor()





class UploadCSV(Resource):

 

    def post(self):

        file = request.files['']
        data = pd.read_excel(file)
        data= data.dropna() 
        print(data)
        parseCSV(data)



def parseCSV(filePath):
       
                for i,row in filePath.iterrows():
                        
                    col_names = ['Από','Έως','Aριθμός ανακτημένων προσωρινών Α.Ο.','ΑΝΑΤΟΛΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ ΘΡΑΚΗΣ','ΑΤΤΙΚΗΣ','ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ','ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ','ΔΥΤΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ','ΗΠΕΙΡΟΥ',
                'ΘΕΣΣΑΛΙΑΣ','ΙΟΝΙΩΝ ΝΗΣΩΝ','ΚΕΝΤΡΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ','ΚΡΗΤΗΣ','ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ','ΠΕΛΟΠΟΝΗΣΟΥ','ΣΤΕΡΕΑΣ ΕΛΛΑΔΑΣ']
                    sql = "INSERT INTO arxeia (apo, eos,arithmos_prosorinon_ao, anatolikis_makedonias_tharkis,attikis,voreio_agaio, dytikis_elladas,dytikis_makedonias,ipeiros,thessalias,ionion_nision,kentrikis_makedonias,kritis,notio_aigaio,pelloponisos,stereas_elladas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                    value = (row['Από'],row['Έως'],row['Aριθμός ανακτημένων προσωρινών Α.Ο.'],row['ΑΝΑΤΟΛΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ ΘΡΑΚΗΣ'],row['ΑΤΤΙΚΗΣ'],row['ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ'],row['ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ'],row['ΔΥΤΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ'],row['ΗΠΕΙΡΟΥ'],row['ΘΕΣΣΑΛΙΑΣ'],row['ΙΟΝΙΩΝ ΝΗΣΩΝ'],row['ΚΕΝΤΡΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ'],row['ΚΡΗΤΗΣ'],row['ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ'],row['ΠΕΛΟΠΟΝΗΣΟΥ'],row['ΣΤΕΡΕΑΣ ΕΛΛΑΔΑΣ'])
                    cursor.execute(sql, value)
                    connection.commit()
                   

        
        



         
             


             


api.add_resource(UploadCSV, '/add') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
