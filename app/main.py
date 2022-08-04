# import requirements needed
from flask import Flask, render_template,request
from utils import get_base_url
import pickle
import pandas as pd
import numpy as np

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')
    
    
    
    
    
columns = ['Inches', 'Ram', 'Memory', 'Weight', 'Company_Apple', 'Company_Asus',
       'Company_Chuwi', 'Company_Dell', 'Company_Fujitsu', 'Company_Google',
       'Company_HP', 'Company_Huawei', 'Company_LG', 'Company_Lenovo',
       'Company_MSI', 'Company_Mediacom', 'Company_Microsoft', 'Company_Razer',
       'Company_Samsung', 'Company_Toshiba', 'Company_Vero', 'Company_Xiaomi',
       'TypeName_Gaming', 'TypeName_Netbook', 'TypeName_Notebook',
       'TypeName_Ultrabook', 'TypeName_Workstation',
       'ScreenResolution_1440x900', 'ScreenResolution_1600x900',
       'ScreenResolution_1920x1080', 'ScreenResolution_1920x1200',
       'ScreenResolution_2160x1440', 'ScreenResolution_2256x1504',
       'ScreenResolution_2304x1440', 'ScreenResolution_2400x1600',
       'ScreenResolution_2560x1440', 'ScreenResolution_2560x1600',
       'ScreenResolution_2736x1824', 'ScreenResolution_2880x1800',
       'ScreenResolution_3200x1800', 'ScreenResolution_3840x2160',
       'Cpu_Intel Core i3', 'Cpu_Intel Core i5', 'Cpu_Intel Core i7',
       'Cpu_Intel Other', 'Cpu_Other', 'Gpu_ARM', 'Gpu_Intel Graphics',
       'Gpu_Nvidia GeForce', 'Gpu_Nvidia Quadro/GTX', 'OpSys_Chrome OS',
       'OpSys_Linux', 'OpSys_Mac OS X', 'OpSys_No OS', 'OpSys_Windows 10',
       'OpSys_Windows 10 S', 'OpSys_Windows 7', 'OpSys_macOS']


def encoded_data(data , columns = columns):
    data_list = ['Company', 'TypeName', 'Inches', 'ScreenResolution', 'Cpu','Ram', 'Memory', 'Gpu', 'OpSys', 'Weight']
    numeric_list = []
    categorical_list = []
    for idx,i in enumerate(data):
        
      try:
        int(i)
        numeric_list.append(int(i))
      except:
        try:
            float(i)
            numeric_list.append(float(i))
        except:
            categorical_list.append(f'{data_list[idx]}_{i}')

        
    for i in columns[4:]:
      if i in categorical_list:
        numeric_list.append(1)
      else:
        numeric_list.append(0)

    return numeric_list
    
    
    
    
    
    

# set up the routes and logic for the webserver
@app.route(f'{base_url}' , methods = ['POST','GET'])
def home():
    if request.method == "POST":
        values = [i for i in request.form.values()]
        print(encoded_data(values))
        print(values)
    
        loaded_model = pickle.load(open("finalmodel.sav", 'rb'))
        result = loaded_model.predict(np.array(encoded_data(values)).reshape(1,58))
        print(round(result[0]))
        
        html_df = pd.DataFrame(values).T
        html_df.columns = ['Company', 'TypeName', 'Inches', 'ScreenResolution', 'Cpu','Ram', 'Memory', 'Gpu', 'OpSys', 'Weight']
        
        df_html = html_df.to_html(classes="table table-dark")
        pred = f"With the given attributes the cost of the laptop approximatley {round(result[0])} euros."
    
        return render_template('index.html' , values = pred ,
                               df_html = df_html)
    return render_template('index.html')

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc1.ai-camp.dev'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
