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
_/           PRI=<True/False>       print/no print temperatur per grid on terminal
_/           COM_ID <>              compare only one temp-ID
_/
_/      additionale will be check if all grids in file_1/2 have tepmperatur definition
_/
_/
_/                                                    A.Gernat PETT3 12.12.2016
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


print """
# find ID-TEMP to check ID of temp check
#    ID_of_Temp_to_compare
#
#   print info ii errors
#
#
 """

if len(set(tem_id_f_1) & set(tem_id_f_2))  == 0 :
        sys.stderr.write("     no ID of temp to compare , diif. ID in two files\n   ------- this is the END\n\n")
        sys.exit(0)    


ID_of_Temp_to_compare  = set(tem_id_f_1) & set(tem_id_f_2)
ID_more_in_file_1 = set(tem_id_f_1)  - ID_of_Temp_to_compare 
ID_more_in_file_2 =set(tem_id_f_2) - ID_of_Temp_to_compare


print "ID-of-Temp-to-compare   ", ";".join([x for x in list(ID_of_Temp_to_compare )])


# print info about IDs
if len(ID_more_in_file_1) !=0:
    sys.stderr.write( "ID_more_in_file_1        " +  str(len(ID_more_in_file_1)) + " " +  "  ;".join([str(x) for x in list(ID_more_in_file_1) ]) + "\n\n")

if len(ID_more_in_file_2) !=0:
    sys.stderr.write( "ID_more_in_file_2        " +  str(len(ID_more_in_file_2)) + " " +  "  ;".join([str(x) for x in list(ID_more_in_file_2) ]) + "\n\n")

if len(ID_more_in_file_1) == 0 and len(ID_more_in_file_2) == 0:
    sys.stdout.write( "\n-------------> in two file ID-tem are identical :)\n\n")



out = open("sys.out", "w")
outErr = open("Errors-sys.out", "w")
out.write("$sets of grids from file: " + file_1 + "  " + file_2 + ": with diverence of temp = "  + str(DEV) + " grad\n")
# compare ID
for ID in ID_of_Temp_to_compare:
    sys.stdout.write( "--------------------------------------------"   +  "\n" +  " check ID :   " +  ID   + "\n")

    # check grids in two files per ID
    # grids group per ID-TEMP
    grids_f_1 =  dic_tem_f_1[ID].keys()
    grids_f_2 =  dic_tem_f_2[ID].keys()
    
    grids_ID_of_Temp_to_compare  = set(grids_f_1) & set(grids_f_2)
    grids_ID_more_in_file_1      = set(grids_f_1)  - grids_ID_of_Temp_to_compare 
    grids_ID_more_in_file_2      = set(grids_f_2) -  grids_ID_of_Temp_to_compare



    # print info about IDs
    #ID of erroer +900000+ID
    if len(grids_ID_more_in_file_1) !=0:
        sys.stderr.write( "grids_ID with temperatur only in file_1        " +  str(len(grids_ID_more_in_file_1)) + "grid(s);   \nSET " + str(int(900000)+int(ID)) + "=" +  "  ;".join([str(x) for x in list(grids_ID_more_in_file_1) ]) + "\n\n")
        outErr.write( "$grids_ID with temperatur only in file_1        " +  str(len(grids_ID_more_in_file_1)) + "grid(s);   \nSET " + str(int(900000)+int(ID)) + "=" +  "  ;".join([str(x) for x in list(grids_ID_more_in_file_1) ]) + "\n\n")

    if len(grids_ID_more_in_file_2) !=0:
       sys.stderr.write( "grids_ID with temperatur only in file_2        " +  str(len(grids_ID_more_in_file_2)) + "grid(s);   SET " + str(int(900000)+int(ID)) + "=" +  "  ;".join([str(x) for x in list(grids_ID_more_in_file_2) ]) + "\n\n")
       outErr.write( "$grids_ID with temperatur only in file_2        " +  str(len(grids_ID_more_in_file_2)) + "grid(s);   \nSET " + str(int(900000)+int(ID)) + "=" +  "  ;".join([str(x) for x in list(grids_ID_more_in_file_2) ]) + "\n\n")

    if len(grids_ID_more_in_file_1) == 0 and len(grids_ID_more_in_file_2) == 0:
        sys.stdout.write( "\n-------------> in two file ID-GRIDS-from-TEMP-cards are identical :)\n\n")


    sys.stdout.write("\n---------------------------------" + "Beginn to compate temperature difference <DEV> for ID of TEMP card\n")

    print "DEV = " , DEV
    
    print "ID =  " , ID

    

    for GRI in grids_ID_of_Temp_to_compare:

        
        # grids group per ID-TEMP
        temp_grids_f_1 =  dic_tem_f_1[ID][GRI]
        temp_grids_f_2 =  dic_tem_f_2[ID][GRI]

        div = float(temp_grids_f_1)-float(temp_grids_f_2)

        # print if
        if PRI==True:
            #pass
            print "GRID  ;  ", GRI.rjust(8), "; file_1 temp ; " , temp_grids_f_1.rjust(8),  "; file_2 temp ; " , temp_grids_f_2.rjust(8), " ; div = tem_fil_1 minus tem_fil_2 ; ", div, " ; " , DEV

        # save grids with div < DEV
        if abs(div ) >= abs(DEV):
            #print "SET " , ID , " = ", GRI , ",\n"
            #sys.stdout.write("SET " + ID + " = " + GRI + ",\n")
            out.write("SET " + ID + " = " + GRI + ",\n")






outErr.close()
out.close()
sys.stdout.write("\n")
sys.stdout.write("------------------------------ end of checks ID --------------\n")
sys.stdout.write("in output file: sys.out patran set with grid that have difference of temperatu=" + str(DEV) + "\n")
sys.stdout.write("file with errore:     Errors-sys.out")
sys.stdout.write("end   A. Gernat PETT3 09.01.2016")

