from tkinter import *

window = Tk()
window.title('BMI Calculator')
window.geometry('400x300')

bmi_label = Label(window)
Label(window, text="Enter your height in m:", fg='blue').grid(row=0, column=0)
Label(window, text="Enter your weight in kg:", fg='blue').grid(row=1, column=0)

height = StringVar()
weight = StringVar()

Entry(window, textvariable=height).grid(row=0, column=1)
Entry(window, textvariable=weight).grid(row=1, column=1)


def bmi_calculator():
    global bmi_label
    bmi_label.destroy()
    person_height = float(height.get())
    person_weight = float(weight.get())
    message = 'Your BMI is:'
    result = round(person_weight / (person_height ** 2), 1)
    message += str(result)
    if result < 18.5:
        message += ' (Underweight)'
    elif result < 25:
        message += ' (Normal)'
    elif result < 30:
        message += ' (Overweight)'
    else:
        message += ' (Obesity)'
    bmi_label = Label(window, text=message, fg='green' if result < 25 else 'red')
    bmi_label.grid(row=3, column=1)


Button(window, text='Calculate your BMI', command=bmi_calculator, fg='blue', bg='white').grid(row=2, column=1)

window.mainloop()
