import calendar

A = calendar.monthrange(2022,11)
print(A)

current_calendar = calendar.Calendar()

B = current_calendar.monthdayscalendar(2022,11)
print(B, len(B))

from random import choices
from collections import deque
total_len = 7 * len(B)
child_attendance = deque(choices(['x',''],k=A[1]),maxlen=total_len)
print(child_attendance)

child_attendance.extend(['']*A[0])
print(len(child_attendance))
child_attendance.extendleft(['']*(7*len(B)))
print(len(child_attendance))

child_data = {
        'Asier': {
            'comedor': choices(['x',''],k=A[1]),
            'judo': choices(['x',''],k=A[1])
        },
        'Mike': {
            'comedor': choices(['x',''],k=A[1]),
            'judo': choices(['x',''],k=A[1])
        }
}
print(child_data,'\n')

for child,activities in child_data.items():
    print(activities.values())

print('################################################\n\n\n')
from pylatex import NoEscape, TextColor
from pylatex.utils import dumps_list
from functools import partial
import numpy as np
from json import loads as jloads
import os
from itertools import chain

EXTRAESCOLARES = jloads(os.getenv('EXTRAESCOLARES',
                                 '{"JUDO": 25, "CIENCIA": 20, "TEATRO": 20, "ROBOTIX": 20}'))
ACTIVIDADES_ESCOLARES = ['COLEGIO', 'ATENCIÓN TEMPRANA', 'COMEDOR']
ACTIVIDADES = ACTIVIDADES_ESCOLARES
ACTIVIDADES.extend(EXTRAESCOLARES.keys())
COLORS = ["black", "blue", "brown", "cyan", "darkgray", "gray",
          "green", "lightgray", "lime", "magenta", "olive", "orange",
          "pink", "purple", "red", "teal", "violet", "white", "yellow"]
assign_colors = dict(zip(ACTIVIDADES,COLORS))


init_attendance = ['']*A[0]
final_attendance = ['']*(7*len(B)-sum(A))


child_attendance_rows = {}
for child, activities_dict in child_data.items():
    # from operator import itemgetter
    # itemgetter(*[x.upper() for x in activities_dict.keys()])(assign_colors)
    assigned_colors = [assign_colors[x.upper()] for x in activities_dict.keys()]
#     # array_child = [' '.join(list(map(NoEscape,
#                                     # map(partial(TextColor,
#                                                 # assign_colors[activity.upper()]),
#                                         # assistance)))) 
#     [print(activity)                for activity,assistance in zip(*activities_dict.items())]
    
#     child_attendance_rows[child] = np.array(array_child).reshape()
    print(f'{child = }: \n{activities_dict = }')
    print(f'{list(activities_dict.keys()) = }')
    print(f'{list(activities_dict.values()) = }')
    array=[]
    
    D = list(chain(init_attendance,[list(map(TextColor,*(assigned_colors,daily_attendance))) for 
         daily_attendance in zip(*activities_dict.values())],final_attendance))
    print(D,sep='\n')

E = [np.reshape(list(chain(init_attendance,[list(map(TextColor,*(assigned_colors,daily_attendance))) for 
         daily_attendance in zip(*activities_dict.values())],final_attendance)),(len(B),7)) for activities_dict in child_data.values()]
print('\n\n\n')
print(*E,sep='\n')
print(len(E[0]))
F = dict(zip(child_data.keys(),E))
print(F)
    # for activity in zip([activities_dict.keys()],*activities_dict.values()):
    # for daily_attendance in zip(*activities_dict.values()):
    #     # print(f'{daily_attendance = }',end='\t')
        
    #     A = list(map(TextColor,*(assigned_colors,daily_attendance)))
    #     print(A)
    #     # print(list(map(TextColor,
    #     #     zip([activities_dict.keys()],activity))))
        
        
    #     # for x in zip([list(activities_dict.keys())],*activity):
    #         # print(x)
            
    #         # map(TextColor,)
            
    #     # print(list(map(dumps,list(map(NoEscape,map(partial(TextColor,assign_colors[activity.upper()]),assistance))))))
    
    
