def ReadMeasureFile(path):
    with open(path, "r") as file:
        message = file.read()
    file.close()

    index = 1
    message = message[message.index("# Begin TRACE A Data"):]
    message = message[message.index("P_")+2:message.index("\n\n")]
    # print(message)

    freq = []
    id = []
    mag = []

    while message.find("P_")!= -1:
        string = message[:message.index("P_")]
        id.append(string[:string.index("=")])
        mag.append(string[string.index("=")+1:string.index(" ")])
        aux_freq = string[string.index(" ")+3:string.index("z")+1]
        freq.append(aux_freq[:aux_freq.index(" ")])

        message = message[len(string):]
        message = message[message.index("P_")+2:]

    id.append(message[:message.index("=")])
    mag.append(message[message.index("=")+1:message.index(" ")])
    aux_freq = message[message.index(" ")+3:message.index("z")+1]
    freq.append(aux_freq[:aux_freq.index(" ")])

    # for i in range(len(id)):
    #     print("ID:" + id[i] + " frequencia:" + freq[i] + " MHz" + " Magnitud:" + mag[i])

    id = [float(i) for i in id]
    mag = [float(i) for i in mag]
    freq = [float(i) for i in freq]

    return id, freq, mag
