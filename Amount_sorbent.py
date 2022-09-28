from Continuous_Flow_Treatment import Result_Processing_cf
import math


def Min_adsorbent_bt(results_counter, Cs_col, days, people):
    """
    Used to calculate the sorbent mass required for the batch process

    Parameters:
     Cs_col- List of Sorbent Concentrations
     results_counter - The number of days that the concentration
                       of arsenic in the aqueous solution is below the UN standard (corresponds to Cs_col)
     days- the duration of the batch treatment
     people- Average number of people per household in the region

    Returns:
     min(results) - Returns Sorbent Mass
     Cs_col[a + 2] - Minimum mass sorbent concentration
     results_counter[a + 2] - Adsorbent effective time


    """
    # Only go for concentrations from 1 to 1000,
    # because the 0.1 and 0.001 adsorbent concentrations are too small and ignored
    ads = Cs_col[2:]

    # The mass of adsorbent required to receive the corresponding concentration
    results = [0] * len(ads)

    for h in range(2, len(results_counter)):

        # To prevent the situation where the number of days is 0
        # so the function cannot be calculated
        if results_counter[h] == 0:

          results_counter[h] = 0.0001

        # Calculate adsorbent mass
        results[h - 2] = (days / results_counter[h]) * ads[h - 2] * 0.001 * (math.ceil(people*7))

    # Select the case with the smallest adsorbent mass
    a = results.index(min(results))
    return min(results), Cs_col[a + 2], results_counter[a + 2]


def Adsorbents_required(C_in1=500, Cs_in=100, j_flow=0.001, ord_in=2, isotherms1="Freundlich",
                        k_in1=0.1111, KF_in1=5.10, n_in1=2.63, Qmax_in1=29.44, KL_in1=0.11):
    """
       Used to calculate the required adsorbent mass for continuous flow processing

       Parameters:
        C_in1-  ppb or ug L-1 - this is the initial concentration of aqueous sorbate in the suspension
        Cs_in - g L-1 - this is the concentration of sorbent
        j_flow- this the turn-over frequency, i.e. bed volumes per minute
        ord_in- The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
        isotherms1- Adsorption isotherms and the default is Freundlich adsorption isotherms
        k_in1-  The rate constant and the default value is 0.1111 (Lg−1 min−1)
        KF_in1- this is the Freundlich constant (mg g-1)
        n_in1-  this is the second parameter for the Freundlich adsorption isotherm (g L-1)
        Qmax_in1- the maximum adsorption capacity  and the default value is 29.44 (mg g-1)
        KL_in1- this is the Langmuir constant (mg g-1)

        Returns:
            min(results) - Returns Sorbent Mass
            Cs_col[a + 2] - Minimum mass sorbent concentration
            results_counter[a + 2] - Adsorbent effective time


    """
    number_of_experiments = 7

    # List of Sorbent Concentrations
    Cs_col_cf = [0] * number_of_experiments
    for i in range(number_of_experiments):
        Cs_col_cf[i] = Cs_in * 10 ** (i - 4)

    # Calculate the number of days
    # when the arsenic concentration in the aqueous solution is below the UN standard
    # for different sorbent concentrations
    _, counter_10000 = Result_Processing_cf(j_flow, C_in1, Cs_col_cf[6], False, ord_in, isotherms1,
                                            k_in1, KF_in1, n_in1, Qmax_in1, KL_in1)

    _, counter_1000 = Result_Processing_cf(j_flow, C_in1, Cs_col_cf[5], False, ord_in, isotherms1,
                                           k_in1, KF_in1, n_in1, Qmax_in1, KL_in1)

    _, counter_100 = Result_Processing_cf(j_flow, C_in1, Cs_col_cf[4], False, ord_in, isotherms1,
                                          k_in1, KF_in1, n_in1, Qmax_in1, KL_in1)

    _, counter_10 = Result_Processing_cf(j_flow, C_in1, Cs_col_cf[3], False, ord_in, isotherms1,
                                         k_in1, KF_in1, n_in1, Qmax_in1, KL_in1)

    _, counter_1 = Result_Processing_cf(j_flow, C_in1, Cs_col_cf[2], False, ord_in, isotherms1,
                                        k_in1, KF_in1, n_in1, Qmax_in1, KL_in1)

    # Only go for concentrations from 1 to 1000,
    # because the 0.1 and 0.001 adsorbent concentrations are too small and ignored
    ads = Cs_col_cf[2:]

    # The number of days that the concentration
    #  of arsenic in the aqueous solution is below the UN standard
    result_counter = [counter_1, counter_10, counter_100, counter_1000, counter_10000]

    # The mass of adsorbent required to receive the corresponding concentration
    results = [0] * len(result_counter)

    for i in range(len(result_counter)):
        # To prevent the situation where the number of days is 0
        # so the function cannot be calculated
        if result_counter[i] == 0:
            result_counter[i] = 0.0001

        # Calculate adsorbent mass
        results[i] = (365 / result_counter[i]) * ads[i] * 0.001 * 40

    # Select the case with the smallest adsorbent mass
    a = results.index(min(results))

    return min(results), Cs_col_cf[a + 2], result_counter[a]
