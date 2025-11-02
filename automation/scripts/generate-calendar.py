#!/usr/bin/env python3
import csv, glob, os
lines = ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Event Calendar Planner//EN']
for path in sorted(glob.glob('data/*.csv')):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i,row in enumerate(reader):
            lines.append('BEGIN:VEVENT')
            uid = f'event-{os.path.basename(path)}-{i}-{row.get("Date","")}' 
            lines.append('UID:' + uid)
            date = row.get('Date','')
            if date:
                if len(date.split())==1:
                    lines.append('DTSTART;VALUE=DATE:' + date.replace('-',''))
                    lines.append('DTEND;VALUE=DATE:' + date.replace('-',''))
                else:
                    dt = date.replace('-','').replace(':','').replace(' ','T') + '00Z'
                    lines.append('DTSTART:' + dt)
                    lines.append('DTEND:' + dt)
            lines.append('SUMMARY:' + (row.get('Event Name','')))
            desc = ' | '.join([row.get('Venue',''), row.get('Organizer',''), row.get('Notes','')])
            if desc.strip():
                lines.append('DESCRIPTION:' + desc)
            lines.append('END:VEVENT')
lines.append('END:VCALENDAR')
os.makedirs('calendar', exist_ok=True)
with open('calendar/events.ics','w',encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Wrote calendar/events.ics')
