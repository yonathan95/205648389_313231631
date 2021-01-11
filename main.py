import atexit
import sys


import Repository
from DTO import Vaccine, Supplier, Clinic, Logistic

if __name__ == '__main__':
    config = sys.argv[1]
    orders = sys.argv[2]
    output = sys.argv[3]
    output_lines = []
    vaccines = 0
    suppliers = 0
    clinics = 0
    logistics = 0
    repo = Repository._Repository()
    repo.create_tables()
    with open(config) as config:
        lines = config.read().splitlines()
        configs = lines[0].split(',')
        vaccines = int(configs[0])
        suppliers = int(configs[1])
        clinics = int(configs[2])
        logistics = int(configs[3])
        lines = lines[::-1]
        lines.pop()
        for line in lines:
            if logistics > 0:
                repo.logistics.insert(Logistic(line.split(',')))
                logistics -= 1
                continue
            if clinics > 0:
                repo.clinics.insert(Clinic(line.split(',')))
                clinics -= 1
                continue
            if suppliers > 0:
                repo.suppliers.insert(Supplier(line.split(',')))
                suppliers -= 1
                continue
            if vaccines > 0:
                repo.vaccines.insert(Vaccine(line.split(',')))
                vaccines -= 1
                continue

    with open(orders) as orders:
        for line in orders:
            line = line.split(',')
            if len(line) == 2:
                repo.send_shipment(line)
                output_lines.append(repo.summary())
            else:
                repo.receive_shipment(line)
                output_lines.append(repo.summary())

    with open(output, 'w') as output:
        for line in output_lines:
            writer = output.write(line)
    atexit.register(repo._close)
