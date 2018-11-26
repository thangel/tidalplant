# Using the module parameterisations module to determine turbine discharge
# coefficient for smooth transition between generating and sluicing
from parameterisations import *


def initialise_barrage(time=0.):
    """
    Initialises dictionary of barrage status - this contains information about the status of the barrage

    :param time: Initial simulation time
    return:
    """

    q_t, q_s, p, energy, m, m_dt, dz, r_f = 0., 0., 0., 0., 1., 0., 0., 0.,

    return {"m": m, "m_t": time/3600, "m_dt": m_dt, "DZ": dz, "f_r": r_f,
            "Q_t": q_t, "Q_s": q_s, "P": p, "E": energy}


def plant_specifications(turbine_number, sluice_number, operation='two-way', options=0):
    """
    Initialises certain control parameters depending on the general strategy to be adopted over the course of the
    operation.

    :param turbine_number: Number of turbines
    :param sluice_number: Number of sluice gates
    :param operation: operation options: Ebb-only generation        ==> "ebb"
                                         Ebb-pump generation        ==> "ebb-pump"
                                         Two-way generation         ==> "two-way"
                                         Two-way-pumping generation ==> "two-way-pump"

    ;:param options: turbine options  0 ==> realistic representation, 1 ==> idealised hill chart

    :return: control parameter array , turbine parameters
    """

    params, control = [], []
    turbine_params = {"f_g": 50, "g_p": 95, "g": 9.807, "t_d": 7.35,
                      "t_cap": 20, "dens": 1025, "h_min": 1.00,
                      "eta": [0.93, 0.83], "options": options}

    # Determination of turbine discharge coefficient for smooth transition from generating to sluicing.
    c_t = turbine_parametrisation(turbine_params["h_min"],
                                  turbine_params)[1] / ((math.pi * (turbine_params["t_d"] / 2)**2) *
                                                        math.sqrt(2 * turbine_params["g"] * turbine_params["h_min"]))

    sluice_params = {"a_s": 100, "c_d": 1.0, "c_t": c_t, "g": turbine_params["g"]}
    params.append({"turbine_specs": turbine_params, "sluice_specs": sluice_params})

    if operation == "ebb":
        control.append({"h_t": [3.5, 0.], "h_p": 2.5, "t_p": [0., 0.], "g_t": [6.0, 6.0], "tr_l": [7, -6],
                        "N_t": turbine_number, "N_s": sluice_number})
    elif operation == "ebb-pump":
        control.append({"h_t": [3.5, 0.], "h_p": 2.5, "t_p": [1.0, 0.], "g_t": [6.0, 6.0], "tr_l": [7, -6],
                        "N_t": turbine_number, "N_s": sluice_number})
    elif operation == "two-way":
        control.append({"h_t": [3.0, 3.0], "h_p": 2.5, "t_p": [0., 0.], "g_t": [3.0, 3.0], "tr_l": [7, -6],
                        "N_t": turbine_number, "N_s": sluice_number})
    elif operation == "two-way-pump":
        control.append({"h_t": [2.0, 2.0], "h_p": 2.5, "t_p": [0.5, 0.5], "g_t": [3.0, 3.0], "tr_l": [7, -6],
                        "N_t": turbine_number, "N_s": sluice_number})

    return control, params
