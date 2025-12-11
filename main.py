import csv
#Global variables
athletes = {}
stations = {
        "LJ": ["LJ1", "LJ2"],
        "TJ": ["TJ1", "TJ2"],
        "HJ": ["HJ1", "HJ2"],
        "PV": ["PV1"],
        "100m": ["TRACK"],
        "200m": ["TRACK"],
        "400m": ["TRACK"],
        "800m": ["TRACK"],
        "1600m": ["TRACK"]
    }

def CSVreader():
    with open("athletes.csv", newline='') as f:
        reader = csv.DictReader(f)
        metadata = {"Name", "Sex", "Age", "Country"}
        allColumns = reader.fieldnames
        events = [c for c in allColumns if c not in metadata]

        for row in reader:
            name = row["Name"].strip()
            if not name:
                continue
            entries = {}
            for d in events:
                val = row.get(d, "").strip()
                if val != "":
                    try:
                        pr = float(val)
                    except ValueError:
                        pr = val
                    entries[d] = pr
            athletes[name] = entries

def Schedules():
    schedule = []
    occupied = {}
    for athlete in sorted(athletes.keys()):
        athleteevents = athletes[athlete]
        for discipline in sorted(athleteevents.keys()):
            assigned = False
            slot = 1
            while not assigned:
                if slot not in occupied:
                    occupied[slot] = {}
                if athlete in occupied[slot].values():
                    slot += 1
                    continue
                for st in stations.get(discipline, []):
                    if st not in occupied[slot]:
                        pr = athleteevents[discipline]
                        occupied[slot][st] = athlete
                        schedule.append({
                            "TimeSlot": slot,
                            "Station": st,
                            "Discipline": discipline,
                            "Athlete": athlete,
                            "PR": pr
                        })
                        assigned = True
                        break
                if not assigned:
                    slot += 1
    schedule.sort(key=lambda x: (x["TimeSlot"], x["Station"]))
    return schedule

def OutputCSV(schedule, filname="schedule.csv"):
    filnames = ["TimeSlot", "Station", "Discipline", "Athlete", "PR"]
    with open(filname, "w", newline='',) as f:
        write = csv.DictWriter(f, fieldnames=filnames)
        write.writeheader()
        for row in schedule:
            r = dict(row)
            r["PR"] = "" if r["PR"] is None else r["PR"]
            write.writerow(r)

def main():
    outputfile = "schedule.csv"
    CSVreader()
    schedule = Schedules()
    OutputCSV(schedule, outputfile)
    print(f"Scheduled {len(schedule)} event entries -> {outputfile}")


if __name__ == "__main__":
    main()