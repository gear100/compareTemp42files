import sys
import os

"""
file_1 = sys.argv[1]
file_2 = sys.argv[2]

DEV = sys.argv[3]

PRI = sys.argv[4]   # print more default = N0

COM_ID = sys.argv[5]   # compare only one temp-ID default = N0


if sys.argv[4] == "":
    PRI = False
elif sys.argv[4] == "Yes":
    PRI = True
"""    
#compare only one temp-ID default = N0
#COM_ID=123
COM_ID=""

#print on terminal more information
PRI = True
#PRI = False

# deviation
DEV = 1.0


# files
file_1, file_2 = "temp_1.dat", "temp_2.dat"


print """ \n
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/
_/     compare temperatur devinition in two files
_/           
_/        var:
_/           DEV=<>                 grad difference
_/           PRI=<True/False>       print/no print temperatur per grid witg deff.
_/           COM_ID <>              if number id of tem, thath will be only this id compare
_/
_/      additionale will be check if all grids in file_1/2 have tepmperatur definition
_/
_/
_/                                                    A.Gernat PETT4 12.12.2016
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
\n"""


def fileTempDic(file_1):
    """ create dic with temp_id {grid:temp_grid, ...} """



    if not os.path.exists(file_1):
        sys.stderr.write('ERROR: file not found! ' + file_1)
        sys.exit(1)
    else:
        sys.stdout.write('to compare file: ' + "\n---->" + file_1 + "\n"*3)



    f_1 = open(file_1, "r")
    list_grid = []    
    list_f_1 = []
    list_f_1_gri = []
    dic_f_1 = {}

    while 1:
    
        line = f_1.readline()

    
        if not line:
            break
        else:
            if line.startswith("GRID"):
            
                grid_id =line[8:16].strip() 

                if grid_id not in list_grid:
                    list_grid.append(grid_id)

            if line.startswith("TEMP"):
            
                t_id, grid, tem = line[8:16].strip() , line[16:24].strip() , line[24:32].strip() 
                if grid not in list_f_1_gri:
                    list_f_1_gri.append(grid)
                if t_id not in list_f_1:
                    list_f_1.append(t_id)
                    dic_f_1[t_id] = {grid:tem}

                    if PRI == True:                
                        sys.stdout.write("TEMP ID : " + str(t_id).ljust(8) + " " + file_1 + "\n")
            
                else: dic_f_1[t_id].update({grid:tem})
            
            else:
                pass #print line, "in file: ", file_1

    f_1.close()

    return dic_f_1, list_f_1, list_f_1_gri, list_grid





# dic from two files with tem-grids

temp_f_1 = fileTempDic(file_1)
# dic with all      TEMP-IDs    GRID-from-Temp   GRID-ids
dic_tem_f_1,      tem_id_f_1,   grids_f_1 ,     fem_grids_in_f_1 =   temp_f_1[0] ,temp_f_1[1], temp_f_1[2], temp_f_1[3]

temp_f_2 = fileTempDic(file_2)

dic_tem_f_2,      tem_id_f_2,   grids_f_2,      fem_grids_in_f_2  =  temp_f_2[0] ,temp_f_2[1], temp_f_2[2], temp_f_2[3]


print "# dic with all      TEMP-IDs    GRID-from-Temp   GRID-ids"

print dic_tem_f_1,  "\n",    tem_id_f_1,  "\n",  grids_f_1,    "\n",   fem_grids_in_f_1

print dic_tem_f_2,  "\n",    tem_id_f_2,  "\n",  grids_f_2,    "\n",   fem_grids_in_f_2

print dic_tem_f_1["12"].keys()

print dic_tem_f_2["12"].keys()



# comparison

def checkIn2file(grids_f_1,grids_f_2, file_1, what="bla bla"):
    list_no_temp = []
    if set(grids_f_1).issubset(set(grids_f_2))==False:
        rest_f_1 = set(grids_f_1) - set(grids_f_2)
        list_no_temp = list(rest_f_1)
        csv = ",".join([x for x in list_no_temp])
        sys.stderr.write("[ERO ]" + what + " in file: " + file_1 + "\n----> "  + csv + "\n")
    else:
        pass
     
    return list_no_temp



# check if in files grids number is equal

f_ag = checkIn2file(fem_grids_in_f_1,fem_grids_in_f_2, file_1, what="  more grids ? ")
f_bg = checkIn2file(fem_grids_in_f_2,fem_grids_in_f_1, file_2, what="  more grids ? ")


f_ai = checkIn2file(tem_id_f_1, tem_id_f_2, file_1, what=" other temp IDs ")
f_bi = checkIn2file(tem_id_f_2,tem_id_f_1, file_2, what=" other temp IDs ")

# not to be check

#print "grids-  " ,f_ag, f_bg
#print "temp-ID " ,f_ai, f_bi

inters_g = set(grids_f_1) & set(grids_f_2)
grids_in_2 = list(inters_g )



inters_id = set(tem_id_f_1) & set(tem_id_f_2)
id_in_twoF = list(inters_id )

print id_in_twoF
print grids_in_2


out = open("out.set","w")

out.write("$grid with temp dev <temp1-minus-temp2> " + str(DEV) + "grad" + "\n")


if COM_ID != "" :
    if str(COM_ID) in id_in_twoF:
        id_in_twoF = [str(COM_ID)]
        sys.stderr.write("\n - - - - -    compare only one temp ID: " + str(COM_ID) + " - - - - - -\n")
    else:
        
        sys.stderr.write("[ERO ]temp ID NOT in two files: " + str(COM_ID) + "\n")
        sys.exit(0)

                         
for ID in id_in_twoF:
    for grid in grids_in_2:
        if dic_tem_f_1[ID][grid] and dic_tem_f_2[ID][grid]:
            div = float(dic_tem_f_1[ID][grid]) - float(dic_tem_f_2[ID][grid])

            if PRI==True:
                sys.stdout.write("id-:" + ID.ljust(8) + ":grid-:" + grid.rjust(8) + ";temp_file_1;" + dic_tem_f_1[ID][grid].rjust(8) + ";temp_file_2;" + dic_tem_f_2[ID][grid].rjust(8) + ";   div  = ; " + str(div).rjust(8) + "\n")
            if abs(div) >= abs(DEV):
               
                out.write("SET " + ID + " = " + grid + "\n")
                #out.write("id-:" + ID.ljust(8) + ":grid-:" + grid.rjust(8) + ";temp_file_1;" + dic_tem_f_1[ID][grid].rjust(8) + ";temp_file_2;" + dic_tem_f_2[ID][grid].rjust(8) + ";   div  = ; " + str(div).rjust(8) + "\n")

out.close()




print """
file %s with grids temp dev: ---> %sgrad \n ----- done --- \n\n""" % ("out.set", str(DEV)) 

print """ \n
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/
_/     check if all fem GRID have temperatur definition ?
_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
\n"""


f_ag = checkIn2file(fem_grids_in_f_1,grids_f_1, file_1, what=" fem nodes with/ohne temperatur devinition")
f_bg = checkIn2file(fem_grids_in_f_2,grids_f_2, file_2, what=" fem nodes with/ohne temperatur devinition")

print '''
---> in file: %s number of grids without temperatur devinition:   %s
---> in file: %s number of grids without temperatur devinition:   %s

#--- done\n
''' % (file_1, len(f_ag), file_2, len(f_bg))

sys.stdout.write("end   A. Gernat PETT3 09.01.2016")

