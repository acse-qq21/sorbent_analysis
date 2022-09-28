import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.messagebox
from matplotlib.figure import Figure
from tkinter.ttk import *
import time
from Batch_Treatment import Result_Processing_batch
from Amount_sorbent import *



def main_window():
    """
            The main window of the interactive interface is used to input most parameters
            and select the type of adsorption isotherm and the order of the adsorption kinetic equation

    """

    global var_order
    global n_in
    global KF_in
    global k_in
    global Qmax_in
    global KL_in
    global n_in_er
    global KF_in_er
    global k_in_er
    global Qmax_in_er
    global KL_in_er

    # Create a window
    window = tk.Tk()

    # Create title of window
    window.title('Predicting Removal of Sorbate from Sorbents')
    # Set up the window size and position on screen
    window.geometry('600x400+400+200')

    # The pseudo order of kinetic
    # and the default is pseudo-first-order adsorption kinetic equation
    var_order = tk.StringVar()
    var_order.set(1)

    # The rate constant and the default value is 0.1111 (Lg−1min−1)
    k_in = tk.StringVar()
    k_in.set(0.1111)

    # the maximum adsorption capacity  and the default value is 29.44 (mg g-1)
    Qmax_in = tk.StringVar()
    Qmax_in.set(29.44)

    # the Langmuir constant and the default value is 5.11 (L mg-1)
    KL_in = tk.StringVar()
    KL_in.set(5.11)

    # Adsorption capacity ( Freundlich parameters)
    # and the default value is 5.10 (mg g-1 (mg L-1) -1/n)
    KF_in = tk.StringVar()
    KF_in.set(5.10)

    # Experimentally determined constants and the default value is 2.63
    n_in = tk.StringVar()
    n_in.set(2.63)

    # The error range and the default value is 0.015
    k_in_er = tk.StringVar()
    k_in_er.set(0.015)

    # The error range and the default value is 2.99
    Qmax_in_er = tk.StringVar()
    Qmax_in_er.set(2.99)

    # The error range and the default value is 0.10
    KL_in_er = tk.StringVar()
    KL_in_er.set(0.10)

    # The error range and the default value is 1.60
    KF_in_er = tk.StringVar()
    KF_in_er.set(1.60)

    # The error range and the default value is 0.14
    n_in_er = tk.StringVar()
    n_in_er.set(0.14)

    # user information
    # Create a text box
    l = tk.Label(window, text='Prediction of the sorbent required to remove sorbate from water',
                 bg='Blue', font=('Arial', 12), width=50,
                 height=2)

    # Label content content area placement, automatic resizing
    l.pack()

    # Create a text box
    tk.Label(window, text='Langmuir Parameters ',
                 bg='Blue', font=('Arial', 10), width=20,
                 height=1).place(x=25, y=70)

    tk.Label(window, text='Maximum adsorption capacity (mg g^-1)  ').place(x=1, y=110)
    tk.Label(window, text='Langmuir constant (Lmg^-1) ').place(x=1, y=140)

    # Create a text box
    tk.Label(window, text='Freundlich Parameters ',
                 bg='Blue', font=('Arial', 10), width=20,
                 height=1).place(x=25, y=180)

    tk.Label(window, text='constant n ').place(x=1, y=210)
    tk.Label(window, text='Freundlich constant (mg g^-1(mgL^-1)^(-1/n)) ').place(x=1, y=240)

    # Create a text box
    tk.Label(window, text='Kinetics Parameters ',
             bg='Blue', font=('Arial', 10), width=20,
             height=1).place(x=25, y=270)

    # Create a text box
    tk.Label(window, text="Rate constant (L g^-1 min^-1)").place(x=1, y=300)
    tk.Label(window, text="Order of pseudo").place(x=1, y=320)

    tk.Label(window, text='Errors',
             bg='Blue', font=('Arial', 10), width=10,
             height=1).place(x=480, y=70)


    # Create an input box and set the initial value in advance
    lan_Qmax = tk.Entry(window, textvariable=Qmax_in)
    lan_Qmax.place(x=280, y=110)

    # input error
    lan_Qmax_error = tk.Entry(window, textvariable=Qmax_in_er)
    lan_Qmax_error.place(x=450, y=110)

    # Create an input box and set the initial value in advance
    lan_KL = tk.Entry(window, textvariable=KL_in)
    lan_KL.place(x=280, y=140)

    # input error
    lan_KL_error = tk.Entry(window, textvariable=KL_in_er)
    lan_KL_error.place(x=450, y=140)

    # Create an input box and set the initial value in advance
    Fre_n = tk.Entry(window, textvariable=n_in)
    Fre_n.place(x=280, y=210)

    # input error
    Fre_n_error = tk.Entry(window, textvariable=n_in_er)
    Fre_n_error.place(x=450, y=210)

    # Create an input box and set the initial value in advance
    Fre_KF = tk.Entry(window, textvariable=KF_in)
    Fre_KF.place(x=280, y=240)

    # input error
    Fre_KF_error = tk.Entry(window, textvariable=KF_in_er)
    Fre_KF_error.place(x=450, y=240)

    # Create an input box and set the initial value in advance
    entry_k = tk.Entry(window, textvariable=k_in)
    entry_k.place(x=280, y=300)

    # input error
    entry_k_error = tk.Entry(window, textvariable=k_in_er)
    entry_k_error.place(x=450, y=300)

    # Define checkboxes
    # choose either first order or second order
    entry_O = tk.Checkbutton(window, text="pseudo-second order", variable=var_order, onvalue=2, offvalue=1)
    entry_O.place(x=280, y=320)

    # login and sign up button
    # Create button, Click the button to call the Transition function
    # window.destroy() :  delete this window
    btn_bt = tk.Button(window, text='Langmuir isotherms', command=lambda: [window.destroy(), Transition("Langmuir")])
    btn_bt.place(x=50, y=360)
    btn_cf = tk.Button(window, text='Freundlich isotherms', command=lambda: [window.destroy(), Transition("Freundlich")])
    btn_cf.place(x=340, y=360)

    window.mainloop()


def batch_treatment(isotherms):
    """
                  batch treatment interface

                   Parameters:

                       isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms

    """

    global days
    # Create a window
    bt = tk.Tk()
    # window title
    bt.title('Batch Treatment')
    # Call window size and position on screen
    bt.geometry('450x300+400+200')

    # Reaction days and the default value is 365
    days = tk.StringVar()
    days.set(365)

    # user information
    tk.Label(bt, text='Reaction time (days)').place(x=50, y=80)
    # Create an input box and set the initial value in advance
    entry_day = tk.Entry(bt,textvariable=days)
    entry_day.place(x=240, y=80)

    # Create button, Click the button to call the progress function
    # bt.destroy() :  delete this window
    # progress(isotherms, 1): 1 represents the mark as batch treatment
    btn_re = tk.Button(bt, text='Results', command=lambda: [bt.destroy(), progress(isotherms, 2)])
    btn_re.place(x=100, y=200)

    # Create button, Click the button to back to the main window()
    # bt.destroy() :  delete this window
    btn_ba = tk.Button(bt, text='Back', command=lambda: [bt.destroy(), main_window()])
    btn_ba.place(x=270, y=200)

    bt.mainloop()


def continuous_flow(isotherms):
    """
               continuous flow interface

                Parameters:

                    isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms



    """

    global j_in

    # Create a window
    cf = tk.Tk()
    # window title
    cf.title('Continuous Flow Treatment')

    # Call window size and position on screen
    cf.geometry('450x300+400+200')

    # Turnover rate (min-1) and the default value is 0.001
    j_in = tk.StringVar()
    j_in.set(0.001)

    # user information
    tk.Label(cf, text='Turnover rate (min^-1) ').place(x=50, y=80)
    # Create an input box and set the initial value in advance
    entry_j = tk.Entry(cf, textvariable=j_in)
    entry_j.place(x=240, y=80)

    # Create button, Click the button to call the progress function
    # bt.destroy() :  delete this window
    # progress(isotherms, 1): 1 represents the mark as continuous flow
    btn_re = tk.Button(cf, text='Results', command=lambda: [cf.destroy(), progress(isotherms, 1)])
    btn_re.place(x=100, y=200)

    # Create button, Click the button to back to the main window()
    # cf.destroy() :  delete this window
    btn_ba = tk.Button(cf, text='Back', command=lambda: [cf.destroy(), main_window()])
    btn_ba.place(x=240, y=200)

    cf.mainloop()


def progress(isotherms, function_choose):
    """
            A progress bar, showing the running progress of the model

            Parameters:

                isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms
                function_choose-Batch treatment or continue flow treatment


    """
    # Create a window
    root = tk.Tk()
    # window title
    root.title('Loading........')
    # Call window size and position on screen
    root.geometry('450x300+400+200')

    # creat a process bar
    progressbarOne = Progressbar(root, orient=tkinter.HORIZONTAL, length=350, mode='determinate')
    progressbarOne.place(x=40, y=80)


    def preventRepeatedClicks(on):
        """
                    recursive function, Prevent button from calling Result_windows function repeatedly

                    Parameters:

                        on - Determine if a Result_windows function is called


        """


        if on == 'kai':
            # When the Running button is clicked, run the model
            demoBtn = tkinter.Button(root, text="Running", width=20, height=1,
                                     command=lambda: [Result_windows(isotherms,
                                                                     function_choose, progressbarOne, root)

                                                        ])
            demoBtn.place(x=140, y=200)

    # recursive function
    preventRepeatedClicks('kai')

    # progress value max
    progressbarOne['maximum'] = 100
    # progress value initial value
    progressbarOne['value'] = 0

    root.mainloop()


def Transition(isotherms):
    """
        The user inputs parameters such as the adsorbent concentration,
        the concentration of arsenic in the aqueous solution, and selects the method of water treatment

        Parameters:

            isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms


    """
    global Cin
    global Cs
    global people
    # Create a window
    Tra = tk.Tk()
    # Call window size and position on screen
    Tra.geometry('450x300+400+200')
    # window title
    Tra.title('Predicting Removal of Arsenic from Sorbents')
    # Initial sorbate concentration and the default value is 500
    Cin = tk.StringVar()
    Cin.set(500)
    # the concentration of sorbent and the default value is 100
    Cs = tk.StringVar()
    Cs.set(100)
    # Average number of people per household in the region and the default value is 5.7
    people = tk.StringVar()
    people.set(5.7)
    # Create text boxes
    tk.Label(Tra, text='Sorbate concentration (ug/L)').place(x=1, y=50)
    tk.Label(Tra, text='Sorbent concentration (g/L)').place(x=1, y=80)
    tk.Label(Tra, text='Average of people per household').place(x=1, y=110)

    # Create an input box and set the initial value in advance
    entry_sorbent_con = tk.Entry(Tra, textvariable=Cin)
    entry_sorbent_con.place(x=240, y=50)

    entry_sorbate_con = tk.Entry(Tra, textvariable=Cs)
    entry_sorbate_con.place(x=240, y=80)

    entry_sorbate_con = tk.Entry(Tra, textvariable=people)
    entry_sorbate_con.place(x=240, y=110)

    # Create button, Click the button to call the batch_treatment function
    # Tra.destroy() :  delete this window
    btn_bt = tk.Button(Tra, text='Batch Treatment ', command=lambda: [Tra.destroy(), batch_treatment(isotherms)])
    btn_bt.place(x=50, y=180)
    # Create button, Click the button to call the continuous_flow function
    # Tra.destroy() :  delete this window
    btn_cf = tk.Button(Tra, text='Continuous Flow Treatment', command=lambda: [Tra.destroy(), continuous_flow(isotherms)])
    btn_cf.place(x=250, y=180)

    # Create button, Click the button to back to the main window()
    # Tra.destroy() :  delete this window
    btn_back_cf = tk.Button(Tra, text='Back', command=lambda: [Tra.destroy(), main_window()])
    btn_back_cf.place(x=180, y=230)

    Tra.mainloop()


def plot(time, results_table, C_s_in, C_d_in, isotherms, oder,function_choose,num=1):
    """
              plot the result

              Parameters:
                C_d_in-  ppb or ug L-1 - this is the initial concentration of aqueous sorbate in the suspension
                C_s_in - g L-1 - this is the concentration of sorbent
                results_table- Sorbent Mass
                oder- The pseudo order of kinetic and the default is pseudo-second-order adsorption kinetic equation
                isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms


              Returns:
                   graphics

        """
    root = tk.Tk()
    # function_choose == 1 means continuous flow treatment
    if function_choose == 1:
        root.title('Breakthrough curves at influence concentration of %.1d ug/L.' % C_d_in)

    # function_choose == 2 means batch treatment
    elif function_choose == 2:
        root.title('Batch treatment using the concentration of %.1d ug/L adsorbent for 365 days .' % C_d_in)

    if num == 1:
        f = Figure(figsize=(8, 5), dpi=100)
        # Add sub diagram: 1st in 1 row and 1 column
        ax = f.add_subplot(111)

        # Plotting on the subplot obtained earlier
        ax.plot(time, results_table)
        ax.get_xaxis().get_major_formatter().set_scientific(False)

        if function_choose == 1:
            ax.set_title(
                'Breakthrough curves with %s adsorption isotherm and %d-order pseudo model' % (isotherms, oder))
            ax.set_xlabel('bed volumes treated')
        elif function_choose == 2:
            ax.set_title(
                'Batch treatment with %s adsorption isotherm and %d-order pseudo model' % (isotherms, oder))
            ax.set_xlabel('time (min)')

        ax.legend(labels=['Cs = %.1d g/L' % C_s_in], loc="center left")
        ax.set_xscale('log')
        ax.set_ylabel('As(aq) (ug/L)')

    # Display the drawing to tkinter: create a canvas belonging to root and place the drawing on the canvas
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP,  # Top Alignment
                                fill=tk.BOTH,  # Filling method
                                expand=tk.YES)  # Adjusts with window size

    # The navigation toolbar of matplotlib is shown up (it is not shown by default)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP,  # get_tk_widget() gets _tkcanvas
                          fill=tk.BOTH,
                          expand=tk.YES)

    def _quit():
        """This function is called when the exit button is clicked"""
        root.quit()  # Ending the main loop
        root.destroy()  # Destruction window

    # Create a button and bind the above function to it
    button = tk.Button(master=root, text="Exit", command=_quit)
    # Button on the bottom
    button.pack(side=tk.BOTTOM)

    # Main loop
    root.mainloop()


def Result_windows(isotherms, function_choose, progressbarOne, root):
    """
            Select the final result based on the user's options

            Parameters:
                isotherms- Adsorption isotherms and the default is Freundlich adsorption isotherms
                function_choose-Batch treatment or continue flow treatment
                progressbarOne - progressbar information from progress function


    """

    # Receive the value of Cin and assign it to C_in
    C_in = int(Cin.get())

    # Receive the value of Cs and assign it to C_s
    C_s = int(Cs.get())

    # Receive the value of var_order and assign it to oder
    oder = int(var_order.get())

    # Receive the value of k_in and assign it to k_i
    k_i = float(k_in.get())

    # Receive the value of n_in_er and assign it to n_er
    n_er = float(n_in_er.get())

    # Receive the value of KF_in_er and assign it to KF_er
    KF_er = float(KF_in_er.get())

    # Receive the value of k_in_er and assign it to k_er
    k_er = float(k_in_er.get())

    # Receive the value of KL_in_er and assign it to KL_er
    KL_er = float(KL_in_er.get())

    # Receive the value of Qmax_in_er and assign it to Qmax_er
    Qmax_er = float(Qmax_in_er.get())

    # Receive the value of KF_in and assign it to K_in
    K_in = float(KF_in.get())

    # Receive the value of n_in and assign it to n_i
    n_i = float(n_in.get())

    # Receive the value of Qmax_in and assign it to Q_max
    Q_max = float(Qmax_in.get())

    # Receive the value of KL_in and assign it to KL
    KL = float(KL_in.get())

    # Receive the value of people and assign it to peo
    peo = float(people.get())

    def but(time, res, iso, fc):

        """
            plot the plot effect of different reaction times
            on sorbate concentration in water under current conditions

            Parameters:
                time - raction sample time
                res - the concentration of sorbent
                fc-Batch treatment or continue flow treatment
                iso- Adsorption isotherms and the default is Freundlich adsorption isotherms

            Returns:
                graphics

        """
        # confirmation window
        a = tk.messagebox.askokcancel('Notice',
                                      "Need to plot effect of different reaction times on sorbate concentration "
                                      "in water under current conditions?")
        # draw image if user confirms
        if a:
            plot(time,
                 res, C_s,
                 C_in, iso, oder, fc)

    if function_choose == 1:      # continue flow treatment

        # Receive the value of j_in and assign it to jin
        jin = float(j_in.get())

        def plot_cf():
            # Create a window
            root = tk.Tk()
            # Create the title of window
            root.title('Adsorbents required to treatment')
            #  Call window size and position on screen
            root.geometry('850x880+300+0')

            # 3 subplots
            f, ax = plt.subplots(3, 1, figsize=(5, 4), dpi=100)
            k = [(k_i - k_er), k_i, (k_er + k_i)]
            results_table1 = [result_b_k, result, result_u_k]

            # Plotting on the subplot obtained earlier
            ax[0].plot(k, results_table1, color='y', linestyle=':', linewidth=2, marker='o',
                       markerfacecolor='blue', markersize=8)

            for a, b in zip(k, results_table1):
                ax[0].text(round(a, 3), round(b, 3), round(b, 3))

            ax[0].set_title('Effect of rate constants on adsorbent')
            ax[0].set_xlabel('rate constant ')
            ax[0].set_ylabel('sorbent need ')

            if isotherms == "Freundlich":
                # Plotting on the subplot obtained earlier
                KF1 = [ (K_in - KF_er), K_in, (K_in+KF_er)]
                results_table2 = [result_b_KF, result, result_u_KF]
                ax[1].plot(KF1, results_table2, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)

                for a, b in zip(KF1, results_table2):
                    ax[1].text(round(a, 3), round(b, 3), round(b, 3))
                ax[1].set_title('Effect of Freundlich parameters on adsorbent')
                ax[1].set_xlabel('Freundlich parameters ')
                ax[1].set_ylabel('sorbent need ')

                # Plotting on the subplot obtained earlier
                n = [(n_i - n_er), n_i, (n_i + n_er)]
                results_table3 = [result_b_n, result, result_u_n]
                ax[2].plot(n, results_table3, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)

                for a, b in zip(n, results_table3):
                    ax[2].text(round(a, 3), round(b, 3), round(b, 3))
                ax[2].set_title('Effect of parameters n on adsorbent')
                ax[2].set_xlabel('parameters n ')
                ax[2].set_ylabel('sorbent need ')

            elif isotherms == "Langmuir":

                # Plotting on the subplot obtained earlier
                KL_X = [ (KL - KL_er), KL, (KL+KL_er)]
                results_table2 = [result_b_KL, result, result_u_KL]
                ax[1].plot(KL_X, results_table2, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)

                for a, b in zip(KL_X, results_table2):
                    ax[1].text(round(a, 3), round(b, 3), round(b, 3))
                ax[1].set_title('Effect of Langmuir parameters on adsorbent')
                ax[1].set_xlabel('Langmuir parameters')
                ax[1].set_ylabel('sorbent need ')

                # Plotting on the subplot obtained earlier
                Qmax1 = [(Q_max - Qmax_er), Q_max, (Q_max + Qmax_er)]
                results_table3 = [result_b_Q, result, result_u_Q]
                ax[2].plot(Qmax1, results_table3, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)

                for a, b in zip(Qmax1, results_table3):
                    ax[2].text(round(a, 3), round(b, 3), round(b, 3))
                ax[2].set_title('Effect of Maximum adsorption capacity on adsorbent')
                ax[2].set_xlabel('Maximum adsorption capacity')
                ax[2].set_ylabel('sorbent need ')

            plt.tight_layout()

            # Display the drawing to tkinter: create a canvas belonging to root
            # and place the drawing on the canvas
            canvas_spice = FigureCanvasTkAgg(f, root)
            canvas_spice.draw()
            canvas_spice.get_tk_widget().pack(side=tkinter.TOP,
                                              fill=tkinter.BOTH,
                                              expand=tkinter.YES)

            # The navigation toolbar of matplotlib is shown up (it is not shown by default)
            toolbar = NavigationToolbar2Tk(canvas_spice, root)
            toolbar.update()
            canvas_spice._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
                                        fill=tkinter.BOTH,
                                        expand=tkinter.YES)

            def _quit():
                """This function is called when the exit button is clicked"""
                root.quit()  # Ending the main loop
                root.destroy()  # Destruction window

                # Create a button and bind the above function to it

            button = tk.Button(master=root, text="Exit", command=_quit)
            # Button on the bottom
            button.pack(side=tkinter.BOTTOM)

            # Main loop
            root.mainloop()

        if isotherms == "Freundlich":
            # data processing and  determine the adsorbent effective time for continue flow treatment
            results_table_cf, counter = Result_Processing_cf(j_flow=jin, C_inf=C_in, Cs0=C_s,  ord_in=oder,
                                                             k_in1=k_i, KF_in1=K_in, n_in1=n_i)

            # progress bar increase
            progressbarOne['value'] +=12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result, cs, day_need = Adsorbents_required(C_in1=C_in, Cs_in=C_s, j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                                       k_in1=k_i, KF_in1=K_in, n_in1=n_i)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_u_KF, cs_u_KF, day_need_u_KF = Adsorbents_required(C_in1=C_in, Cs_in=C_s, j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                                                      k_in1=k_i, KF_in1=(K_in+KF_er), n_in1=n_i)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_b_KF, cs_b_KF, day_need_b_KF = Adsorbents_required(C_in1=C_in, Cs_in=C_s, j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                                                      k_in1=k_i, KF_in1=(K_in-KF_er), n_in1=n_i)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_u_k, cs_u_k, day_need_u_k = Adsorbents_required(C_in1=C_in, Cs_in=C_s,
                                             j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                             k_in1=(k_i+k_er), KF_in1=K_in, n_in1=n_i)

            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_b_k, cs_b_k, day_need_b_k = Adsorbents_required(C_in1=C_in, Cs_in=C_s, j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                             k_in1=(k_i-k_er), KF_in1=K_in, n_in1=n_i)

            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_u_n, cs_u_n, day_need_u_n = Adsorbents_required(C_in1=C_in, Cs_in=C_s, j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                             k_in1=k_i, KF_in1=K_in, n_in1=n_i+n_er)

            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_b_n, cs_b_n, day_need_b_n = Adsorbents_required(C_in1=C_in, Cs_in=C_s, j_flow=jin, ord_in=oder, isotherms1=isotherms,
                                             k_in1=k_i, KF_in1=K_in, n_in1=n_i-n_er)

            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()

            # Wait 1.5 seconds to prevent the model from running too fast
            time.sleep(1.5)
            # remove root window
            root.destroy()

            # Create a window
            result_w = tk.Tk()
            # Create the title of window
            result_w.title('Sorbent efficiency ')
            #  Call window size and position on screen
            result_w.geometry('550x300+400+200')

            # Create text boxes
            tk.Label(result_w, text='Effect of rate constants on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=10)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per year ranges from %.2f kg to %.2f kg' % (cs,
                     result_u_k, result_b_k)
                     ).place(x=1, y=50)

            tk.Label(result_w, text='Effect of parameter n on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=80)

            # Create text boxes
            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per year ranges from %.2f kg to %.2f kg' % (cs,
                         result_u_n, result_b_n)
                     ).place(x=1, y=120)

            tk.Label(result_w, text='Effect of Freundlich parameters on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=150)

            # Create text boxes
            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per year ranges from %.2f kg to %.2f kg' % (cs,
                         result_u_KF, result_b_KF)
                     ).place(x=1, y=190)

        elif isotherms == "Langmuir":
            # data processing and  determine the adsorbent effective time for continue flow treatment
            results_table_cf, counter = Result_Processing_cf(j_flow=jin,
                                                             C_inf=C_in, Cs0=C_s,  ord_in=oder,
                                                             isotherms1=isotherms, k_in1=k_i, Qmax_in1=Q_max, KL_in1=KL)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result, cs, day_need = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s, ord_in=oder,
                                                       isotherms1=isotherms,
                                                       k_in1=k_i, Qmax_in1=Q_max, KL_in1=KL)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_u_k, cs_u_k, day_need_u_k = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s, ord_in=oder,
                                                                   isotherms1=isotherms,
                                                                   k_in1=(k_i+k_er), Qmax_in1=Q_max, KL_in1=KL)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # calculate the sorbent mass required for continue flow treatment
            result_b_k, cs_b_k, day_need_b_k = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s, ord_in=oder,
                                                                   isotherms1=isotherms,
                                                                   k_in1=(k_i-k_er), Qmax_in1=Q_max, KL_in1=KL)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()

            result_u_KL, cs_u_KL, day_need_u_KL = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s, ord_in=oder,
                                                                      isotherms1=isotherms,
                                                                      k_in1=k_i, Qmax_in1=Q_max, KL_in1=KL+KL_er)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()

            result_b_KL, cs_b_KL, day_need_b_KL = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s, ord_in=oder,
                                                                      isotherms1=isotherms,
                                                                      k_in1=k_i, Qmax_in1=Q_max, KL_in1=KL-KL_er)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()

            result_u_Q, cs_u_Q, day_need_u_Q = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s,
                                                                   ord_in=oder, isotherms1=isotherms,
                                                                   k_in1=k_i, Qmax_in1=Q_max+Qmax_er, KL_in1=KL)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()

            result_b_Q, cs_b_Q, day_need_b_Q = Adsorbents_required(C_in1=C_in, j_flow=jin, Cs_in=C_s, ord_in=oder,
                                                                   isotherms1=isotherms,
                                                                   k_in1=k_i, Qmax_in1=Q_max-Qmax_er, KL_in1=KL)
            # progress bar increase
            progressbarOne['value'] += 12.5
            # update window
            root.update()
            # Wait 1.5 seconds to prevent the model from running too fast
            time.sleep(1.5)
            # remove root window
            root.destroy()
            # creat a new window
            result_w = tk.Tk()
            # creat the title of window
            result_w.title('Sorbent efficiency ')
            #  Call window size and position on screen
            result_w.geometry('550x300+400+200')

            # creat the text label
            tk.Label(result_w, text='Effect of rate constants on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=10)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per year ranges from %.2f kg to %.2f kg' %(cs,
                                                                                                                result_u_k,
                                                                                                                result_b_k)
                     ).place(x=1, y=50)

            # creat the text label
            tk.Label(result_w, text='Effect of Langmuir parameters on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=80)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required '
                          'per year ranges from %.2f kg to %.2f kg' % (cs,
                                                                       result_u_KL,
                                                                       result_b_KL)
                     ).place(x=1, y=120)

            # creat the text label
            tk.Label(result_w, text='Effect of Maximum adsorption capacity on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=150)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per year ranges from %.2f kg to %.2f kg' % (cs,
                      result_u_Q, result_b_Q)
                     ).place(x=1, y=190)

        # Create button, Click the button to call the but function
        btn_plot1_cf = tk.Button(master=result_w,
                                 text='plot (time) ',
                                 command=lambda: [but(results_table_cf[0][0],
                                                      results_table_cf[0][1],
                                                      isotherms, 1)])

        # Create button, Click the button to call the plot_cf function
        btn_plot2_cf = tk.Button(master=result_w, text='plot results', command=plot_cf)

        btn_plot1_cf.place(x=230, y=250)
        btn_plot2_cf.place(x=100, y=250)

        # Create button, Click the button back to the main window
        # result_w.destroy() :  delete this window
        btn_Lan_back = tk.Button(result_w, text='Back',
                                 command=lambda: [result_w.destroy(), main_window()])

        btn_Lan_back.place(x=350, y=250)

        result_w.mainloop()

    elif function_choose == 2:    # batch treatment
        # Receive the value of days and assign it to day
        day = int(days.get())
        if isotherms == "Freundlich":

            # k_in=0.1111, KF_in=5.10, n_in=2.63
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct, Cs_F, data_collect, results_table_F = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                                                                      k_i, K_in, n_i)
            # progress bar increase
            progressbarOne['value'] += 7.143
            # update window
            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_n_u, Cs_F_n_u, data_collect_n_u, results_table_F_n_u \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          n_in=n_i + n_er, KF_in=K_in)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_n_b, Cs_F_n_b, data_collect_n_b, results_table_F_n_b \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          n_in=n_i - n_er, KF_in=K_in)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_k_u, Cs_F_k_u, data_collect_k_u, results_table_F_k_u \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i + k_er,
                                          n_in=n_i, KF_in=K_in)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_k_b, Cs_F_k_b, data_collect_k_b, results_table_F_k_b \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i - k_er,
                                          n_in=n_i, KF_in=K_in)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_KF_u, Cs_F_KF_u, data_collect_KF_u, results_table_F_KF_u \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          n_in=n_i, KF_in=K_in+KF_er)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_KF_b, Cs_F_KF_b, data_collect_KF_b, results_table_F_KF_b \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          n_in=n_i, KL_in=K_in - KL_er)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result, cs, day_need = Min_adsorbent_bt(results_table_F[-1], Cs_F, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_n_u, cs_n_u, day_need_n_u = Min_adsorbent_bt(results_table_F_n_u[-1], Cs_F_n_u, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_n_b, cs_n_b, day_need_n_b = Min_adsorbent_bt(results_table_F_n_b[-1], Cs_F_n_b, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_k_u, cs_k_u, day_need_k_u = Min_adsorbent_bt(results_table_F_k_u[-1], Cs_F_k_u, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_k_b, cs_k_b, day_need_k_b = Min_adsorbent_bt(results_table_F_k_b[-1], Cs_F_k_b, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_KF_u, cs_KF_u, day_need_KF_u = Min_adsorbent_bt(results_table_F_KF_u[-1], Cs_F_KF_u, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_KF_b, cs_KF_b, day_need_KF_b = Min_adsorbent_bt(results_table_F_KF_b[-1], Cs_F_KF_b, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # Wait 0.5 seconds to prevent the model from running too fast
            time.sleep(0.5)
            # remove root window
            root.destroy()
            # creat new window
            result_w = tk.Tk()
            # creat window title
            result_w.title('Sorbent efficiency ')
            #  Call window size and position on screen
            result_w.geometry('550x330+400+200')
            # Create text boxes
            tk.Label(result_w, text='Effect of rate constants on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=10)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per %d days ranges from %.2f kg to %.2f kg' % (cs,day,
                                                                                                           result_k_u,
                                                                                                           result_k_b)
                     ).place(x=1, y=50)

            tk.Label(result_w, text='Effect of Freundlich parameters on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=80)
            # Create text boxes
            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per %d days ranges from %.2f kg to %.2f kg' % (cs,day,
                                                                                                           result_KF_u,
                                                                                                           result_KF_b)
                     ).place(x=1, y=120)

            tk.Label(result_w, text='Effect of parameters n on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=150)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per %d days ranges from %.2f kg to %.2f kg' % (cs,day,
                                                                                                           result_n_u,
                                                                                                           result_n_b)
                     ).place(x=1, y=190)

        elif isotherms == "Langmuir":
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct, Cs_L, data_collect, results_table_L = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                                                                      k_i,
                                                                                      Qmax_in=Q_max, KL_in=KL)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_Q_u, Cs_L_Q_u, data_collect_Q_u, results_table_L_Q_u \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          Qmax_in=Q_max+Qmax_er, KL_in=KL)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_Q_b, Cs_L_Q_b, data_collect_Q_b, results_table_L_Q_b \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          Qmax_in=Q_max-Qmax_er, KL_in=KL)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_k_u, Cs_L_k_u, data_collect_k_u, results_table_L_k_u\
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i+k_er,
                                          Qmax_in=Q_max, KL_in=KL)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_k_b, Cs_L_k_b, data_collect_k_b, results_table_L_k_b \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i-k_er,
                                          Qmax_in=Q_max, KL_in=KL)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_KL_u, Cs_L_KL_u, data_collect_KL_u, results_table_L_KL_u \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          Qmax_in=Q_max, KL_in=KL)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # data processing and  determine the adsorbent effective time for batch treatment
            results_Ct_KL_b, Cs_L_KL_b, data_collect_KL_b, results_table_L_KL_b \
                = Result_Processing_batch(C_in, C_s, day, oder, isotherms,
                                          k_i,
                                          Qmax_in=Q_max, KL_in=KL-KL_er)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result, cs, day_need = Min_adsorbent_bt(results_table_L[-1], Cs_L, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_Q_u, cs_Q_u, day_need_Q_u = Min_adsorbent_bt(results_table_L_Q_u[-1], Cs_L_Q_u, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_Q_b, cs_Q_b, day_need_Q_b = Min_adsorbent_bt(results_table_L_Q_b[-1], Cs_L_Q_b, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()

            # calculate the sorbent mass required for batch treatment
            result_k_u, cs_k_u, day_need_k_u = Min_adsorbent_bt(results_table_L_k_u[-1], Cs_L_k_u, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_k_b, cs_k_b, day_need_k_b = Min_adsorbent_bt(results_table_L_k_b[-1], Cs_L_k_b, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_KL_u, cs_KL_u, day_need_KL_u = Min_adsorbent_bt(results_table_L_KL_u[-1], Cs_L_KL_u, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # calculate the sorbent mass required for batch treatment
            result_KL_b, cs_KL_b, day_need_KL_b = Min_adsorbent_bt(results_table_L_KL_b[-1], Cs_L_KL_b, day, peo)
            # progress bar increase
            progressbarOne['value'] += 7.143

            root.update()
            # Wait 0.5 seconds to prevent the model from running too fast
            time.sleep(0.5)
            # remove root window
            root.destroy()
            # creat new window
            result_w = tk.Tk()
            # creat title of window
            result_w.title('Sorbent efficiency ')
            #  Call window size and position on screen
            result_w.geometry('550x330+400+200')
            # Create text boxes
            tk.Label(result_w, text='Effect of rate constants on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=10)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per %d days ranges from %.2f kg to %.2f kg' % (cs,day,
                                                                                                           result_k_u,
                                                                                                           result_k_b)
                     ).place(x=1, y=50)
            # Create text boxes
            tk.Label(result_w, text='Effect of Langmuir parameters on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=80)

            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per %d days ranges from %.2f kg to %.2f kg' % (cs,day,
                                                                                                           result_KL_u,
                                                                                                           result_KL_b)
                     ).place(x=1, y=120)

            tk.Label(result_w, text='Effect of Maximum adsorption capacity on adsorbent ',
                     bg='green', font=('Arial', 10), width=50,
                     height=2).place(x=1, y=150)
            # Create text boxes
            tk.Label(result_w,
                     text='The amount of absorbent (%d g/L) required per %d days ranges from %.2f kg to %.2f kg' % (cs,day,
                                                                                                           result_Q_u,
                                                                                                           result_Q_b)
                     ).place(x=1, y=190)

        def plot_bt():
            # creat a new window
            root = tk.Tk()
            # creat the window title
            root.title('Adsorbents required to treatment')
            root.geometry('850x880+300+0')

            # 3 subplots
            f, ax = plt.subplots(3, 1, figsize=(5, 4), dpi=100)

            # Plotting on the subplot obtained earlier
            k = [(k_i - k_er), k_i, (k_er + k_i)]
            results_table1 = [result_k_b, result, result_k_u]
            ax[0].plot(k, results_table1, color='y', linestyle=':', linewidth=2, marker='o',
                       markerfacecolor='blue', markersize=8)
            for a, b in zip(k, results_table1):
                ax[0].text(round(a, 3), round(b, 3), round(b, 3))
            ax[0].set_title('Effect of rate constants on adsorbent')
            ax[0].set_xlabel('rate constant ')
            ax[0].set_ylabel('sorbent need ')

            if isotherms == "Freundlich":

                # Plotting on the subplot obtained earlier
                KF1 = [(K_in - KF_er), K_in, (K_in + KF_er)]
                results_table2 = [result_KF_b, result, result_KF_u]
                ax[1].plot(KF1, results_table2, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)

                for a, b in zip(KF1, results_table2):
                    ax[1].text(round(a, 3), round(b, 3), round(b, 3))
                ax[1].set_title('Effect of Freundlich parameters on adsorbent')
                ax[1].set_xlabel('Freundlich parameters ')
                ax[1].set_ylabel('sorbent need ')

                # Plotting on the subplot obtained earlier
                n = [(n_i - n_er), n_i, (n_i + n_er)]
                results_table3 = [result_n_b, result, result_n_u]
                ax[2].plot(n, results_table3, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)
                for a, b in zip(n, results_table3):
                    ax[2].text(round(a, 3), round(b, 3), round(b, 3))
                ax[2].set_title('Effect of parameters n on adsorbent')
                ax[2].set_xlabel('parameters n ')
                ax[2].set_ylabel('sorbent need ')

            elif isotherms == "Langmuir":

                # Plotting on the subplot obtained earlier
                KL_X = [(KL - KL_er), KL, (KL + KL_er)]
                results_table2 = [result_KL_b, result, result_KL_u]
                ax[1].plot(KL_X, results_table2, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)
                for a, b in zip(KL_X, results_table2):
                    ax[1].text(round(a, 3), round(b, 3), round(b, 3))
                ax[1].set_title('Effect of Langmuir parameters on adsorbent')
                ax[1].set_xlabel('Langmuir parameters')
                ax[1].set_ylabel('sorbent need ')

                # Plotting on the subplot obtained earlier
                Qmax1 = [(Q_max - Qmax_er), Q_max, (Q_max + Qmax_er)]
                results_table3 = [result_Q_b, result, result_Q_u]
                ax[2].plot(Qmax1, results_table3, color='y', linestyle=':', linewidth=2, marker='o',
                           markerfacecolor='blue', markersize=8)

                for a, b in zip(Qmax1, results_table3):
                    ax[2].text(round(a, 3), round(b, 3), round(b, 3))

                ax[2].set_title('Effect of Maximum adsorption capacity on adsorbent')
                ax[2].set_xlabel('Maximum adsorption capacity')
                ax[2].set_ylabel('sorbent need ')

            plt.tight_layout()
            # Display the drawing to tkinter: create a canvas belonging to root and place the drawing on the canvas
            canvas_spice = FigureCanvasTkAgg(f, root)
            canvas_spice.draw()
            canvas_spice.get_tk_widget().pack(side=tkinter.TOP,
                                              fill=tkinter.BOTH,
                                              expand=tkinter.YES)

            # The navigation toolbar of matplotlib is shown up (it is not shown by default)
            toolbar = NavigationToolbar2Tk(canvas_spice, root)
            toolbar.update()
            canvas_spice._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()
                                        fill=tkinter.BOTH,
                                        expand=tkinter.YES)

            def _quit():
                """This function is called when the exit button is clicked"""
                root.quit()  # Ending the main loop
                root.destroy()  # Destruction window

                # Create a button and bind the above function to it

            button = tk.Button(master=root, text="Exit", command=_quit)
            # Button on the bottom
            button.pack(side=tkinter.BOTTOM)

            # Main loop
            root.mainloop()

        # Create button, Click the button to call the plot_bt function
        btn_plot1_bt = tk.Button(master=result_w, text='plot(time)',
                                 command=lambda: [but(data_collect[1:],
                                                  results_Ct[4][1:],
                                                  isotherms, 2)])

        # Create button, Click the button to call the plot_bt function
        btn_plot2_bt = tk.Button(master=result_w, text='plot results', command=plot_bt)

        btn_plot1_bt.place(x=230, y=250)
        btn_plot2_bt.place(x=100, y=250)

        # Create button, Click the button back to the main window
        # result_w.destroy() :  delete this window
        btn_Lan_back = tk.Button(result_w, text='Back', command=lambda: [result_w.destroy(), main_window()])
        btn_Lan_back.place(x=350, y=250)
        result_w.mainloop()


main_window()






