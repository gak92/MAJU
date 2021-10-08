########################################################## Importing Libraries
import ast
import re
import tkinter as tk
from PIL import ImageTk, Image
import face_recognition
import os
import cv2
import mysql.connector
from PIL import ImageTk, Image
from tkinter import filedialog
import shutil
import numpy as np

######################################################### Main Window Settings
root = tk.Tk()
root.title("Facial Recognition System")
root.iconbitmap('./frs.ico')
# root.geometry("1250x800")

root.attributes("-fullscreen", False)
root.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                    not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

######################################################### Database Connection
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "frs"
)

print(conn)

########################################################## Select Query
mycursor = conn.cursor()
mycursor.execute("SELECT f1 FROM frs")
myresult = mycursor.fetchall()
# print(type(myresult), len(myresult))
# print(myresult[0])

kfaces = []
for i in range(len(myresult)):
    f = myresult[i]
    flst = re.sub('\s+', ',', f[0])
    farr = np.array(ast.literal_eval(flst))
    kfaces.append(farr)


#print(kfaces)

# f1 = myresult[0]
# print(f1[0])
# print(type(f1[0]))

# f1lst = re.sub('\s+', ',', f1[0])
# print(f1lst)

# f1arr = np.array(ast.literal_eval(f1lst))
# print(f1arr)
# print(type(f1arr))



#mycursor.execute('SET GLOBAL max_allowed_packet=67108864')

############################################################### INSERT RECORD
def insert_record(uname, img_path, known_images):
    NAME = uname
    IMAGE = img_path
    #F1 = "[-0.02116332  0.13720067  0.10318542 -0.05196164 -0.17237011  0.05090503 -0.0889101  -0.02987301  0.15273921 -0.05662467  0.20970015  0.05968854 -0.20885052 -0.08554964 -0.09161564  0.06531018 -0.09849533 -0.10098393 -0.07948841  0.02035731  0.03339933  0.06060907  0.07988704  0.0488099 -0.05197472 -0.36315969 -0.12083968 -0.02779869  0.07716605 -0.09454514 -0.01260472  0.04241971 -0.22068635 -0.09646179 -0.01459705  0.03064538 -0.15456331 -0.06465548  0.1760533   0.05165669 -0.13947421  0.06036856 -0.04066943  0.29222757  0.13596857  0.10196032  0.01804152 -0.0796313  0.0822889  -0.24933571  0.08348437  0.24492575  0.17023982  0.06991183  0.12161578 -0.17172427  0.16406588  0.19796439 -0.20911437  0.06352677 -0.0426515  -0.10612943  0.09046756 -0.03477132 -0.02116332  0.13720067  0.10318542 -0.05196164 -0.17237011  0.05090503 -0.0889101  -0.02987301  0.15273921 -0.05662467  0.20970015  0.05968854 -0.20885052 -0.08554964 -0.09161564  0.06531018 -0.09849533 -0.10098393 -0.07948841  0.02035731  0.03339933  0.06060907  0.07988704  0.0488099 -0.05197472 -0.36315969 -0.12083968 -0.02779869  0.07716605 -0.09454514 -0.01260472  0.04241971 -0.22068635 -0.09646179 -0.01459705  0.03064538 -0.15456331 -0.06465548  0.1760533   0.05165669 -0.13947421  0.06036856 -0.04066943  0.29222757  0.13596857  0.10196032  0.01804152 -0.0796313  0.0822889  -0.24933571  0.08348437  0.24492575  0.17023982  0.06991183  0.12161578 -0.17172427  0.16406588  0.19796439 -0.20911437  0.06352677 -0.0426515  -0.10612943  0.09046756 -0.03477132]"

    print("Length of known images: ", len(known_images))
    print("Type of known images: ", type(known_images))
    print(len(known_images[0]))
    print(type(known_images[0]))

    # f1 = np.array_str(known_images[0])
    # print(f1)
    # print(type(f1))
    f = []
    for img in known_images:
        f.append(np.array_str(img))

    print(f[0])
    print(type(f[0]))
    print(len(f))

    # INSERT INTO TABLES
    sql = "INSERT INTO frs (name, image, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (NAME, IMAGE, f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9])
    mycursor.execute(sql, val)

    conn.commit()
    print(mycursor.rowcount, "record inserted.")
    # conn.close()


######################################################### Declaring Variables
PATH = 'C:/Users/ali/PycharmProjects/Face Recognition System/'
KNOWN_FACES_DIR = "./known_faces"
UNKNOWN_FACES_DIR = "./unknown_faces"
known_names = []

####################################################### Training Area GUI
my_train_frame = tk.LabelFrame(root, text="Upload Training Data", padx=5, pady=5, width=600, height=400)
my_train_frame.grid(row=0, column=0, padx=5, pady=2)
my_train_frame.grid_propagate(False)


def load_train_images():
    root.dirname = filedialog.askdirectory(initialdir="./", title="Select a folder")
    train_img_entry_box.insert(0, root.dirname)

    my_train_img_label = tk.Label(my_train_frame, text=root.dirname)
    my_train_img_label.grid(row=1, column=0, columnspan=5)


train_img_entry_box = tk.Entry(my_train_frame, width=40)
train_img_entry_box.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
train_img_load_btn = tk.Button(my_train_frame, text="Select Folder", command=load_train_images)
train_img_load_btn.grid(row=0, column=6)

def load_data():
    mycursor.execute("SELECT name FROM frs")
    uname = mycursor.fetchall()
    uname_lst = [uname[i][0] for i in range(len(uname))]

    rows = []
    for i in range(len(uname_lst)):
        cols = []
        for j in range(1):
            e = tk.Entry(my_train_frame, relief=tk.GROOVE)
            e.grid(row=i+7, column=j, sticky=tk.NSEW)
            e.insert(tk.END,  uname_lst[i])
            cols.append(e)
        rows.append(cols)

load_data()

######################################################## Testing Area GUI
my_test_frame = tk.LabelFrame(root, text="Upload Test Image", padx=5, pady=5, width=600, height=400)
my_test_frame.grid(row=0, column=1, padx=5, pady=2)
my_test_frame.grid_propagate(False)

def load_test_image():
    global my_test_img
    global my_test_img_label
    root.filename = filedialog.askopenfilename(initialdir="./", title="Select a file",
                                               filetypes=(("all files", "*.*"), ("jpg files", "*.jpg")))

    # my_test_img_label = tk.Label(my_test_frame, text=root.filename)
    # my_test_img_label.grid(row=2, column=0)
    test_img_entry_box.insert(0, root.filename)

    WIDTH, HEIGHT = 300, 300
    resize_img = Image.open(root.filename).resize((WIDTH, HEIGHT), Image.ANTIALIAS)

    my_test_img = ImageTk.PhotoImage(resize_img)
    # my_test_img = ImageTk.PhotoImage(Image.open(root.filename))
    my_test_img_label = tk.Label(my_test_frame, image=my_test_img)
    my_test_img_label.grid(row=1, column=1)


test_img_entry_box = tk.Entry(my_test_frame, width=40)
test_img_entry_box.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
test_img_load_btn = tk.Button(my_test_frame, text="Open File", command=load_test_image)
test_img_load_btn.grid(row=0, column=6)


########################################################### TRaining Data (Images)
def training_data():
    print("Loading known faces...")
    print(root.dirname)
    TRAINING_DIR = root.dirname

    mycursor.execute("SELECT name FROM frs")
    name_exist = mycursor.fetchall()
    print(name_exist[0][0])
    print(type(name_exist[0][0]))
    ne = [name_exist[i][0] for i in range(len(name_exist))]
    print(ne)

    for name in os.listdir(TRAINING_DIR):
        print("\nName of Person: ",name)
        known_faces = []
        if name not in ne:
            for i, filename in enumerate(os.listdir(f"{TRAINING_DIR}/{name}")):
                if i == 0:
                    dest_dir = KNOWN_FACES_DIR
                    src_dir = f"{TRAINING_DIR}/{name}"
                    print(src_dir, " -- ", dest_dir)
                    src_file = src_dir + "/" + filename   #os.path.join(src_dir, filename)
                    print("source file: ", src_file)
                    shutil.copy(src_file, dest_dir)  # copy the file to destination dir

                    os.chdir(dest_dir)              # change directory to destination folder
                    dest_file = filename
                    oldfname, ext = filename.split(".")
                    print(oldfname, ext)
                    newfname = name + "." + ext
                    os.rename(dest_file, newfname)  # rename
                    print("destination file:", newfname)
                    img_path = KNOWN_FACES_DIR + "/" + newfname

                print("Images: ",filename)
                # resize_img = Image.open(f"{TRAINING_DIR}/{name}/{filename}").resize((300, 300), Image.ANTIALIAS)
                # print("Resize image: ", type(resize_img))
                image = face_recognition.load_image_file(f"{TRAINING_DIR}/{name}/{filename}")
                print(type(image), len(image))
                try:
                    encoding = face_recognition.face_encodings(image)[0]
                    print("encoding: \n", encoding)
                except:
                    print("Error in processing image", i, filename)

                known_faces.append(encoding)
                known_names.append(name)
            insert_record(name, img_path, known_faces)
            os.chdir(TRAINING_DIR)


    # print(len(known_faces), len(known_names))
    #print(known_names)
    #print(known_faces)
    load_data()     # Refresh list of name


start_training_btn = tk.Button(my_train_frame, text="Start Training", command=training_data)
start_training_btn.grid(row=3, column=1)
# training_data()


##################################################################### Testing Data(Images)
TOLERANCE = 0.5
FRAME_THICKNESS = 2
FONT_THICKNESS = 2
MODEL = "cnn"


def testing_data():
    global my_test_img
    global my_test_img_label
    print("Processing test image...", root.filename)
    # for filename in os.listdir(UNKNOWN_FACES_DIR):
    image = face_recognition.load_image_file(root.filename)
    # print("before encoding: \n", image)
    locations = face_recognition.face_locations(image, model=MODEL)
    # print("Locations: ", locations)
    print("Length of locations(Number of person in testing image): ", len(locations))
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # print("after encoding: \n", image)

    mycursor.execute("SELECT id,name FROM frs")
    name_exist = sorted(mycursor.fetchall())
    print("\n name_exist:------>>>>>", type(name_exist), name_exist)
    ne = [name_exist[i][1] for i in range(len(name_exist))]

    print("Name Exist: ", ne)
    num_unknown = len(locations)
    to_break = []
    print("To break list and its length: ", to_break, len(to_break))


    # Actual Code to Compare the unkown face from training data (known_faces)
    img_feature = 1
    while(len(to_break) <= num_unknown and img_feature<=10):
        print("img_feature no: ----->", img_feature)
        print("To Break List: ", to_break)
        mycursor.execute("SELECT f" + str(img_feature) + " FROM frs")
        myresult = mycursor.fetchall()
        print(type(myresult), len(myresult))
        print(myresult[0])

        kfaces = []
        for i in range(len(myresult)):
            f = myresult[i]
            flst = re.sub('\s+', ',', f[0])
            farr = np.array(ast.literal_eval(flst))
            kfaces.append(farr)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(kfaces, face_encoding, TOLERANCE)
            match = None
            print(type(results), "--> ", results)

            if True in results:
                  match = ne[results.index(True)]
                  print(f"match found: {match}")
                  # to_break[results.index(True)] = True
                  to_break.append(True)

                  top_left = (face_location[3], face_location[0])
                  bottom_right = (face_location[1], face_location[2]+22)
                  color = [0, 255, 0]
                  cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                  top_left = (face_location[3], face_location[2])
                  bottom_right = (face_location[1], face_location[2])
                  cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                  cv2.putText(image, match, (face_location[3]+10, face_location[2]+15),
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), FONT_THICKNESS)

        img_feature = int(img_feature) + 1

    cv2.imshow("Test image", image)
    cv2.waitKey(0)



start_testing_btn = tk.Button(my_test_frame, text="Start Testing Image", command=testing_data)
start_testing_btn.grid(row=3, column=1)

  # cv2.imshow(filename, image)
  # # cv2_imshow(image)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

#conn.close()
def doSomething():
    conn.close()
    print("Closing connection to database...")
    root.destroy()


root.protocol('WM_DELETE_WINDOW', doSomething)

root.mainloop()