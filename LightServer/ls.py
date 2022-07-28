from flask import Flask, render_template
app = Flask(__name__)
powered = False

@app.route("/")
def turnOn():
   global powered
   if not powered:
      print("turning on")
      powered=1
   return render_template('index.html')

@app.route("/off")
def turnOff():
   global powered
   if powered:
      print("turning off")
      powered=0
   return render_template('/off.html')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)