import os
import matplotlib
import matplotlib.pyplot as plt

def ReadFile(path):
    with open(path, "r") as file:
        message = file.read()
    file.close()

    index = 1
    message = message[message.index("# Begin TRACE A Data"):]
    message = message[message.index("P_")+2:message.index("\n\n")]
    # print(message)

    frec = []
    id = []
    mag = []

    while message.find("P_")!= -1:
        string = message[:message.index("P_")]
        id.append(string[:string.index("=")])
        mag.append(string[string.index("=")+1:string.index(" ")])
        aux_frec = string[string.index(" ")+3:string.index("z")+1]
        frec.append(aux_frec[:aux_frec.index(" ")])

        message = message[len(string):]
        message = message[message.index("P_")+2:]

    id.append(message[:message.index("=")])
    mag.append(message[message.index("=")+1:message.index(" ")])
    aux_frec = message[message.index(" ")+3:message.index("z")+1]
    frec.append(aux_frec[:aux_frec.index(" ")])

    # for i in range(len(id)):
    #     print("ID:" + id[i] + " Frecuencia:" + frec[i] + " MHz" + " Magnitud:" + mag[i])

    id = [float(i) for i in id]
    mag = [float(i) for i in mag]
    frec = [float(i) for i in frec]

    return id, frec, mag

def main():
    dirpath = os.getcwd()
    id, frec, mag = ReadFile(dirpath + "/DROP_FILES_HERE/FileName.spa")

    # for i in range(len(id)):
    #     print("ID:" + id[i] + " Frecuencia:" + frec[i] + " MHz" + " Magnitud:" + mag[i])
    fig, ax = plt.subplots()
    ax.plot(frec, mag)

    ax.set(xlabel='frec [MHz]', ylabel='Amplitude [dB]',
           title='Simple plot')
    ax.grid()

    # fig.savefig("test.png")
    plt.show()



if __name__ == '__main__':
    main()
