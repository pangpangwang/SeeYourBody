def link(cBuffer_num):
    data_list = []
    for j in range(20):
        data = cBuffer_num[3 + j * 3] <<16;
        data += cBuffer_num[4 + j * 3] <<8;
        data += cBuffer_num[5 + j * 3];
        data_list.append(data);
    return data_list

def tran(data_list):
    data_list_tran = []
    for data in data_list:
        if data >= 8388608:
            data_tran = 2.4 * (data - 16777215) / 8388607
        elif data < 8388608:
            data_tran = 2.4 * data / 8388607
        data_list_tran.append(data_tran)
    return data_list_tran


def Filtering(data_list, dimension):
    order =  4
    Input_temp = [0] * (order - 1)
    Output_temp = [0] * (order - 1)
    IIR_Coefs = [[0.9970879016782, -2.991263705035, 2.991263705035, -0.9970879016782],
                 [1, -2.994167310674, 2.988351619079, -0.9941842836731]]
    res = []
    for data in data_list:
        y = IIR_Coefs[0][0] * data
        for i in range(dimension)[1:]:
            y += IIR_Coefs[0][i] * Input_temp[i-1] - IIR_Coefs[1][i] * Output_temp[i-1]
        i = dimension - 2
        while i:
            Input_temp[i] = Input_temp[i-1]
            Output_temp[i] = Output_temp[i-1]
            i = i - 1
        Input_temp[0] = data
        Output_temp[0] = y
        res.append(y)
    return res

