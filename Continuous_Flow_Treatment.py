import numpy as np
from scipy.integrate import odeint


def DiffEq_cf(d_list, t):
    """
        Used to calculate the rate of change of the concentration of As(III) aqueous solution at time t

        Parameters:
            d_list-  [concentration of aqueous As(III) at time t, the quantity of arsenic adsorbed at time t]

        Returns:
            dCdt - the rate of change of the concentration of As(III) aqueous solution at time t

    """
    time1 = t
    # the reactor turnover rate
    j = exp[0, 2]
    # the inflow As(III) concentration
    Cinfluent = exp[0, 3]
    # rate constant
    k = exp[0, 4]
    # sorbent concentrations
    Cs = exp[0, 5]
    # Freundlich constant
    KF = exp[0, 6]

    # experimentally determined constants
    n = exp[0, 7]
    Qmax = exp[0, 8]
    KL = exp[0, 9]
    isotherm = exp[0, 10]
    order = exp[0, 11]
    Figure = exp[0, 12]

    # concentration of aqueous As(III) and the quantity of arsenic adsorbed at time t
    Ct, qt = d_list
    if Ct < 0.001:
        # set a minimum concentration of sorbate
        # in the reactor to prevent the Freundlich adsorption isotherm from running an error.
        Ct = 0.001

    if Ct >= Cinfluent:
        # control incase ode15s time intervals are too large
        Ct = Cinfluent

    Ct_mgL = Ct / 1000
    qt_mgg = qt / (Cs * 1000)
    if isotherm == 1:
        # Freundlich
        # batch treatment reactor design
        rate_ads = 1000 * k * Ct_mgL * Cs * (
                    (1 - (qt_mgg / (KF * (Ct_mgL ** (1 / n))))) ** order)

    elif isotherm == 2:
        # Langmuir
        # batch treatment reactor design
        rate_ads = 1000 * k * Ct_mgL * Cs * ((1 - (qt_mgg / ((Qmax * KL * Ct_mgL) / (1 + KL * Ct_mgL)))) ** order)

    # calculate the rate of sorbate influx (continuous-flow systems only)
    rate_influx = j * Cinfluent

    # calculate the rate of sorbate outflux (continuous-flow systems only)
    rate_outflux = j * Ct
    dCdt = [0, 0]

    # continuous treatment reactor design
    dCdt[0] = -rate_ads + rate_influx - rate_outflux


    if Figure == True:

        dCdt[1] = rate_ads / Cs * 1000
    elif Figure == False:

        dCdt[1] = rate_ads

    return dCdt








def Result_Processing_cf(j_flow, C_inf, Cs0, figure=True, ord_in=2, isotherms1="Freundlich",
                         k_in1=0.1111, KF_in1=5.10, n_in1=2.63,
                         Qmax_in1=29.44, KL_in1=0.11):
    """
          Used to data processing

          Parameters:
           C_inf -  Influence concentration (μg L-1)
           Cs0 - g L-1 - this is the concentration of sorbent
           j_flow - this the turn-over frequency, i.e. bed volumes per minute
           ord_in - The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
           isotherms1 - Adsorption isotherms and the default is Freundlich adsorption isotherms
           k_in1 -  The rate constant and the default value is 0.1111 (Lg−1 min−1)
           KF_in1 - this is the Freundlich constant (mg g-1)
           n_in1 -  this is the second parameter for the Freundlich adsorption isotherm (g L-1)
           Qmax_in1 - the maximum adsorption capacity  and the default value is 29.44 (mg g-1)
           KL_in1 - this is the Langmuir constant (mg g-1)

           Returns:
               results_table - [time, the concentration of aqueous As(III) at time t]
               counter - The number of days that the concentration of arsenic in the aqueous solution is below the UN standard



    """
    # each experiment will have a different initial sorbate concentration (C0)
    number_of_experiments = 1

    # counting how many rows in the array we need
    # to store the input parameters for each kinetic plot
    number_of_variables = 13

    # each experiment refers to a single kinetic plot
    experiments = np.zeros((number_of_experiments,
                            number_of_variables))

    # Select the corresponding adsorption isotherm according to the input
    if isotherms1 == "Freundlich":
        isoth_in = 1
    elif isotherms1 == "Langmuir":
        isoth_in = 2

    # creating the input variables for each kinetic plots

    C_init = 0.01
    # ug L-1  - this is
    # the initial concentration of aqueous sorbate in the suspension

    q_init = 0
    # ug L-1  - this is the initial concentration of adsorbed sorbate in the suspension

    Cs = Cs0
    # g L-1 - this is the concentration of sorbent

    Cinfluent = C_inf
    # ppb or ug L-1 - this is the concentration of sorbate in the influent (for continuous-flow modelling)

    j = j_flow
    # this the turn-over frequency, i.e. bed volumes per minute

    k = k_in1
    # this is the value of normalised k' (L g-1 min-1)

    KF = KF_in1
    # this is the Freundlich constant (mg g-1) used to determine 'qe' at each time step

    n = n_in1
    # this is the second parameter for
    # the Freundlich adsorption isotherm (g L-1) used to determine 'qe' at each time step

    Figure = figure

    Qmax = Qmax_in1
    # the maximum adsorption capacity
    isotherm = isoth_in
    # Adsorption isotherms
    order = ord_in
    # The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
    KL = KL_in1
    # the Langmuir constant

    # setting the time intervals upon which data is recorded. This will be
    # overwritten later to avoid wasting computational time after breakthrough
    # has already occurred.

    t_end = 1000000
    # 1440 min = 1 day
    t_steps = 20000
    t_step = t_end / t_steps
    bv_end = t_end * j
    tt = list(np.arange(0, t_end + 1, t_step))

    results_table = [0] * number_of_experiments

    for i in range(number_of_experiments):
        experiments[i, 0] = C_init
        experiments[i, 1] = q_init
        experiments[i, 2] = j
        experiments[i, 3] = Cinfluent
        experiments[i, 4] = k
        experiments[i, 5] = Cs  # exponentially increasing sorbent concentration
        experiments[i, 6] = KF
        experiments[i, 7] = n
        experiments[i, 8] = Qmax
        experiments[i, 9] = KL
        experiments[i, 10] = isotherm
        experiments[i, 11] = order
        experiments[i, 12] = Figure

    for i in range(number_of_experiments):
        global exp
        exp = np.zeros((1, number_of_variables))

        exp[0, :] = experiments[i, :]
        exp_C_init = exp[0, 0]
        exp_q_init = exp[0, 1]

        # making sure that we model an appropriate length of time (duration) with
        # appropriate interval lengths for each simulation.
        t_end = 180000 * exp[0, 5] / (exp[0, 2] * exp[0, 3])
        if t_end < 1000:
            t_end = t_end * 20

        if t_end < 500:
            t_end = t_end * 5

        if j < 0.01:
            t_end = t_end * 10

        if Figure == True:

            # collect data at shorter time intervals in the initial stages of the simulation
            stepping = [i for i in range(
                t_steps + 1)]
            stepping[0] = 0
            gradient_1 = 1
            gradient_2 = 30
            for j in range(1, (t_steps + 1)):
                # change the time intervals from being evenly spaced to having a smooth
                # transition from gradient_1 to gradient_2
                stepping[j] = stepping[j - 1] + (gradient_2 * (stepping[j] / t_steps)) + (
                            gradient_1 * ((t_steps - stepping[j]) / t_steps))

            for k in range(1, (t_steps + 1)):
                # normalise the time intervals to 1 and then multiply out by the desired
                # final time
                stepping[k] = (stepping[k] / stepping[-1]) * t_end

        elif Figure == False:

            # 525,600 minutes a year, 1,440 minutes a day
            stepping = [i for i in range(0, 525600, 1440)]

        # Use ODE to calculate the concentration of arsenic in aqueous solution at time t
        result = odeint(DiffEq_cf, [exp_C_init, exp_q_init], stepping, rtol=1e-6)

        counter = 0
        results_Ct = np.zeros((number_of_experiments, len(result[:, 0])))
        results_t = np.zeros((number_of_experiments, len(stepping)))
        results_t[i, :] = stepping
        results_Ct[i, :] = result[:, 0]

        # determine the adsorbent effective time
        for j in range(len(result[:, 0])):
            if result[:, 0][j] <= 10.5:
                counter += 1

        results_table[i] = [results_t[i, :], results_Ct[i, :]]
    return results_table, counter