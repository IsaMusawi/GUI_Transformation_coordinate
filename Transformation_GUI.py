import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Parameter as par

root = tk.Tk()
root.geometry("1000x1000")
root.title("TRANSFORMASI KOORDINATE DARI LOKAL SITE KE UTM")
root.pack_propagate(False)
root.resizable(0, 0)

labelFile = ttk.Label(root, text="No File Selected")


def fileLoad():
    global v
    fileName = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetype=(("csv files", "*.csv"),("All Files", "*.*")))
    print(fileName)
    v.set(fileName)
    labelFile["text"] = fileName


def loadData():
    global dataLoad
    filePath = labelFile["text"]
    try:
        csv_data = r"{}".format(filePath)
        dataLoad = pd.read_csv(csv_data)
        dataLoad.columns = ['No', 'Easting', 'Northing', 'Elevation', 'Remarks']
        return dataLoad
    except:
        tk.messagebox.showerror("Error", "Please choose the correct data")

#----------- Menu dialog ----------
menuFrame = tk.LabelFrame(root, text="MENU")
menuFrame.place(height=110, width=450, rely=0.0, relx=0.03)
# ---------------- Menu Button
tk.Label(menuFrame, text='File Path').grid(row=0, column=0, padx=10, pady=5)
v = tk.StringVar()
entry = tk.Entry(menuFrame, textvariable=v).grid(row=0, column=1, columnspan=4)
openButton = tk.Button(menuFrame, text='BROWSE DATA',command=lambda : fileLoad())
openButton.grid(row=1, column=0, padx=10, pady=5)
procesButton = tk.Button(menuFrame, text='PROCESS',command=lambda : procesStart())
procesButton.grid(row=1, column=2, padx=10, pady=5)
saveButton = tk.Button(menuFrame, text='SAVE DATA',command=lambda : SaveFile())
saveButton.grid(row=1, column=3, padx=10, pady=5)


# ----------- Choice dialog -----------
choiceFrame = tk.LabelFrame(root, text="Transformation Choice")
choiceFrame.place(height=100, width=450, rely=0.12, relx=0.03)
# ---------------- Choice Button
choiceVar = tk.StringVar()
choiceVar.set("l")
choiceOne = ttk.Radiobutton(choiceFrame, text='TRANSFORMATION FROM LOCAL SITE TO UTM', value="l", variable=choiceVar)
choiceOne.place(rely=0.1, relx=0.1)
choiceTwo = ttk.Radiobutton(choiceFrame, text='TRANSFORMATION FROM UTM TO LOCAL SITE', value="u", variable=choiceVar)
choiceTwo.place(rely=0.55, relx=0.1)


#Frame Treeview 1 (data input)
inputFrame = tk.LabelFrame(root, text="Data Input")
inputFrame.place(height=350, width=500, rely=0.60, relx=0)
# Treeview data input
inputTreeview = ttk.Treeview(inputFrame)
inputTreeview.place(relheight=1, relwidth=1)
treescrollyInput = tk.Scrollbar(inputFrame, orient="vertical", command=inputTreeview.yview)
treescrollxInput = tk.Scrollbar(inputFrame, orient="horizontal", command=inputTreeview.xview)
inputTreeview.configure(xscrollcommand=treescrollxInput.set, yscrollcommand=treescrollyInput.set)
treescrollxInput.pack(side="bottom", fill="x")
treescrollyInput.pack(side="right", fill="y")

#Frame Treeview 2 (Hasil Transformasi)
transFrame = tk.LabelFrame(root, text="Hasil Transformasi")
transFrame.place(height=350, width=500, rely=0.60, relx=0.5)
# Treeview transformasi
transTreeview = ttk.Treeview(transFrame)
transTreeview.place(relheight=1, relwidth=1)
treescrollyTrans = tk.Scrollbar(transFrame, orient="vertical", command=transTreeview.yview)
treescrollxTrans = tk.Scrollbar(transFrame, orient="horizontal", command=transTreeview.xview)
transTreeview.configure(xscrollcommand=treescrollxTrans.set, yscrollcommand=treescrollyTrans.set)
treescrollxTrans.pack(side="bottom", fill="x")
treescrollyTrans.pack(side="right", fill="y")

#Frame Treeview 3 (Deviasi Jarak)
devFrame = tk.LabelFrame(root, text="Deviasi Perbandingan distorsi antara jarak dan koordinat")
devFrame.place(height=200, width=500, rely=0.40, relx=0.5)
# Treeview transformasi
devTreeview = ttk.Treeview(devFrame)
devTreeview.place(relheight=1, relwidth=1)
treescrollyDev = tk.Scrollbar(devFrame, orient="vertical", command=devTreeview.yview)
treescrollxDev = tk.Scrollbar(devFrame, orient="horizontal", command=devTreeview.xview)
devTreeview.configure(xscrollcommand=treescrollxDev.set, yscrollcommand=treescrollyDev.set)
treescrollxDev.pack(side="bottom", fill="x")
treescrollyDev.pack(side="right", fill="y")


#Frame Figure
figureFrame = tk.LabelFrame(root, text="Plotting")
figureFrame.place(height=400, width=500, rely=0.0, relx=0.5)


#Frame resume
resumeFrame = tk.LabelFrame(root, text="RESUME PENGOLAHAN DATA")
resumeFrame.place(height=380, width=450, rely=0.22, relx=0.03)

dC = tk.IntVar()
dataCountText = tk.Label(resumeFrame, text=" Total data adalah                                         ||   ")
dataCountText.grid(column=0, row=0)
dataCount = tk.Label(resumeFrame, textvariable=dC)
dataCount.grid(column=1, row=0)

dfC = tk.IntVar()
datafilterCountText = tk.Label(resumeFrame, text=" Total data setelah di bersihkan                    ||   ")
datafilterCountText.grid(column=0, row=1)
datafilterCount = tk.Label(resumeFrame, textvariable=dfC)
datafilterCount.grid(column=1, row=1)

NArE = tk.IntVar()
naRowText = tk.Label(resumeFrame, text=" Total data NA di kolom Easting                   ||   ")
naRowText.grid(column=0, row=2)
naRow = tk.Label(resumeFrame, textvariable=NArE)
naRow.grid(column=1, row=2)

NArN = tk.IntVar()
naRowText = tk.Label(resumeFrame, text=" Total data NA di kolom Northing                ||   ")
naRowText.grid(column=0, row=3)
naRow = tk.Label(resumeFrame, textvariable=NArN)
naRow.grid(column=1, row=3)

separator = tk.Label(resumeFrame, text="\n< == Perbandingan Nilai Distorsi Jarak dan Koordinat  == > ")
separator.grid(column=0, row=4, columnspan=2)

dCount = tk.IntVar()
dCounttext = tk.Label(resumeFrame, text=" Total data                                                 || ")
dCounttext.grid(column=0, row=5)
dataCountDev = tk.Label(resumeFrame, textvariable=dCount)
dataCountDev.grid(column=1, row=5)

dMax = tk.IntVar()
dMaxtext = tk.Label(resumeFrame, text=" Deviasi maksimum                                   || ")
dMaxtext.grid(column=0, row=6)
dataMax = tk.Label(resumeFrame, textvariable=dMax)
dataMax.grid(column=1, row=6)

dMin = tk.IntVar()
dMintext = tk.Label(resumeFrame, text=" Deviasi minimum                                     || ")
dMintext.grid(column=0, row=7)
dataMin = tk.Label(resumeFrame, textvariable=dMin)
dataMin.grid(column=1, row=7)

dMean = tk.IntVar()
dMeantext = tk.Label(resumeFrame, text=" Rata-rata deviasi                                      || ")
dMeantext.grid(column=0, row=8)
dataMean = tk.Label(resumeFrame, textvariable=dMean)
dataMean.grid(column=1, row=8)

dStd = tk.IntVar()
dStdtext = tk.Label(resumeFrame, text=" Simpangan Baku deviasi                          || ")
dStdtext.grid(column=0, row=9)
dataStd = tk.Label(resumeFrame, textvariable=dStd)
dataStd.grid(column=1, row=9)

devCount = tk.IntVar()
devCounttext = tk.Label(resumeFrame, text=" Data diluar batas Toleransi                      || ")
devCounttext.grid(column=0, row=10)
devCountn = tk.Label(resumeFrame, textvariable=devCount)
devCountn.grid(column=1, row=10)

fCount = tk.IntVar()
fCounttext = tk.Label(resumeFrame, text=" Data index awal dan akhir berbeda        || ")
fCounttext.grid(column=0, row=10)
fCountn = tk.Label(resumeFrame, textvariable=fCount)
fCountn.grid(column=1, row=10)

def processing():
    global data_count, na_rowE, na_rowN, data_filter_count
    print(choiceVar.get())
    choice = choiceVar.get()

    if choice == "l":
        parTrans = par.L2U()
    elif choice == "u":
        parTrans = par.U2L()

    data_init = loadData()
    data_init.replace('na', np.nan, inplace=True)
    data_init.replace('N/A', np.nan, inplace=True)
    data_init.replace('#Value', np.nan, inplace=True)
    data_count = data_init['No'].count()
    data = data_init.drop_duplicates()
    na_rowE = data['Easting'].isna().sum()
    na_rowN = data['Northing'].isna().sum()
    # print(f"\nTotal data with na is: \n{na_row}")
    data = data.dropna()
    data['Easting'] = data['Easting'].astype(float)
    data['Northing'] = data['Northing'].astype(float)
    data = data[(data['Easting'] > 796000.0) | (data['Easting'] < 808500)]
    data_filter_count = data['No'].count()
    print(f"\nTotal data is {data_count}")
    print(f"\nTotal data removed is {data_count - data_filter_count}")

    data_trans = []

    class dataInit:
        def __init__(self, dataInput, minLimit, maxLimit, Parameter):
            self.data = dataInput
            self.ll = minLimit
            self.lr = maxLimit
            self.prm = Parameter

        def transf(self):
            for index, row in self.data.iterrows():
                if (self.data['Easting'][index] >= self.ll) and (
                        self.data['Easting'][index] < self.lr):  # Transformation in middlestream
                    E = data['Easting'][index]
                    N = data['Northing'][index]
                    A1 = [E, N, 0, 0, 1, 0]
                    A2 = [0, 0, E, N, 0, 1]
                    A = [A1, A2]
                    Ad = pd.DataFrame(A)
                    F = np.dot(Ad, self.prm)
                    fdf = pd.DataFrame(F)
                    trans = [self.data['No'][index], round(fdf[0][0], 3), round(fdf[0][1], 3),
                             round(data['Elevation'][index], 3), self.data['Remarks'][index]]
                    tf = pd.DataFrame(trans).T
                    tf.index = [index]
                else:
                    trans = [np.nan, np.nan, np.nan, np.nan, np.nan]
                    tf = pd.DataFrame(trans).T
                    tf.index = [index]
                data_trans.append(tf)
            data_concat = pd.concat(data_trans)
            return data_concat

    xd = parTrans.Xd()
    xm = parTrans.Xm()
    xu = parTrans.Xu()

    dataUp = dataInit(data, 796000.0, 800600.0, xu)
    dataUp.transf()
    dataMiddle = dataInit(data, 800600.0, 803500.0, xm)
    dataMiddle.transf()
    dataDown = dataInit(data, 803500.0, 808500.0, xd)
    dataMerge = dataDown.transf().dropna()
    dataMerge.sort_index(inplace=True)
    dataMerge.columns = ['No', 'Easting', 'Northing', 'Elevation', 'Remarks']
    return data_init, data, dataMerge


def procesStart():
    global dC, NArE, dfC, dInit, dCount, dMax, dMin, dMean, dStd, devCount, fCount
    data_init, data, dataMerge = processing()
    NArE.set(na_rowE)
    NArN.set(na_rowN)
    dC.set(data_count)
    dfC.set(data_filter_count)

    data_comp = data
    data_comp['No_T'] = dataMerge['No']
    data_comp['Easting_T'] = dataMerge['Easting']
    data_comp['Northing_T'] = dataMerge['Northing']
    data_comp['Elevation_T'] = dataMerge['Elevation']
    data_comp['Remarks_T'] = dataMerge['Remarks']

    # Quality control data
    data_comp['Check_no'] = np.where(data_comp['No'] == data_comp['No_T'], True, False)
    data_comp['Check_Easting'] = np.where(data_comp['Easting'] == data_comp['Easting_T'], 0, data_comp['Easting'] - data_comp['Easting_T'])
    data_comp['Check_Northing'] = np.where(data_comp['Northing'] == data_comp['Northing_T'], 0, data_comp['Northing'] - data_comp['Northing_T'])
    data_comp['Check_Elevation'] = np.where(data_comp['Elevation'] == data_comp['Elevation_T'], 0, data_comp['Elevation'] - data_comp['Elevation_T'])
    data_comp['Check_Remarks'] = np.where(data_comp['Remarks'] == data_comp['Remarks_T'], True, False)
    data_comp['Distance'] = (((data_comp['Easting'] - 806842.970)**2) + ((data_comp['Northing'] - 9755607.709)**2))**0.5
    data_comp['dev_t'] = (((data_comp['Check_Easting'])**2) + ((data_comp['Check_Northing'])**2))**0.5
    data_comp['S_dist'] = np.multiply(data_comp['Distance'],
                                              [1 * 0.0007290161672 if dv > 803500.0 else 1 * 0.000585044212 if dv < 800600.0 else 1 * .00070122909528 for dv in data_comp['Easting_T']])

    # Calculated descriptive statistic
    data_comp['dev_t'] = data_comp['dev_t'].astype(float).round(decimals=3)
    data_comp['S_dist'] = data_comp['S_dist'].astype(float).round(decimals=3)
    data_comp['dev_d'] = data_comp['dev_t'] - data_comp['S_dist']
    data_comp['dev_d'] = data_comp['dev_d'].astype(float).round(decimals=3)
    data_show = data_comp[['No','dev_t', 'S_dist', 'dev_d', 'Check_Remarks', 'Remarks_T']]
    falseCount = data_comp[data_comp['Check_no'] == False].count()['Check_Remarks']
    fCount.set(falseCount)
    desc_count = round(data_comp['dev_d'].count(), 3)
    dCount.set(desc_count)
    desc_max = round(data_comp['dev_d'].max(), 3)
    dMax.set(desc_max)
    desc_min = round(data_comp['dev_d'].min(), 3)
    dMin.set(desc_min)
    desc_mean = round(data_comp['dev_d'].mean(), 3)
    dMean.set(desc_mean)
    desc_std = round(data_comp['dev_d'].std(), 3)
    dStd.set(desc_std)
    dist_not_ok = data_show[(data_show['dev_d'] < -0.155) | (data_show['dev_d'] > 0.155)]
    dev_count = dist_not_ok['No'].count()
    devCount.set(dev_count)
    dist_not_ok.columns = ['No', 'Selisih Koordinat', 'Jarak x faktor skala', 'Deviasi', 'Cek Pengurutan', 'Remarks']

    # Plotting to compared distortion between coordinate and distance
    figure = plt.Figure(figsize=(5,5), dpi=100)
    ax = figure.add_subplot(111)
    ax.scatter(data_comp['Distance'], data_comp['dev_t'], marker="s", color='red', label='Distortion from coordinate')
    ax.scatter(data_comp['Distance'], data_comp['S_dist'], marker="o",color='blue', label='Distortion from distance')
    scatter = FigureCanvasTkAgg(figure, figureFrame)
    scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax.set_xlabel('Distance', fontsize=10)
    ax.set_ylabel('Deviation', fontsize=10)
    ax.set_title('Comparing distortion from coordinate and distance', fontsize=12)
    ax.legend()

    clearData()
    #Treeview Input
    inputTreeview["column"] = list(data_init.columns)
    inputTreeview["show"] = "headings"
    for column in inputTreeview["column"]:
        inputTreeview.heading(column, text=column)

    data_init_row = data_init.to_numpy().tolist()
    for row in data_init_row:
        inputTreeview.insert("", "end", values=row)

    #Treeview Transformasi
    transTreeview["column"] = list(dataMerge.columns)
    transTreeview["show"] = "headings"
    for columnT in transTreeview["column"]:
        transTreeview.heading(columnT, text=columnT)

    dataMerge_row = dataMerge.to_numpy().tolist()
    for rowT in dataMerge_row:
        transTreeview.insert("", "end", values=rowT)

    #Treeview Transformasi
    devTreeview["column"] = list(dist_not_ok.columns)
    devTreeview["show"] = "headings"
    for columnD in devTreeview["column"]:
        devTreeview.heading(columnD, text=columnD)

    distNotOK_row = dist_not_ok.to_numpy().tolist()
    for rowD in distNotOK_row:
        devTreeview.insert("", "end", values=rowD)

def clearData():
    inputTreeview.delete(*inputTreeview.get_children())
    transTreeview.delete(*transTreeview.get_children())

def SaveFile():
    data_init, data, dataMerge = processing()
    extension = [("csv file(*.csv)","*.csv"), ('All tyes(*.*)', '*.*')]
    SAVING_PATH = filedialog.asksaveasfile(mode='w',filetypes=extension, defaultextension=extension)
    dataMerge.to_csv(SAVING_PATH, index=False, line_terminator="\n")

root.mainloop()