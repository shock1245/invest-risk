from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import numpy as np
import matplotlib.pyplot as plt
from tkinter.messagebox import showerror

base_parameters = {}

#### Функции расчета ####

def set_weight(x1, x2, x3, x4, x5, x6, x7, x8):
    global economic_weight, techno_weight, politic_weight, market_weight, finance_weight, operation_weight, social_weight, other_weight
    economic_weight = 0.0
    techno_weight = 0.0
    politic_weight = 0.0
    market_weight = 0.0
    finance_weight = 0.0
    operation_weight = 0.0
    social_weight = 0.0
    other_weight = 0.0
    economic_weight = x1
    techno_weight = x2
    politic_weight = x3
    market_weight = x4
    finance_weight = x5
    operation_weight = x6
    social_weight = x7
    other_weight = x8


def input_expert_data():
    global economic_factors, techno_factors, politic_factors, market_factors, finance_factors, operation_factors, social_factors, other_factors
    economic_factors = []
    techno_factors = []
    politic_factors = []
    market_factors = []
    finance_factors = []
    operation_factors = []
    social_factors = []
    other_factors = []
    if selected_industry.get() == 1:
        set_weight(1.3, 1.4, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7)
    elif selected_industry.get() == 2:
        set_weight(1.3, 1.4, 1.1, 1.2, 1.0, 0.9, 0.8, 0.7)
    elif selected_industry.get() == 3:
        set_weight(1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7)
    elif selected_industry.get() == 4:
        set_weight(1.2, 1.3, 1.1, 1.4, 1.0, 0.9, 0.8, 0.7)
    elif selected_industry.get() == 5:
        set_weight(1.3, 1.4, 1.1, 1.2, 1.0, 0.9, 0.8, 0.7)
    economic_factors.append(ef_text.get(1.0, "end").split(','))
    techno_factors.append(tf_text.get(1.0, "end").split(','))
    politic_factors.append(pf_text.get(1.0, "end").split(','))
    market_factors.append(mf_text.get(1.0, "end").split(','))
    finance_factors.append(ff_text.get(1.0, "end").split(','))
    operation_factors.append(of_text.get(1.0, "end").split(','))
    social_factors.append(sf_text.get(1.0, "end").split(','))
    other_factors.append(othf_text.get(1.0, "end").split(','))


def calculate_expert_risk():
    risk = 0
    factors = [economic_factors, techno_factors, politic_factors, market_factors, finance_factors, operation_factors,
               social_factors, other_factors]
    weights = [economic_weight, techno_weight, politic_weight, market_weight, finance_weight, operation_weight,
               social_weight, other_weight]
    for i in range(8):
        if factors[i][0][0] != "\n":
            risk += (len(factors[i][0]) * weights[i])
    return round(risk)


def calculate_npv(parameters):
    global time, first_invest, discount_rate, fixed_cf
    npv = 0
    cash_flow = 0
    #cash_flow_list = []
    #dummy_list = []
    time = int(text_time.get(1.0, "end"))
    first_invest = int(text_first_invest.get(1.0, "end"))
    discount_rate = int(text_discount_rate.get(1.0, "end")) / 100
    #if fixed_cf:
    for parameter in parameters.values():
        cash_flow += int(parameter)
    discount_first_invest = first_invest / (1 + discount_rate) ** 0
    for i in range(1, time + 1):
        npv += cash_flow / (1 + discount_rate) ** i
    npv -= discount_first_invest
    #else:
    #    for parameter in parameters.values():
    #        if not isinstance(parameter, list):
    #           cash_flow += int(parameter)
    #        else:
    #            dummy_list.append(parameter)
    #    for i in range(0, time):
    #        j = 0
    #        a = 0
    #        while j < len(dummy_list):
    #            a += dummy_list[j][i]
    #            j = j + 1
    #        cash_flow_list.append(a + cash_flow)
    #    discount_first_invest = first_invest / (1 + discount_rate) ** 0
    #    for i, cashflow in enumerate(cash_flow_list):
    #        npv += cashflow / (1 + discount_rate) ** i
    #    npv -= discount_first_invest
    return npv


def sensetivity_analysis():
    global npv_result
    npv_result = {}
    for key in base_parameters.keys():
        modified_base_parameters = base_parameters.copy()
        modified_parameters = []
        dummy_list = []
        dummy_dict = {}
        a = calculate_npv(base_parameters)
        if not isinstance(base_parameters.get(key), list):
            for i in np.arange(0.8, 1.3, 0.1):
                modified_parameters.append(int(base_parameters.get(key)) * i)
            # print(modified_parameters)
            i = 0.8
            for modified_parameter in modified_parameters:
                percentage_difference = 0
                modified_base_parameters.update({key: modified_parameter})
                b = calculate_npv(modified_base_parameters)
                if (a > b) and (a > 0) and (b > 0):
                    percentage_difference = ((a - b) / a * 100)
                elif (a < b) and (a > 0) and (b > 0):
                    percentage_difference = ((b - a) / a * 100)
                elif (a > b) and (a < 0) and (b < 0):
                    percentage_difference = ((a - b) / abs(a) * 100)
                elif (a < b) and (a < 0) and (b < 0):
                    percentage_difference = ((b - a) / abs(a) * 100)
                elif (a > b) and (b < 0):
                    percentage_difference = ((a - b) / -a * 100)
                elif (a < b) and (a < 0):
                    percentage_difference = ((b - a) / a * 100)
                elif a == b:
                    percentage_difference = 0
                dummy_dict.update({f"{round(i * 100 - 100)}%": [round(int(base_parameters.get(key)) * i),
                                                                round(calculate_npv(modified_base_parameters)),
                                                                f"{round(percentage_difference)}%"]})
                i += 0.1
            npv_result.update({key: dummy_dict})
        else:
            for i in np.arange(0.8, 1.3, 0.1):
                if i != 1:
                    for j in base_parameters.get(key):
                        dummy_list.append(int(j) * i)
                    modified_parameters.append(dummy_list)
                    dummy_list = []
            for modified_parameter in modified_parameters:
                modified_base_parameters.update({key: modified_parameter})

#### Конец Функции расчета ####

#### Пользовательский интерфейс ####

def main_window():
    global enable_sens_analysis, enable_expert_analysis, main_root

    main_root = Tk()
    main_root.title("Приложение")
    main_root.resizable(False, False)
    main_root.geometry("400x300")

    frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    frame.pack(anchor=NW, fill=BOTH, padx=5, pady=5, expand=True)

    label_about = ttk.Label(frame, text="О программе")
    label_about.place(x=260, y=30)

    label_about2 = ttk.Label(frame,
                             text="Данная программа используется для оценки риска инвестициооного проекта на основе "
                                  "введенных пользователем данных. Для оценки риска используются методы анализа "
                                  "чувствительности и экспертной оценки.", wraplength=150, justify=CENTER)
    label_about2.place(x=225, y=70)

    label_analysis_type = ttk.Label(frame, text="Выберите необходимые методы: ")
    label_analysis_type.place(x=15, y=50)

    enable_sens_analysis = BooleanVar()
    checkbutton1 = ttk.Checkbutton(text="Анализ чувствительности", variable=enable_sens_analysis, onvalue=True,
                                   offvalue=False)
    checkbutton1.place(x=30, y=100)

    enable_expert_analysis = BooleanVar()
    checkbutton2 = ttk.Checkbutton(text="Экспертный анализ", variable=enable_expert_analysis, onvalue=True,
                                   offvalue=False)
    checkbutton2.place(x=30, y=130)

    btn_next = ttk.Button(text="Далее", command=to_analysis)
    btn_next.place(x=300, y=250)

    main_root.mainloop()


def to_analysis():
    if enable_expert_analysis.get() is True:
        main_root.destroy()
        expert_analysis_input_data_window()

    if (enable_sens_analysis.get() is True) and (enable_expert_analysis.get() is False):
        main_root.destroy()
        sens_analysis_input_data_window()

    if (enable_expert_analysis.get() is False) and (enable_sens_analysis.get() is False):
        showerror(title="Ошибка", message="Выберите один или несколько методов анализа")

def expert_analysis_input_data_window():
    global selected_industry, ef_text, tf_text, pf_text, mf_text, ff_text, of_text, sf_text, othf_text, expert_window
    # main_root.destroy()

    expert_window = Tk()
    expert_window.title("Экспертный анализ")
    expert_window.resizable(False, False)
    expert_window.geometry("550x980")

    frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    for c in range(2): frame.columnconfigure(index=c, weight=1)
    for r in range(4): frame.rowconfigure(index=r, weight=1)

    label = ttk.Label(frame, text="Выберите желаемую отрасль:")
    label.grid(row=0, column=0, columnspan=2)

    selected_industry = IntVar(value=1)

    rbtn1 = ttk.Radiobutton(frame, text="Нефтегазовая промышленность", value=1, variable=selected_industry)
    rbtn1.grid(row=1, column=0)

    rbtn2 = ttk.Radiobutton(frame, text="Автомобильная промышленность", value=2, variable=selected_industry)
    rbtn2.grid(row=2, column=0)

    rbtn3 = ttk.Radiobutton(frame, text="Производство металлов", value=3, variable=selected_industry)
    rbtn3.grid(row=3, column=0)

    rbtn4 = ttk.Radiobutton(frame, text="Пищевая промышленность", value=4, variable=selected_industry)
    rbtn4.grid(row=1, column=1)

    rbtn5 = ttk.Radiobutton(frame, text="Химическая промышленность", value=5, variable=selected_industry)
    rbtn5.grid(row=2, column=1)

    ef_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    ef_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    ef_label = ttk.Label(ef_frame, text="Введите список рисков, связанных с экономическими факторами (через запятую)")
    ef_label.pack(anchor=NW)

    ef_text = ScrolledText(ef_frame, height=3, wrap="word")
    ef_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    tf_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    tf_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    tf_label = ttk.Label(tf_frame, text="Введите список рисков, связанных с технологическими факторами")
    tf_label.pack(anchor=NW)

    tf_text = ScrolledText(tf_frame, height=3, wrap="word")
    tf_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    pf_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    pf_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    pf_label = ttk.Label(pf_frame, text="Введите список рисков, связанных с политическими факторами")
    pf_label.pack(anchor=NW)

    pf_text = ScrolledText(pf_frame, height=3, wrap="word")
    pf_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    mf_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    mf_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    mf_label = ttk.Label(mf_frame, text="Введите список рисков, связанных с рыночными факторами")
    mf_label.pack(anchor=NW)

    mf_text = ScrolledText(mf_frame, height=3, wrap="word")
    mf_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    ff_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    ff_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    ff_label = ttk.Label(ff_frame, text="Введите список рисков, связанных с финансовыми факторами")
    ff_label.pack(anchor=NW)

    ff_text = ScrolledText(ff_frame, height=3, wrap="word")
    ff_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    of_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    of_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    of_label = ttk.Label(of_frame, text="Введите список рисков, связанных с операционными факторами")
    of_label.pack(anchor=NW)

    of_text = ScrolledText(of_frame, height=3, wrap="word")
    of_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    sf_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    sf_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    sf_label = ttk.Label(sf_frame, text="Введите список рисков, связанных с социальными факторами")
    sf_label.pack(anchor=NW)

    sf_text = ScrolledText(sf_frame, height=3, wrap="word")
    sf_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    othf_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    othf_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    othf_label = ttk.Label(othf_frame, text="Введите список рисков, связанных с другими факторами")
    othf_label.pack(anchor=NW)

    othf_text = ScrolledText(othf_frame, height=3, wrap="word")
    othf_text.pack(anchor=NW, fill=X, side=LEFT, expand=True)

    btn_result = ttk.Button(text="Далее", command=button_click_next)
    btn_result.pack(anchor=NE, padx=10, pady=5)

    expert_window.mainloop()


def sens_analysis_input_data_window():
    global text_time, text_first_invest, text_discount_rate, entry_name, entry_value, listbox, sens_window

    sens_window = Tk()
    sens_window.title("Анализ чувствительности")
    sens_window.resizable(False, False)
    sens_window.geometry("420x430")

    frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    frame.pack(anchor=NW, fill=X, padx=5, pady=5)

    label_time = ttk.Label(frame, text="Введите время реализации проекта")
    label_time.pack(anchor=NW)

    text_time = Text(frame, height=1, width=12)
    text_time.pack(anchor=NW)

    label_first_invest = ttk.Label(frame, text="Введите значение первоначальных инвестиций")
    label_first_invest.pack(anchor=NW)

    text_first_invest = Text(frame, height=1, width=12)
    text_first_invest.pack(anchor=NW)

    label_discount_rate = ttk.Label(frame, text="Введите значение ставки дисконтирования (в процентах)")
    label_discount_rate.pack(anchor=NW)

    text_discount_rate = Text(frame, height=1, width=12)
    text_discount_rate.pack(anchor=NW)

    frame2 = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    frame2.pack(anchor=NW, fill=X, padx=5, pady=5)

    for c in range(2): frame2.columnconfigure(index=c, weight=1)
    for r in range(6): frame2.rowconfigure(index=r, weight=1)

    label_title = ttk.Label(frame2,
                            text="Ввод денежных потоков",
                            wraplength=400, justify=CENTER)
    label_title.grid(row=0, column=0, columnspan=2, pady=[3, 20])

    label_name = ttk.Label(frame2, text="Имя параметра")
    label_name.grid(row=1, column=1, sticky=W)

    label_value = ttk.Label(frame2, text="Значение параметра", wraplength=100)
    label_value.grid(row=3, column=1, sticky=W)

    entry_name = Entry(frame2)
    entry_name.grid(row=2, column=1, sticky=W)

    entry_value = Entry(frame2)
    entry_value.grid(row=4, column=1, sticky=W)

    listbox = Listbox(frame2, width=30)
    listbox.grid(row=1, column=0, rowspan=5)

    btn_add_parameter = ttk.Button(frame2, text="Добавить параметр", command=add_parameter)
    btn_add_parameter.grid(row=5, column=1, sticky=W)

    btn_next = ttk.Button(text="Далее", command=button_result_output)
    btn_next.place(x=330, y=400)

    sens_window.mainloop()


def button_click_next():
    global expert_risk
    input_expert_data()
    expert_risk = calculate_expert_risk()
    if expert_risk == 0:
        showerror(title="Ошибка", message="Заполните как минимум одно поле")
    else:
        expert_window.destroy()
        if (enable_expert_analysis.get() is True) and (enable_sens_analysis.get() is True):
            sens_analysis_input_data_window()
        if (enable_expert_analysis.get() is True) and (enable_sens_analysis.get() is False):
            button_result_output()


def button_result_output():

    if (enable_expert_analysis.get() is True) and (enable_sens_analysis.get() is True):
        sensetivity_analysis()
        if npv_result == {}:
            showerror(title="Ошибка", message="Заполните все поля в окне")
        else:
            sens_window.destroy()
            result_window = Tk()
            result_window.title("Результат")
            result_window.resizable(False, False)
            result_window.geometry("370x570")

            upper_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
            upper_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

            label = ttk.Label(upper_frame, text="Значение оценки риска экспертным методом составляет: ")
            label.pack(anchor=N)

            label_expert_risk = ttk.Label(upper_frame, text=expert_risk, font=("Arial", 30), foreground="red")
            label_expert_risk.pack(anchor=N)

            label_sens_analysis = ttk.Label(text="Анализ чувствительности параметров инвестиционного проекта")
            label_sens_analysis.pack(anchor=N)

            canvas = Canvas()
            lower_frame = ttk.Frame(canvas, borderwidth=1, relief=SOLID, padding=[8, 10])
            scrollbar = Scrollbar(orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", pady=[10, 40], expand=True)
            canvas.create_window((4, 4), window=lower_frame, anchor="nw")

            for i, key in enumerate(npv_result.keys()):
                create_frame(key, i, lower_frame)

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            graph_button = ttk.Button(result_window, text="Показать график", command=graph)
            graph_button.place(x=10, y=545)

            result_window.mainloop()

    if (enable_expert_analysis.get() is True) and (enable_sens_analysis.get() is False):
        result_window = Tk()
        result_window.title("Результат")
        result_window.resizable(False, False)
        result_window.geometry("370x100")

        upper_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        upper_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

        label = ttk.Label(upper_frame, text="Значение оценки риска экспертным методом составляет: ")
        label.pack(anchor=N)

        label_expert_risk = ttk.Label(upper_frame, text=expert_risk, font=("Arial", 30), foreground="red")
        label_expert_risk.pack(anchor=N)

        result_window.mainloop()

    if (enable_expert_analysis.get() is False) and (enable_sens_analysis.get() is True):
        sensetivity_analysis()
        if npv_result == {}:
            showerror(title="Ошибка", message="Заполните все поля в окне")
        else:
            sens_window.destroy()
            result_window = Tk()
            result_window.title("Результат")
            result_window.resizable(False, False)
            result_window.geometry("370x450")

            label_sens_analysis = ttk.Label(text="Анализ чувствительности параметров инвестиционного проекта")
            label_sens_analysis.pack(anchor=N)

            canvas = Canvas()
            lower_frame = ttk.Frame(canvas, borderwidth=1, relief=SOLID, padding=[8, 10])
            scrollbar = Scrollbar(orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((4, 4), window=lower_frame, anchor="nw")
            # lower_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

            for i, key in enumerate(npv_result.keys()):
                create_frame(key, i, lower_frame)

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            result_window.mainloop()



def create_frame(key, index, lower_frame):
    globals()['frame' + str(index)] = ttk.Frame(lower_frame, borderwidth=1, relief=SOLID, padding=[8, 10])
    globals()['frame' + str(index)].pack(anchor=NW, fill=X, padx=5, pady=5)

    for c in range(5): globals()['frame' + str(index)].columnconfigure(index=c, weight=1)
    for r in range(7): globals()['frame' + str(index)].rowconfigure(index=r, weight=1)

    globals()['label_param_name' + str(index)] = ttk.Label(globals()['frame' + str(index)], text=key, wraplength=100)
    globals()['label_param_name' + str(index)].grid(row=0, column=0, columnspan=7)

    globals()['label_percent' + str(index)] = ttk.Label(globals()['frame' + str(index)], text="Изменение параметра",
                                                        wraplength=100)
    globals()['label_percent' + str(index)].grid(row=1, column=0)

    globals()['label_param' + str(index)] = ttk.Label(globals()['frame' + str(index)], text="Значение параметра",
                                                      wraplength=100)
    globals()['label_param' + str(index)].grid(row=1, column=1)

    globals()['label_npv' + str(index)] = ttk.Label(globals()['frame' + str(index)], text="Значение NPV",
                                                    wraplength=100)
    globals()['label_npv' + str(index)].grid(row=1, column=2)

    globals()['label_diff' + str(index)] = ttk.Label(globals()['frame' + str(index)], text="Изменение NPV")
    globals()['label_diff' + str(index)].grid(row=1, column=3)

    k = npv_result.get(key)
    for i, key2 in enumerate(k.keys()):
        globals()['label_percent1' + str(index)] = ttk.Label(globals()['frame' + str(index)], text=key2, wraplength=100)
        globals()['label_percent1' + str(index)].grid(row=i + 2, column=0)

        globals()['label_param1' + str(index)] = ttk.Label(globals()['frame' + str(index)], text=k.get(key2)[0],
                                                           wraplength=100)
        globals()['label_param1' + str(index)].grid(row=i + 2, column=1)

        globals()['label_npv1' + str(index)] = ttk.Label(globals()['frame' + str(index)], text=k.get(key2)[1],
                                                         wraplength=100)
        globals()['label_npv1' + str(index)].grid(row=i + 2, column=2)

        globals()['label_diff1' + str(index)] = ttk.Label(globals()['frame' + str(index)], text=k.get(key2)[2])
        globals()['label_diff1' + str(index)].grid(row=i + 2, column=3)


def graph():
    xvalues = [-20, -10, 0, 10, 20]
    for key in npv_result.keys():
        yvalues = []
        k = npv_result.get(key)
        for key2 in k.keys():
            yvalues.append(k.get(key2)[1])
        plt.plot(xvalues, yvalues, label=key, marker='s')
    plt.xlabel('Процентное изменение параметра')
    plt.ylabel('NPV')
    plt.title('Анализ чувствительности')
    plt.legend()
    plt.grid(True)
    plt.show()

#### Конец пользовательского интерфеса ####



#### Другие функции ####

def add_parameter():
    #global fixed_cf
    found_key = False
    en = entry_name.get()
    ev = entry_value.get()
    if base_parameters == {}:
        listbox.insert(END, f"{en} - {ev}")
        base_parameters.update({en: ev})
    else:
        for key in base_parameters.keys():
            if en == key:
                found_key = True
                for i, element in enumerate(listbox.get(0, END)):
                    if element.find(en) != -1:
                        listbox.delete(i)
                        listbox.insert(i, f"{en} - {ev}")
                        base_parameters.update({en: ev})
    #if entry_value.get().find(",") == -1:
        if found_key is False:
            listbox.insert(END, f"{en} - {ev}")
            base_parameters.update({en: ev})
        #fixed_cf = True
    #else:
    #    base_parameters.update({entry_name.get(): entry_value.get().split(",")})
    #    fixed_cf = False

#### Конец Другие функции ####

main_window()