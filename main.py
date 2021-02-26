import os
import sys
import datetime



if os.path.exists("database.db"):
    os.remove("database.db")

from DTO import Vaccine, Supplier, Clinic, Logistic
from persistence import repo


def Receive_Shipment(vaccineid, suppliername, vaccinesamount, vaccinesdate):
    # adding < amount > vaccines from < name > on < date >
    supplier_id = repo.getSupplierIDByName(suppliername)[0]
    repo.vaccines.insert(Vaccine(vaccineid, vaccinesdate, supplier_id, vaccinesamount))

    #  update the count received on the relevant supplier
    logisticofsupplier = repo.getlogisticsOfSupplier(supplier_id)
    repo.logistics.update_count_received(logisticofsupplier.id, logisticofsupplier.count_received + int(vaccinesamount))


def Send_Shipment(location, amount):
    # remove < amount > from the demand of < location >
    clinic = repo.getClinicsByLocation(location)
    repo.clinics.update(clinic.id, clinic.demand - amount)

    # update the relevant logistic service count sent with the added < amount >
    logisticofclinic = repo.getlogisticsOfClinic(clinic.id)
    repo.logistics.update_count_sent(logisticofclinic.id, logisticofclinic.count_sent + amount)

    # remove the sum of < amount > from the inventory
    while amount > 0:
        vaccine = repo.getOldestVaccine();
        if vaccine.quantity <= amount:
            amount = amount - vaccine.quantity
            repo.vaccines.delete(vaccine.id)
        else:
            repo.vaccines.update(vaccine.id, vaccine.quantity - amount)
            amount = 0


def main(args):
    vaccinesID = 0
    suppliersID = 0
    clinicsID = 0
    logisticsID = 0

    # Print a summary in a output file.
    outpufilename = args[3]
    outpufile = open(outpufilename, "w")

    # Create and populate the database according to a configuration file
    repo.create_tables()
    configfilename = args[1]
    with open(configfilename) as configfile:
        number_of_entries = configfile.readline().split(",")

        # Insert the vaccines
        for i in range(int(number_of_entries[0])):
            line = configfile.readline().split(",")
            repo.vaccines.insert(Vaccine(*line))
            vaccinesID = max(vaccinesID, int(line[0]))

        # Insert the suppliers
        for i in range(int(number_of_entries[1])):
            line = configfile.readline().split(",")
            repo.suppliers.insert(Supplier(*line))
            suppliersID = max(suppliersID, int(line[0]))

        # Insert the clinics
        for i in range(int(number_of_entries[2])):
            line = configfile.readline().split(",")
            repo.clinics.insert(Clinic(*line))
            clinicsID = max(clinicsID, int(line[0]))

        # Insert the logistics
        for i in range(int(number_of_entries[3])):
            line = configfile.readline().split(",")
            repo.logistics.insert(Logistic(*line))
            logisticsID = max(logisticsID, int(line[0]))


    # Execute a list of orders, according to a second file.
    ordersfilename = args[2]
    with open(ordersfilename) as ordersfile:
        for line in ordersfile:
            orderline = line.split(",")
            if len(orderline) == 3:
                vaccinesID += 1
                Receive_Shipment(vaccinesID, *orderline)
            else:
                Send_Shipment(orderline[0], int(orderline[1]))
            summarylist = repo.getSummary()
            outpufile.writelines((','.join(str(i) for i in summarylist)) + '\n')

    outpufile.close()

if __name__ == '__main__':
    main(sys.argv)

