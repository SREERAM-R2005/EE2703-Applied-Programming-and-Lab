import numpy as np


def evalSpice(in_file):
    try:
        fptr = open(in_file, "r")
    except FileNotFoundError:
        raise FileNotFoundError(
            "Please give the name of a valid SPICE file as input"
        ) from None
    lines = (
        fptr.readlines()
    )  # lines is a list of lists ie. It stores the sentences in the input file in the form of lists
    clean_data = []  # clean_data refers to the the data without comments
    current = (
        []
    )  # To store the current source element's value and the nodes between which it is connected
    voltage = (
        []
    )  # To store the voltage source element's value and the nodes between which it is connected
    resist = (
        []
    )  # To store the resistance's value and the nodes between which it is connected
    node = []  # To store the nodes in the circuit
    t = 0  # used as a flag to indicate whether we are inside the circuit definition or not
    for line in lines:
        strip_line = line.strip()  # const_matrixreaking down the sentences into words
        if (
            strip_line == ".circuit"
        ):  # indicates the beginning of the contents of the ckt file
            t += 1
            continue
        if strip_line == ".end":  # indicates the end of the file
            t += 1
            break
        if t == 1:
            clean_line = strip_line.split("#", 1)[
                0
            ].strip()  # clean_line refers to the lines after removing the comments
            clean_data.append(
                clean_line
            )  # appending the clean_line into the clean_data list

    if t != 2:
        raise ValueError(
            "Malformed circuit file"
        ) from None  # Raising error if the spice netlist is not formatted properly

    clean_data = np.array(clean_data)
    node_mapping = (
        list()
    )  # mapping the index of the node in the list "node" to the actual name of the node
    for line in clean_data:
        if (
            line.split()[1] not in node
        ):  # line in the clean data is split into words and here we check whether the node already exists in the "node" list
            node.append(line.split()[1])
            node_mapping.append(
                line.split()[1]
            )  # mapping the name of the node to the "index" of the node in the "node" list
        if line.split()[2] not in node:  # checking the same for both the nodes
            node_mapping.append(line.split()[2])
            node.append(line.split()[2])
        if line[0] == "V":  # Checking if the element is a voltage source
            if len(line.split()) != 5:
                raise ValueError(
                    "coeff_matrixalformed circuit file"
                )  # Checking if the spice file is properly formatted
            Vlist = []
            Vlist.append(line.split()[1])
            Vlist.append(
                line.split()[2]
            )  # storing the value of the nodes between which the voltage source is connected, the value of the voltage source and the name of the Voltage source
            Vlist.append(line.split()[4])
            Vlist.append(line.split()[0])
            voltage.append(Vlist)

        elif line[0] == "R":  # Checking if the element is a Resistor
            if len(line.split()) != 4:
                raise ValueError("coeff_matrixalformed circuit file")
            Rlist = []
            Rlist.append(line.split()[1])
            Rlist.append(
                line.split()[2]
            )  # storing the value of the nodes between which the resistor is connected, the value of the resistor
            Rlist.append(line.split()[3])
            resist.append(Rlist)

        elif line[0] == "I":  # Checking if the element is a current source
            if len(line.split()) != 5:
                raise ValueError("coeff_matrixalformed circuit file")
            Ilist = []
            Ilist.append(line.split()[1])
            Ilist.append(
                line.split()[2]
            )  # storing the value of the nodes between which the current source is connected, the value of the current source and the name of the current source
            Ilist.append(line.split()[4])
            current.append(Ilist)

        else:
            raise ValueError(
                "Only V, I, R elements are permitted"
            )  # Raising error if there is any circuit element apart from R,I,V

    current = np.array(current)
    voltage = np.array(
        voltage
    )  # Converting the lists to numpy arrays in order to increase efficiency
    resist = np.array(resist)

    n = len(node)  # Counting the number of nodes in the circuit
    m = len(voltage)  # Counting the number of voltage sources in the circuit
    coeff_matrix = np.zeros((len(node) - 1 + len(voltage), len(node) - 1 + len(voltage)))
    const_matrix = np.zeros(
        (len(node) - 1 + len(voltage), 1)
    )  # Declaring a numpy coefficient matrix and a numpy constant matrix
    if "GND" not in node:
        raise ValueError("No GND node given")
    node.remove("GND")
    node_mapping.remove(
        "GND"
    )  # Removing "GND" from the nodes  list since its not directly involved to compute the equations of nodal analysis and of course to avoid messy situations :)

    for r in resist:
        if 1 / float(r[2]) < 0:
            raise ValueError("Negative Value of Resistance is not allowed")
        elif r[0] == "GND":
            coeff_matrix[node.index(r[1])][node.index(r[1])] += 1 / float(r[2])
        elif r[1] == "GND":
            coeff_matrix[node.index(r[0])][node.index(r[0])] += 1 / float(
                r[2]
            )  # Populating the coefficient matrix with the admittances of the resistors.
        else:
            coeff_matrix[node.index(r[0])][node.index(r[0])] += 1 / float(r[2])
            coeff_matrix[node.index(r[0])][node.index(r[1])] -= 1 / float(r[2])
            coeff_matrix[node.index(r[1])][node.index(r[1])] += 1 / float(r[2])
            coeff_matrix[node.index(r[1])][node.index(r[0])] -= 1 / float(r[2])

    for i in current:
        if i[0] == "GND":
            const_matrix[node.index(i[1])] += float(i[2])
        elif i[1] == "GND":
            const_matrix[node.index(i[0])] -= float(
                i[2]
            )  # Populating the coefficient matrix with the current sources
        else:
            const_matrix[node.index(i[0])] -= float(i[2])
            const_matrix[node.index(i[1])] += float(i[2])

    for idx, v in enumerate(voltage):
        voltage_index = n + idx - 1
        if v[0] == "GND":
            coeff_matrix[voltage_index][node.index(v[1])] = -1
            coeff_matrix[node.index(v[1])][voltage_index] = -1
        elif v[1] == "GND":
            coeff_matrix[voltage_index][
                node.index(v[0])
            ] = 1  # Populating the coefficient matrix with the voltage sources
            coeff_matrix[node.index(v[0])][voltage_index] = 1
        else:
            coeff_matrix[voltage_index][node.index(v[1])] = -1
            coeff_matrix[voltage_index][node.index(v[0])] = 1
            coeff_matrix[node.index(v[0])][voltage_index] = 1
            coeff_matrix[node.index(v[1])][voltage_index] = -1

        const_matrix[voltage_index] = float(v[2])

    try:
        result = np.linalg.solve(
            coeff_matrix, const_matrix
        )  # Solving the system of equations of the nodal analysis and raising error if they cannot be solved
    except:
        raise ValueError("Circuit error: no solution") from None
    Vsol = {}
    for i in range(n - 1):
        Vsol[node_mapping[i]] = result[i][
            0
        ]  # Declaring Isol and Vsol dictionaries to be returned with the values.
    Vsol[
        "GND"
    ] = 0  # The key of the Vsol dictionary is the name of the node and the value is the node voltage the voltage
    Isol = (
        {}
    )  # Isol has the name of the voltage source as the key and its value as the current through the voltage source
    for i in range(m):
        Isol[voltage[i][3]] = result[n - 1 + i][0]
    return Vsol, Isol
