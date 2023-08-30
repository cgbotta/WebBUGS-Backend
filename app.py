from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
   # s = subprocess.check_output('OpenBUGS script.txt', shell=True).decode('utf-8').strip()

   # return s

   return "Hello, World!"

@app.route('/please/')
def please():
   s = subprocess.check_output('OpenBUGS script.txt', shell=True).decode('utf-8')

   return s

   # return "Hello, World!"

@app.route('/compile/', methods=['GET', 'POST'])
def compile():
   data = True
   inits = True
   monitor = True
   to_monitor = []
   try:
      user_input = request.form['user_input']
      if user_input:
         with open('model.txt', 'w') as f:
            f.write(user_input)
      else:
         return "error: no BUGS code specified"
      
      data_input = request.form['data_input']
      if data_input:
         with open('data.txt', 'w') as f:
            f.write(data_input)
      else:
         data = False
      
      inits_input = request.form['inits_input']
      if inits_input:
         with open('inits1.txt', 'w') as f:
            f.write(inits_input)
      else:
         inits = False

      monitor_input = request.form['monitors_input']
      if monitor_input:
         to_monitor = monitor_input.strip().split(',')
      else:
         monitor = False
   except Exception as e:
      return "error:" + str(e)


   try:
      with open('final_script.txt', 'w') as f:
         f.write('modelCheck(\'./model.txt\')\n')
         # f.write('modelSaveState(\'model_state.txt\')')

         if data:
            f.write('modelData(\'./data.txt\')\n')
         f.write('modelCompile(1)\n')
         if inits:
            f.write('modelInits(\'./inits1.txt\',1)\n')
         # f.write('modelSaveState(\'model_state1.txt\')')
         # f.write('modelDisplay(\'log\')')
         # f.write('modelGenInits()\n')

         
         f.write('modelUpdate(1000)\n')
         # f.write('modelSaveState(\'model_state2.txt\')')

         if monitor:
            for var in to_monitor:
               f.write('samplesSet(\'' + var + '\')\n')
               # f.write('summarySet(\'' + var + '\')\n')

         f.write('modelUpdate(10000)\n')
         # f.write('modelSaveState(\'model_state3.txt\')')
         if monitor:
         #    for var in to_monitor:
         #       f.write('samplesCoda(\'' + var + '\',\'c\')\n')
            f.write('samplesCoda(\'*\',\'c\')\n')

         f.write('samplesStats(\'*\')\n')

   except Exception as e:
      return "error:" + str(e)

   s = subprocess.check_output('OpenBUGS final_script.txt', shell=True).decode('utf-8')

   
   info = []
   if os.path.isfile('cCODAindex.txt'):
      with open('cCODAindex.txt', 'r') as f:
         lines = f.readlines()
         for line in lines:
            values = line.strip().split()
            info.append(values)

   data = []
   if os.path.isfile('cCODAchain1.txt'):
      with open('cCODAchain1.txt', 'r') as f:
         lines = f.readlines()
         for var_info in info:
            name = "{0}".format(var_info[0])
            start = int(var_info[1])
            end = int(var_info[2])
            to_append = []
            for i in range(start - 1, end):
               to_append.append(float(lines[i].strip().split()[1]))
            data.append((name, to_append))

   data = {
      "logs": s,
      "data":data
   }

   if os.path.isfile('model.txt'):
      os.remove('model.txt')
   if os.path.isfile('data.txt'):
      os.remove('data.txt')
   if os.path.isfile('inits1.txt'):
      os.remove('inits1.txt')
   # if os.path.isfile('final_script.txt'):
   #    os.remove('final_script.txt')
   if os.path.isfile('cCODAchain1.txt'):
      os.remove('cCODAchain1.txt')
   if os.path.isfile('cCODAinput.txt'):
      os.remove('cCODAinput.txt')

   return json.dumps(data)

   # if data and inits:
   #    s = subprocess.check_output('OpenBUGS script.txt', shell=True).decode('utf-8')
   #    print("data and inits")
   # elif data:
   #    s = subprocess.check_output('OpenBUGS script_2.txt', shell=True).decode('utf-8')
   #    print("data")
   # elif inits:
   #    s = subprocess.check_output('OpenBUGS script_3.txt', shell=True).decode('utf-8')
   #    print("inits")
   # else:
   #    s = subprocess.check_output('OpenBUGS script_4.txt', shell=True).decode('utf-8')
   #    print("code only")
   # return s

# @app.route('/run/', methods=['GET', 'POST'])
# def run():
#    try:
#       with open('user_model.txt', 'w') as f:
#          f.write(request.form['user_input'])
#    except Exception as e:
#       print("error:", e)
#       return str(e)

#    s = subprocess.check_output('OpenBUGS script.txt', shell=True).decode('utf-8')
#    return s


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=3000)