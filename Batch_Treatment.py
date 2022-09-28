
import numpy as np
from scipy.integrate import odeint


def DiffEq_batch(conditions, t):

    """
          Used to calculate the rate of change of the concentration of As(III) aqueous solution at time t

          Parameters:
               conditions- [concentration of aqueous As(III) at time t, the quantity of arsenic adsorbed at time t]

          Returns:
               dCdt - the rate of change of the concentration of As(III) aqueous solution at time t

    """
    time = t
    j = exp[0][2]
    # the reactor turnover rate
    Cinfluent = exp[0][3]
    # the inflow As(III) concentration
    k = exp[0][4]
    # rate constant
    Cs1 = exp[0][5]
    # sorbent concentrations
    KF = exp[0][6]
    # Freundlich constant
    n = exp[0][7]
    # experimentally determined constants
    Qmax = exp[0][8]
    # the maximum adsorption capacity
    KL = exp[0][9]
    # the Langmuir constant
    isotherm = exp[0][10]
    # Adsorption isotherms
    order = exp[0][11]
    # The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
    Ct = conditions[0]
    # concentration of aqueous As(III) at time t
    qt[i] = conditions[1]
    # the quantity of arsenic adsorbed at time t

    # unit change
    Ct_mgL = Ct / 1000
    qt_mgg = qt[i] / (Cs1 * 1000)

    if isotherm == 1:
        # Freundlich
        # batch treatment reactor design
        rate_ads = 1000 * k * Ct_mgL * Cs1 * (
                    (1 - (qt_mgg / (KF * (Ct_mgL ** (1 / n))))) ** order)

    elif isotherm == 2:
        # Langmuir
        # batch treatment reactor design
        rate_ads = 1000 * k * Ct_mgL * Cs1 * ((1 - (qt_mgg / ((Qmax * KL * Ct_mgL) / (1 + KL * Ct_mgL)))) ** order)

    if Ct < 0.000001:
        Ct = 0.00001
        rate_ads = 0

    rate_influx = j * Cinfluent
    rate_outflux = j * Ct
    # batch treatment reactor design (when j=0)
    dCdt = [-rate_ads + rate_influx - rate_outflux, rate_ads]
    # finally we need to update qt(i) so that the next day's simulation begins
    # with the appropriate amount of sorbate already attached.

    qt[i] = qt[i] + rate_ads

    return dCdt


def Result_Processing_batch(C_in, Cs0, days, ord_in=2, isotherms="Freundlich", k_in=0.1111, KF_in=5.10, n_in=2.63,
                            Qmax_in=29.44, KL_in=0.11):
    """
          data processing and  determine the adsorbent effective time

          Parameters:
           C_in-  ppb or ug L-1 - this is the initial concentration of aqueous sorbate in the suspension
           Cs0 - g L-1 - this is the concentration of sorbent
           days - the duration of the batch treatment
           ord_in- The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
           isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms
           k_in-  The rate constant and the default value is 0.1111 (Lg−1 min−1)
           KF_in- this is the Freundlich constant (mg g-1)
           n_in-  this is the second parameter for the Freundlich adsorption isotherm (g L-1)
           Qmax_in- the maximum adsorption capacity  and the default value is 29.44 (mg g-1)
           KL_in- this is the Langmuir constant (mg g-1)

           Returns:

               Cs_col - Sorbent concentration
               results_Ct - the concentration of aqueous As(III) at time t
               results_table - Adsorbent effective time
               data_collect - time sampling within one day


       """

    global i
    global exp
    global qt
    qt = [0, 0, 0, 0, 0, 0, 0]
    number_of_experiments = 7
    number_of_variables = 12

    # each experiment refers to a single kinetic plot
    results_table = [([0] * number_of_experiments) for i in range(10)]

    # Select the corresponding adsorption isotherm according to the input
    if isotherms == "Freundlich":
        isoth_in = 1
    elif isotherms == "Langmuir":
        isoth_in = 2

    for day in range(1, days + 1):
        C_init = C_in
        # sorbent concentrations (initial value)
        q_init = qt
        # the quantity of arsenic adsorbed at time t (initial value)
        Cs = Cs0
        # sorbent concentrations
        Cinfluent = 0
        # the inflow As(III) concentration
        j = 0
        # the reactor turnover rate
        k = k_in
        # rate constant
        KF = KF_in
        # Freundlich constant
        Qmax = Qmax_in
        # the maximum adsorption capacity
        isotherm = isoth_in
        # Adsorption isotherms
        order = ord_in
        # The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
        KL = KL_in
        # the Langmuir constant
        n = n_in
        # Experimentally determined constants

        # time sampling within one day
        data_collect = [0, 1, 2, 3, 4,
                        5, 6, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 200, 210, 220, 230,
                        240, 270, 300, 330, 360, 390, 420, 450, 480, 500, 570,
                        600, 660, 690, 720, 750, 780, 840, 870, 900, 930, 960, 990, 1000, 1050, 1080, 1110, 1140,
                        1170, 1200, 1260, 1290, 1320, 1350, 1380, 1410, 1440]
        t_end = 1440

        t_steps = len(data_collect)
        t_step = t_end / t_steps
        tt = list(np.arange(0, t_end + 1, t_step))

        results_Ct = np.zeros((number_of_experiments, len(data_collect)))
        results_qt = np.zeros((number_of_experiments, len(data_collect)))

        experiments = [[0] * number_of_variables for _ in range(number_of_experiments)]
        Cs_col = [0] * number_of_experiments
        for i in range(number_of_experiments):
            experiments[i][0] = C_init
            experiments[i][1] = q_init[i]
            experiments[i][2] = j
            experiments[i][3] = Cinfluent
            experiments[i][4] = k
            experiments[i][5] = Cs * 10 ** (i - 4)  # exponentially increasing sorbent concentration
            experiments[i][6] = KF
            experiments[i][7] = n
            experiments[i][8] = Qmax
            experiments[i][9] = KL
            experiments[i][10] = isotherm
            experiments[i][11] = order
            Cs_col[i] = experiments[i][5]

        for i in range(number_of_experiments):

            exp = [[0] * number_of_variables for _ in range(1)]
            exp[0][:] = experiments[i][:]
            exp_C_init = exp[0][0]
            exp_q_init = exp[0][1]

            # Use ODE to calculate the concentration of arsenic in aqueous solution at time t
            result = odeint(DiffEq_batch, [exp_C_init, exp_q_init], data_collect, rtol=1e-6)

            results_Ct[i, :] = result[:, 0]

            #  determine the adsorbent effective time

            for j in range(len(results_Ct[i, :])):
                if results_Ct[i, :][j] <= 10 and data_collect[j] == 1:
                    results_table[0][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] == 2:
                    results_table[1][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] == 5:
                    results_table[2][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [10]:
                    results_table[3][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [20]:
                    results_table[4][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [50]:
                    results_table[5][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [100]:
                    results_table[6][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [200]:
                    results_table[7][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [500]:
                    results_table[8][i] += 1

                if results_Ct[i, :][j] <= 10 and data_collect[j] in [100]:
                    results_table[9][i] += 1

            results_qt[i, :] = result[:, 1]

    return results_Ct, Cs_col,data_collect, results_table