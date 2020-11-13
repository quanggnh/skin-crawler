import requests
import json
from PIL import Image
import pandas as pd
import pathlib
import os

"""This is a module to fetch data from the archive International Skin Imaging Collaboration using its API 

For further information about the API,please go to this website: https://isic-archive.com/api/v1/ """


    
def ISIC_request(response,num=100):
    """Fetching the metadata of the images that later on might be used by sending a HTTP request to the ISIC's REST API
        
    Parameters:
    
    num(int):   Number of the images that you want to get from the archive,default is 100
        
    Returns:
    
    Json:Response metadata in JSON format"""
    start_url = 'https://isic-archive.com/api/v1/image?limit='+str(num)+'&sort=name&sortdir=-1&detail=true'
    headers =  {
        'Accept': 'application/json'
    }
    r = requests.get(start_url, headers=headers)
    data = r.json()
    return data

def ISIC_getdata(numjson = 100,numimage = 20):
    """Download images from internet that are confirmed melanocytic in its metadata and are classified as being acquired through dermoscopy and creating a CSV from metadata of such images"
    
    Parameters:
    
    numjson(int):   Number of metadata sets of images that you get from the parse() function.Default is 100
    
    numimage(int):  Number of images you want to get that are both true to the requirements(dermoscopic image and being melanocytic) from the metadata sets.Should be more than numjson.Default is 20
    """
    if (numjson < numimage or not isinstance(numjson,int) or not isinstance(numimage,int) ):
        print("Invalid parameters")
    else:
        dataset = parse(numimage)
        output = {}
        output2 = []
        i = 0
        for set in dataset:
            if(str(set['meta']['acquisition']['image_type'])=='dermoscopic' and set['meta']['clinical']['melanocytic']==True):

                output['Id'] = str(set['_id'])

                output['Name'] = str(set['name'])
                
                output['Age'] = str(set['meta']['clinical']['age_approx'])
                
                output['General Anatomy Site'] = str(set['meta']['clinical']['anatom_site_general'])
                
                output['Description'] = str(set['dataset']['description'])

                output['Diagnosis'] = str(set['meta']['clinical']['diagnosis'])
                
                output['Sex']= str(set['meta']['clinical']['sex'])
                
                output['Confirmed Diagnosis']= str(set['meta']['clinical']['diagnosis_confirm_type'])
                
                headers =  {
                    'Accept': 'application/json'
                }
                r = requests.get("https://isic-archive.com/api/v1/image/"+output['Id']+"/download",headers = headers)
                if not os.path.exists("Image"):
                    os.makedirs("Image")
                with open(str(pathlib.Path(__file__).parent.absolute())+"/Image/"+str(output['Name']),'wb') as f:
                    f.write(r.content)                    
                output2.append(output)
                i=i+1
                if(i==numimage):
                    break
        df = pd.DataFrame.from_dict(output2)
        
        df.to_csv(r''+str(pathlib.Path(__file__).parent.absolute())+'/Metadata.csv',index=False,header=True)


if __name__=="__main__":
    
    """ Main function
    
    """
    ISIC_getdata()


