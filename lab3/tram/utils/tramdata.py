import sys
import json
from math import cos, sqrt, pi


# files given
# 
STOP_FILE = './data/tramstops.json'
# 
LINE_FILE = './data/tramlines.txt'


# file to give

TRAM_FILE = './tramnetwork.json'

#-----------------------------------------------------------------------------------------------------------------------------------





def build_tram_stops(jsonobject):
    
    with open(STOP_FILE, "r", encoding='utf-8') as stopfile:           
       jsonobject = json.load(stopfile)       
        
    stop_dic = {}

    
    for i , x in jsonobject.items():
        stop_lat = float(x.get("position")[0])
        stop_long = float(x.get("position")[1])
        format = {"lat": stop_lat, "lon": stop_long}
        stop_dic[i] = format    
    return stop_dic

#print(build_tram_stops(jsonobject)) TEST          
    


#-----------------------------------------------------------------------------------------------------------------------------------




def build_tram_lines(lines): 
    with open(LINE_FILE, "rt", encoding='utf-8') as linefile: 
        lines = linefile.read()   
    tram_lines = {}
    time = {}
    current_line = None
    old = None
    last_stop = None


    for row in lines.splitlines():
        
        
        if row.endswith(':'):
            current_line = row[:-1]
            tram_lines[current_line] = []
            
        elif row.strip(): 
            
            stop = ' '.join(row.split()[:-1])
            tram_lines[current_line].append(stop) #första outputen färdig här dvs, tram_lies dict
            
            
            time_seperated = int(row.split()[-1][-2:]) #börjar med tid dict
       
            
            if old is not None and not old.endswith(':'):
                time_at_old = int(old.split()[-1][-2:])
                duration = abs(time_at_old - time_seperated)

                if stop not in time:
                    time[stop] = {}
                if last_stop is not None and last_stop not in time[stop]:
                    time[stop][last_stop] = duration
                

            last_stop = stop 
        
        old = row
        
    #test_json = json.dumps(time, ensure_ascii=False, indent=1) 
    #print(test_json)
      
    return tram_lines, time

#-----------------------------------------------------------------------------------------------------------------------------------

    

def build_tram_network(stopfile, linefile):
    stops = build_tram_stops(stopfile)
    lines, times = build_tram_lines(linefile)

    tramnetwork = {"stops": stops, "lines": lines, "times": times}
    
    with open(TRAM_FILE, 'w', encoding='utf-8') as tram_network_file:
        json.dump(tramnetwork, tram_network_file, ensure_ascii=False, indent=1)
    
    return tramnetwork

#build_tram_network(stopfile, linefile)
    
    
    

#vill ha på den formen #{"stops": {"Östra Sjukhuset": {"lat": 57.7224618,"lon": 12.0478166},   and so on, the entire stop dict} }, "lines": {"1": ["Östra Sjukhuset","Tingvallsvägen", and so on, all stops on line 1],   and so on, the entire line dict},"times": {"Tingvallsvägen": {"Kaggeledstorget": 2 },   and so on, the entire time dict }}


#-----------------------------------------------------------------------------------------------------------------------------------





def lines_via_stop(linedict, stop):
    lines_via_stop = []

    for line, stops in linedict.items():
        if stop in stops:
            lines_via_stop.append(line)

    lines_via_stop.sort(key=lambda x: int(x))

    return lines_via_stop

#dictionary, time = build_tram_lines(lines) #test

#stoplines = lines_via_stop(linedict=dictionary, stop='Chalmers') #test
#print(stoplines) #test


 #-----------------------------------------------------------------------------------------------------------------------------------
 
 
 
def lines_between_stops(linedict, stop1, stop2):
    lines_between_stops = []

    for line, stops in linedict.items():
        if stop1 in stops and stop2 in stops:
            lines_between_stops.append(line)

    # här sorterar vi i order
    lines_between_stops.sort(key=lambda x: int(x))

    return lines_between_stops

#dictionary, time = build_tram_lines(lines) #test
#stoplines = lines_between_stops(dictionary, 'Centralstationen', 'Chalmers') #test
#print(stoplines) #test


#---------------------------------------------------------------------------------------------------------------------------------------
    
def time_between_stops(linedict, timedict, line, stop1, stop2):
    if line not in linedict or stop1 not in linedict[line] or stop2 not in linedict[line]:
        return False

    stops_on_line = linedict[line]
    start_index = stops_on_line.index(stop1)
    end_index = stops_on_line.index(stop2)
    
    time = 0

    if start_index == end_index:
        return time

    elif start_index < end_index:
        stops_between_values = stops_on_line[start_index: end_index + 1]
    else:
        stops_between_values = stops_on_line[end_index: start_index + 1]

    for indx in range(len(stops_between_values) - 1):
        current_stop = stops_between_values[indx]
        next_stop = stops_between_values[indx + 1]

        if current_stop in timedict and next_stop in timedict[current_stop]:
            time += timedict[current_stop][next_stop]
        else:
            time += timedict[next_stop][current_stop]

    return time
    # if line not in linedict:
    #     return "Line not found"

    # stops_on_line = linedict[line]
    # if stop1 not in stops_on_line or stop2 not in stops_on_line:
    #     return "Stops not on the line"

    # stops = linedict[line]

    # if stops.index(stop1) > stops.index(stop2):
    #     stop1, stop2 = stop2, stop1

    # total_time = 0
    # current_stop = stop1
    
    # #_______________________
    # while current_stop != stop2:
    #     next_stop = stops[stops.index(current_stop) + 1]
    #     total_time += timedict[current_stop][next_stop]
    #     current_stop = next_stop

    # return total_time
    #________________________________
# line_check = '10' #test
# stop1_check = 'Chalmers' #test
# stop2_check = 'Centralstationen' #test
# dictionary, time = build_tram_lines(lines) #test
# time_between = time_between_stops(dictionary, time, line_check, stop1_check, stop2_check) #test

# print(f"Time between {stop1_check} and {stop2_check} on line {line_check}: {time_between} minutes") #test


#---------------------------------------------------------------------------------------------------------------------------------------
    
def distance_between_stops(stopdict, stop1, stop2):
    #formel från wikipedia:
    
    radius = 6371.0  
    lat_stop1 = stopdict[stop1]['lat'] * pi/180
    lon_stop1 = stopdict[stop1]['lon'] * pi/180
    lat_stop2 = stopdict[stop2]['lat'] * pi/180
    lon_stop2 = stopdict[stop2]['lon'] * pi/180
    lat_diff = lat_stop2 - lat_stop1
    lon_diff = lon_stop2 - lon_stop1
    middle_lat = (lat_stop1 + lat_stop2) / 2
    
    distance = radius* sqrt(lat_diff**2 + (cos(middle_lat) * lon_diff) **2 )
    
    return distance


#test = build_tram_stops(jsonobject) #test
#mjau = distance_between_stops(test, 'Östra Sjukhuset', 'Centralstationen') #test
#print(mjau) #test
 
 
#---------------------------------------------------------------------------------------------------------------------------------------


def answer_query(tramdict, query):
    
    # with open(TRAM_FILE, 'r', encoding='utf-8') as json_file:
    #     network = json.load(json_file)

    split_query = query.split()

    word_one = split_query[0].lower()
    
    if word_one == 'via':
        stop = query.lstrip('via ')   
        return lines_via_stop(tramdict['lines'], stop)
    
    
    elif word_one == 'between':
        stop = query.lstrip("between ").rsplit(" and ")
        return lines_between_stops(tramdict['lines'], stop[0], stop[1])
    

    elif word_one == 'time':
        line = query.lstrip("time with").rsplit(" from ")
        stop = line[1].rsplit(" to ")
        return time_between_stops(tramdict['lines'], tramdict['times'], line[0], stop[0], stop[1])

    elif word_one == 'distance':
        stop = query.lstrip("distance from ").rsplit(" to ")
        return distance_between_stops(tramdict['stops'], stop[0], stop[1])
    
    elif word_one == 'quit':
        return "Terminating the program"


    else:
        False
      

   
   
#---------------------------------------------------------------------------------------------------------------------------------------
   
def dialogue(tramfile=TRAM_FILE):
    with open(TRAM_FILE, 'r', encoding='utf-8') as json_file:
       tramdict = json.load(json_file)
       
    while True:
        query = input('> ')
        if query.lower() == 'quit':
            break

        if any(keyword in query for keyword in ['via', 'between', 'time', 'distance']):
            answer = answer_query(TRAM_FILE, query)
            print(answer if answer else 'Unknown argument')
        else:
            print('Sorry, try again')




if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE, LINE_FILE)
    else:
        dialogue(TRAM_FILE)