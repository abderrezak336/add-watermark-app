# import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from add_watermark import AddWatermark
from tkinter import ttk
from color import colors_rgb, colors_tuple
from PIL import Image


win = Tk()
win.config(width=1500, height=780)
win.iconbitmap("app_logo.ico")
win.title("Add Watermark App")

def cond_dec(function):
    def wrapper(self, path):
        if path != "":
            function(self, path)
        else:
            messagebox.showinfo(title="Empty photo", message="Open your photo to add a watermark")
    return wrapper






class App:
    def __init__(self, master):
        self.win = master
        self.background = PhotoImage(file="images/gradient_background.png")
        self.none_image = PhotoImage(file="images/none_image.png")
        self.widget_image = PhotoImage(file="images/grey_widjet.png")
        self.open_image = PhotoImage(file="images/open.png")
        self.save_image = PhotoImage(file="images/save.png")
        self.remove_image = PhotoImage(file="images/remove.png")
        self.addl_image = PhotoImage(file="images/addlogo.png")
        self.addt_image = PhotoImage(file="images/addtext.png")
        self.many_image = PhotoImage(file="images/many.png")
        self.buttom = PhotoImage(file="images/bottom.png")
        self.above = PhotoImage(file="images/above.png")
        self.save_bg = PhotoImage(file="images/save_bg.png")
        self.save_loc = PhotoImage(file="images/save_loc.png")
        self.converted_image = None
        self.canvas = Canvas(width=1500, height=780)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(750, 390, image=self.background)
        self.none_img_bg = self.canvas.create_image(1130, 405, image=self.none_image)
        self.canvas.create_image(485, 442, image=self.widget_image)
        self.open_btn = Button(image=self.open_image, borderwidth=0, highlightthickness=0, command=self.open_photo)
        self.save_btn = Button(image=self.save_image, borderwidth=0, highlightthickness=0, command=lambda :self.save_photo(self.photo_path))
        self.remove_btn = Button(image=self.remove_image, borderwidth=0, highlightthickness=0, command=lambda :self.reset_photo(self.photo_path))
        self.addt_btn = Button(image=self.addt_image, borderwidth=0, highlightthickness=0, command=lambda :self.show_text_properties(self.photo_path))
        self.addl_btn = Button(image=self.addl_image, borderwidth=0, highlightthickness=0, command=lambda :self.open_logo(self.photo_path))
        self.open_btn.place(x=38, y=161)
        self.save_btn.place(x=38, y=256)
        self.remove_btn.place(x=38, y=352)
        self.addl_btn.place(x=231, y=46)
        self.addt_btn.place(x=584, y=46)

        self.photo_path = ""
        self.logo_path = ""
        self.original_size = ()
        self.add_wmark = None
        self.text_entry = None
        self.selected_font = ""
        self.selected_color = ""
        self.slider_value = ""
        self.opacity_value = ""
        self.angle_value = ""
        self.selected_box = ""
        self.watermark_text = ""
        self.format = ""

    def open_photo(self):
        self.photo_path = filedialog.askopenfilename()
        if self.photo_path != "":
            self.add_wmark = AddWatermark(self.photo_path)
            self.original_size = self.add_wmark.get_size()
            self.add_wmark.resize_image(706, 714)
            self.config_image()
        else:
            pass

    @cond_dec
    def reset_photo(self, path):
        self.add_wmark.resize_image(706, 714)
        self.config_image()

    @cond_dec
    def open_logo(self, path):
        self.logo_path = filedialog.askopenfilename()
        if self.logo_path != "":
            self.add_wmark.add_logo(self.logo_path)
            self.show_logo_properties()
            self.config_image()
        else:
            pass

    def config_image(self):
        self.converted_image = PhotoImage(file="converted_image.png")
        self.canvas.itemconfig(self.none_img_bg, image=self.converted_image)

    def show_logo_properties(self):
        def get_slider_value(value):
            self.slider_value = int(value)
            self.add_wmark.size = self.slider_value
            self.add_wmark.watermarked_image = self.add_wmark.img
            self.add_wmark.add_logo(self.logo_path)
            self.config_image()

        def get_opacity_value(value):
            self.opacity_value = int(value)
            self.add_wmark.opacity = self.opacity_value
            self.add_wmark.watermarked_image = self.add_wmark.img
            self.add_wmark.add_logo(self.logo_path)
            self.config_image()

        def get_angle_value(value):
            self.angle_value = int(value)
            self.add_wmark.angle = self.angle_value
            self.add_wmark.watermarked_image = self.add_wmark.img
            self.add_wmark.add_logo(self.logo_path)
            self.config_image()

        def selected_position(event):
            self.selected_pos = position_box.get()
            self.add_wmark.position = self.selected_pos
            self.add_wmark.watermarked_image = self.add_wmark.img
            self.add_wmark.add_logo(self.logo_path)
            self.config_image()

        # labels
        self.canvas.create_text(262, 385, text="Size", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 485, text="Tile", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 569, text="Opacity", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 675, text="Rotation", fill="white", font=("Arial", 20, "normal"), anchor="nw")


        # scale slider
        size = Scale(from_=10, to=100, resolution=1, orient='horizontal',
                     highlightthickness=0, borderwidth=0, length=400,
                     background="#545454", font=("Arial", 10, "normal"), foreground="white", command=get_slider_value)
        size.set(60)  # Default value
        size.place(x=262, y=430)

        opacity = Scale(from_=0, to=255, resolution=1, orient='horizontal',
                        highlightthickness=0, borderwidth=0, length=400,
                        background="#545454", font=("Arial", 10, "normal"), foreground="white",
                        command=get_opacity_value)
        opacity.set(128)  # Default value
        opacity.place(x=262, y=614)

        rotation = Scale(from_=0, to=360, resolution=1, orient='horizontal',
                         highlightthickness=0, borderwidth=0, length=400,
                         background="#545454", font=("Arial", 10, "normal"), foreground="white",
                         command=get_angle_value)
        rotation.set(0)  # Default value
        rotation.place(x=262, y=710)

        # comobox
        position_var = StringVar()
        position_box = ttk.Combobox(textvariable=position_var, width=14, font=("Arial", 15, "normal"))
        position_box["values"] = ("top_right", "top_left", "bottom_left", "bottom_right", "center", "many")

        position_box.bind('<<ComboboxSelected>>', selected_position)
        position_box.place(x=350, y=480)

    @cond_dec
    def show_text_properties(self, path):
        def selected_font(event):
            self.selected_font = font_box.get()
            self.add_wmark.font = self.selected_font
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()
        def selected_color(event):
            self.selected_color = list(colors_rgb[color_box.get()])
            self.add_wmark.color = self.selected_color
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()
        def get_slider_value(value):
            self.slider_value = int(value)
            self.add_wmark.size = self.slider_value
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()
        def get_opacity_value(value):
            self.opacity_value = int(value)
            self.add_wmark.opacity = self.opacity_value
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()
        def get_angle_value(value):
            self.angle_value = int(value)
            self.add_wmark.angle = self.angle_value
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()
        def get_watermark_text(event):
            self.watermark_text = self.text_entry.get()
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()
        def selected_position(event):
            self.selected_pos = position_box.get()
            self.add_wmark.position = self.selected_pos
            self.add_wmark.add_text(self.watermark_text)
            self.config_image()


        #labels
        self.canvas.create_text(262, 144, text="Text", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 251, text="Font", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 309, text="Color", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 385, text="Size", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 485, text="Tile", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 569, text="Opacity", fill="white", font=("Arial", 20, "normal"), anchor="nw")
        self.canvas.create_text(262, 675, text="Rotation", fill="white", font=("Arial", 20, "normal"), anchor="nw")


        #entries
        self.text_entry = Entry(width=20, font=("Arial", 30, "normal"), highlightthickness=0, borderwidth=0)
        self.text_entry.place(x=262, y=185)
        self.text_entry.bind("<Return>", get_watermark_text)

        #scale slider
        size = Scale(from_=10, to=100, resolution=1, orient='horizontal',
                     highlightthickness=0, borderwidth=0, length=400,
                     background="#545454", font=("Arial", 10, "normal"), foreground="white", command=get_slider_value)
        size.set(40)  # Default value
        size.place(x=262, y=430)

        opacity = Scale(from_=0, to=255, resolution=1, orient='horizontal',
                     highlightthickness=0, borderwidth=0, length=400,
                     background="#545454", font=("Arial", 10, "normal"), foreground="white", command=get_opacity_value)
        opacity.set(128)  # Default value
        opacity.place(x=262, y=614)

        rotation = Scale(from_=0, to=360, resolution=1, orient='horizontal',
                     highlightthickness=0, borderwidth=0, length=400,
                     background="#545454", font=("Arial", 10, "normal"), foreground="white", command=get_angle_value)
        rotation.set(0)  # Default value
        rotation.place(x=262, y=710)

        #comobox
        font_var = StringVar()
        font_box = ttk.Combobox(textvariable=font_var, width=14,
                                    font=("Arial", 15, "normal"))
        font_box["values"] = tuple(self.add_wmark.fonts)

        font_box.bind('<<ComboboxSelected>>', selected_font)
        font_box.place(x=350, y=255)

        color_var = StringVar()
        color_box = ttk.Combobox(textvariable=color_var, width=14,
                                    font=("Arial", 15, "normal"))
        color_box["values"] = colors_tuple

        color_box.bind('<<ComboboxSelected>>', selected_color)
        color_box.place(x=350, y=312)

        position_var = StringVar()
        position_box = ttk.Combobox(textvariable=position_var, width=14, font=("Arial", 15, "normal"))
        position_box["values"] = ("top_right", "top_left", "bottom_left", "bottom_right", "center", "many")

        position_box.bind('<<ComboboxSelected>>', selected_position)
        position_box.place(x=350, y=480)

    @cond_dec
    def save_photo(self, path):
        def selected_format(event):
            self.format = format_box.get()

        def get_location():
            loc = filedialog.askdirectory()
            new_width = int(width.get())
            new_height = int(height.get())
            saved_photo = Image.open("converted_image.png")
            saved_photo.resize((new_width, new_height)).save(f"{loc}/watermarked_photo.{self.format.lower()}", format=self.format)



        save_win = Toplevel(self.win)
        save_win.config(width=300, height=350)
        save_win.iconbitmap("app_logo.ico")
        canv = Canvas(save_win, width=300, height=350)
        canv.place(x=0, y=0)
        canv.create_image(150, 175, image=self.save_bg)

        #comobox
        format_var = StringVar()
        format_box = ttk.Combobox(save_win, textvariable=format_var, width=14,
                                    font=("Arial", 15, "normal"))
        format_box["values"] = ("JPEG", "PNG", "BMP", "GIF", "TIFF", "PPM", "ICO", "WEBP")


        format_box.bind('<<ComboboxSelected>>', selected_format)
        format_box.place(x=30, y=68)

        #entry
        width = Entry(save_win, width=10, font=("Arial", 20, "normal"), highlightthickness=0, borderwidth=0)
        width.insert(0, str(self.original_size[0]))
        width.place(x=98, y=154)

        height = Entry(save_win, width=10, font=("Arial", 20, "normal"), highlightthickness=0, borderwidth=0)
        height.insert(0, str(self.original_size[1]))
        height.place(x=98, y=198)

        save_loc = Button(save_win, image=self.save_loc, highlightthickness=0, borderwidth=0, command=get_location)
        save_loc.place(x=33, y=293)


app = App(win)
win.mainloop()



# def update_spacing(val):
#     spacing_label.config(text=f"{float(val):.2f}x")
#
# def get_slider_value():
#     # Retrieve the current value of the slider
#     value = spacing_slider.get()
#     print(f"Current Spacing Value: {value}")
#     value_label.config(text=f"Value: {value:.2f}x")
#
# root = tk.Tk()
# root.title("Spacing Adjustment")
#
# # Label for the slider
# spacing_text = tk.Label(root, text="Spacing")
# spacing_text.pack()
#
# # Scale (Slider) widget
# spacing_slider = tk.Scale(root, from_=1.0, to=2.0, resolution=0.01, orient='horizontal', command=update_spacing)
# spacing_slider.set(1.52)  # Default value
# spacing_slider.pack()
#
# # Label to display the spacing value
# spacing_label = tk.Label(root, text="1.52x")
# spacing_label.pack()
#
# # Button to get and display the current value of the slider
# get_value_button = tk.Button(root, text="Get Spacing Value", command=get_slider_value)
# get_value_button.pack()
#
# # Label to show the current value when the button is clicked
# value_label = tk.Label(root, text="Value: 1.52x")
# value_label.pack()
#
# root.mainloop()
