import csv as csv_import
import operator
import os

print type(csv_import)

in_dir = '/home/sbasu/Videopedia_MM/all_plsi'
out_dir = '/home/sbasu/Videopedia_MM/sortedPLSA'
csvs = [
    (os.path.join(in_dir, csv), 
        os.path.join(out_dir, csv))
    for csv in os.listdir(in_dir) 
    if csv.endswith('.csv')
    ]

##for i in csvs:
##    print(i)



def sort_by_column(csv_cont, col, reverse=False):
    """ 
    Sorts CSV contents by column name (if col argument is type <str>) 
    or column index (if col argument is type <int>). 
    
    """
    header = csv_cont[0]
    print header
    body = csv_cont[1:]
    #print body
    if isinstance(col, str):  
        col_index = header.index(col)
    else:
        col_index = col
    body = sorted(body, 
           key=operator.itemgetter(col_index), 
           reverse=reverse)
    body.insert(0, header)
    return body

def print_csv(csv_content):
    """ Prints CSV file to standard output."""
    print(50*'-')
    for row in csv_content:
        row = [str(e) for e in row]
        print('\t'.join(row))
    print(50*'-')

def write_csv(dest, csv_cont):
    """ Writes a comma-delimited CSV file. """

    with open(dest, 'w') as out_file:
        writer = csv_import.writer(out_file, delimiter=',')
        for row in csv_cont:
            writer.writerow(row)



def convert_cells_to_floats(csv_cont):
    """ 
    Converts cells to floats if possible
    (modifies input CSV content list).
    
    """
    for row in range(len(csv_cont)):
        for cell in range(len(csv_cont[row])):
            try:
                csv_cont[row][cell] = float(csv_cont[row][cell])
            except ValueError:
                pass 

def csv_to_list(csv_file, delimiter=','):
    """ 
    Reads in a CSV file and returns the contents as list,
    where every row is stored as a sublist, and each element
    in the sublist represents 1 cell in the table.
    
    """
    filename = ''.join(csv_file[0:])
    with open(filename, 'r') as csv_con:
        print type(csv_con)
        print csv_con
        print type(csv_import)
        reader = csv_import.reader(csv_con, delimiter=delimiter)
        return list(reader)

def process_csv(csv_in, csv_out):
    """ 
    Takes an input- and output-filename of an CSV file
    and marks minimum values for every column.
    
    """
    csv_cont = csv_to_list(csv_in)
    #csv_marked = copy.deepcopy(csv_cont)
    convert_cells_to_floats(csv_cont)
    csv_sorted = sort_by_column(csv_cont, ' KL ')
    #mark_all_col(csv_marked, mark_max=False, marker='*')
    write_csv(csv_out, csv_sorted)

    
##csv_cont = csv_to_list('/home/sbasu/VideoClustering/all_ldas/all_ldas0A45kt2U3U8_words.txt_topics.txt.csv')
##
####print('first 3 rows:')
####for row in range(3):
####    print(csv_cont[row])
##
####csv_cont = csv_to_list('../Data/test.csv')
####
####print('\n\nOriginal CSV file:')
####print_csv(csv_cont)
##
##print('\n\nCSV sorted by column "KL":')
##convert_cells_to_floats(csv_cont)
##csv_sorted = sort_by_column(csv_cont, ' KL ')
##print_csv(csv_sorted)
##
##
####csv_cont = csv_to_list('../Data/test_marked.csv')
##
##write_csv('/home/sbasu/VideoClustering/sortedKLCSV/test_marked.csv', csv_sorted)
##
##print('\n\nWritten CSV file:')

for inout in csvs:
    print inout[0]
    print inout[1]
    process_csv(inout[0], inout[1])
