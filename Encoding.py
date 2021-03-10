from tkinter import *
from tkinter import messagebox
from encodelib import *


def encode_and_show():
    outbox.config(state="normal")
    outbox1.config(state="normal")
    outbox2.config(state="normal")
    normal_key.config(state="normal")
    complex_key.config(state="normal")
    in_text = input_box.get(1.0, "end-1c")
    encoded_simple = begin(in_text, "e")
    encoded_complex = begin(in_text, "ec")
    outbox.delete(1.0, END)
    outbox.insert(1.0, encoded_simple[0])
    normal_key.delete(1.0, "end-1c")
    normal_key.insert(1.0, encoded_simple[1])
    outbox1.delete(1.0, END)
    outbox1.insert(1.0, encoded_complex[0])
    complex_key.delete(1.0, "end-1c")
    complex_key.insert(1.0, str(encoded_complex[1]).strip("[]").replace(", ", ",") + "\n" + str(encoded_complex[2]) +
                       "\n" + str(encoded_complex[3]))
    if in_text.__len__() > 25:
        complex_key.config(width=50)
    else:
        complex_key.config(width=in_text.__len__() * 2 - 1)
    outbox2.delete(1.0, END)
    outbox2.insert(1.0, b64e(in_text.encode()).decode())
    outbox.config(state="disabled")
    outbox1.config(state="disabled")
    outbox2.config(state="disabled")
    normal_key.config(state="disabled")
    complex_key.config(state="disabled")


def decode_and_show():
    decode_outbox.config(state="normal")
    decode_outbox.delete(1.0, "end-1c")
    extra_info_s = decode_extra_info.get(1.0, "end-1c")
    if extra_info_s.strip() == "" and current_decode_choice.get() != "Base64":
        messagebox.showerror(title="Decoding error", message="Wrong decoding type! Did you mean Base64?")
        current_decode_choice.set("Base64")
        return
    elif extra_info_s.split("\n").__len__() == 3 and current_decode_choice.get() != "Complex":
        messagebox.showerror(title="Decoding error", message="Wrong decoding type! Did you mean Complex?")
        current_decode_choice.set("Complex")
        return
    elif extra_info_s.split("\n").__len__() == 1 and current_decode_choice.get() != "Normal" and extra_info_s.strip() \
            != "":
        messagebox.showerror(title="Decoding error", message="Wrong decoding type! Did you mean Normal?")
        current_decode_choice.set("Normal")
        return
    if current_decode_choice.get() == "Normal":
        key = int(extra_info_s)
        decode_outbox.insert(1.0, begin(input_d_box.get(1.0, "end-1c"), "d"), key)
    elif current_decode_choice.get() == "Complex":
        scrambled_nums_list = [int(i) for i in extra_info_s.split("\n")[0].split(",")]
        scramble_key = int(extra_info_s.split("\n")[1])
        key = int(extra_info_s.split("\n")[2])
        decode_outbox.insert(1.0, begin(input_d_box.get(1.0, "end-1c"), "dc", scrambled_nums_list, scramble_key, key))
    elif current_decode_choice.get() == "Base64":
        decode_outbox.insert(1.0, begin(input_d_box.get(1.0, "end-1c"), "db"))
    decode_outbox.config(state="disabled")


def switch_to_decode():
    for item_ in encoding_items:
        item_.grid_remove()
    for item_ in decoding_items:
        item_.grid()


def switch_to_encode():
    for item_ in decoding_items:
        item_.grid_remove()
    for item_ in encoding_items:
        item_.grid()


if __name__ == '__main__':
    app = Tk()
    app.title("Encode/Decode")
    app.minsize(1050, 225)
    encodings = ["Normal", "Complex", "Base64"]
    encode_button = Button(master=app, text="Press to encode", command=encode_and_show)
    encode_button.grid(row=2, column=1, ipadx=50)
    decode_button = Button(master=app, text="Press to decode", command=decode_and_show)
    decode_button.grid(row=1, column=1, ipadx=50, pady=15)
    input_box = Text(master=app, height=3, width=50)
    input_box.grid(row=3, column=1)
    normal_label = Label(master=app, text="Normal:  ")
    normal_label.grid(row=2, column=2)
    complex_label = Label(master=app, text="Complex:  ")
    complex_label.grid(row=3, column=2)
    base64_label = Label(master=app, text="Base64:  ")
    base64_label.grid(row=4, column=2)
    outbox = Text(master=app, height=3, width=50, borderwidth=0, state="disabled")
    outbox.grid(row=2, column=3)
    outbox1 = Text(master=app, height=3, width=50, borderwidth=0, state="disabled")
    outbox1.grid(row=3, column=3)
    outbox2 = Text(master=app, height=3, width=50, borderwidth=0, state="disabled")
    outbox2.grid(row=4, column=3)
    complex_encoding_info_label = Label(master=app, text="Info for complex encoding: ")
    complex_encoding_info_label.grid(row=3, column=4)
    normal_encoding_info_label = Label(master=app, text="Info for normal encoding: ")
    normal_encoding_info_label.grid(row=2, column=4)
    normal_key = Text(master=app, height=1, width=2, borderwidth=0, state="disabled")
    normal_key.grid(row=2, column=5)
    complex_key = Text(master=app, height=3, width=1, borderwidth=0, state="disabled")
    complex_key.grid(row=3, column=5)
    current_decode_choice = StringVar(app)
    current_decode_choice.set(encodings[0])
    encoding_option = OptionMenu(app, current_decode_choice, *encodings)
    encoding_option.grid(row=3, column=1)
    input_d_box = Text(master=app, height=3, width=50)
    input_d_box.grid(row=2, column=1)
    decode_outbox = Text(master=app, height=3, width=50, borderwidth=0, state="disabled")
    decode_outbox.grid(row=2, column=3)
    output_label = Label(master=app, text="Output: ")
    output_label.grid(row=2, column=2)
    decode_extra_info = Text(master=app, height=3, width=50)
    decode_extra_info.grid(row=5, column=1)
    decode_extra_info_label = Label(master=app, text="Extra info for the decoding: ")
    decode_extra_info_label.grid(row=4, column=1)
    switch_to_decode_button = Button(master=app, text="Switch to decoding", command=switch_to_decode)
    switch_to_decode_button.grid(row=5, column=4, pady=15)
    switch_to_encode_button = Button(master=app, text="Switch to encoding", command=switch_to_encode)
    switch_to_encode_button.grid(row=5, column=4, pady=15)
    encoding_items = [encode_button, input_box, normal_label, complex_label, base64_label, outbox, outbox1, outbox2,
                      complex_encoding_info_label, complex_key, normal_encoding_info_label, normal_key,
                      switch_to_decode_button]
    decoding_items = [decode_button, input_d_box, encoding_option, decode_outbox, output_label, decode_extra_info,
                      decode_extra_info_label, switch_to_encode_button]
    for item in decoding_items:
        item.grid_remove()
    app.mainloop()
