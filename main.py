from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import ImageTk, Image, ImageDraw, ImageFont

window = Tk()
window.title('Watermark processor')
window.minsize(width=1000, height=650)
title = Label(text='Watermark Processor')
title.pack()


class waterMark:
    def __init__(self, window):
        self.img_choice = Button(window, text='Choose an image',
                                 command=lambda: [self.img_choice.pack_forget(), self.choose_img()])
        self.img_choice.pack()
        self.img_txt = StringVar()
        self.selected_size = StringVar()
        self.opacity = StringVar()
        self.watermark_placements = (('Top Left', 'TOP NW'),
                                     ('Top Right', 'TOP NE'),
                                     ('Bottom Left', 'BOTTOM NW'),
                                     ('Bottom Right', 'BOTTOM NE'))
        self.opacity_levels = {
            '50%',
            '75%',
            '95%',
        }

    def show_selected_size(self):
        self.size = self.selected_size.get()

    def show_selected_opacity(self):
        self.opacity_choice = self.opacity.get()
        print(self.opacity_choice)

    def choose_img(self):
        window.filename = filedialog.askopenfilename(initialdir='C', title="Select your image",
                                                     filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        self.img = Image.open(window.filename)

        while self.img.width > 1000:
            width = int(self.img.width / 2)
            height = int(self.img.height / 2)
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
        while self.img.height > 600:
            width = int(self.img.width / 2)
            height = int(self.img.height / 2)
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.img_label = Label(window, image=self.img)
        self.img_label.pack(expand=True, fill=BOTH)
        self.img_name = window.filename
        self.choose_txt_logo = Button(window, text='Create a text logo', command=lambda: [self.choose_txt_logo.
                                      pack_forget(), self.choose_pic_logo.pack_forget(), self.create_txt_logo()])
        self.choose_txt_logo.pack(side=RIGHT)
        self.choose_pic_logo = Button(window, text='Create a picture', command=lambda: [self.choose_txt_logo.
                                      pack_forget(), self.choose_pic_logo.pack_forget(), self.create_txt_logo()])
        self.choose_pic_logo.pack(side=LEFT)
        self.img_label.image = self.img

    def create_txt_logo(self):
        self.img_label.pack_forget()

        # label
        self.submit_label = Label(text="Submit placement")
        self.submit_label.pack(padx=5, pady=5)

        # radio buttons
        for size in self.watermark_placements:
            r = Radiobutton(
                window,
                text=size[0],
                value=size[1],
                variable=self.selected_size
            )
            r.pack(fill='x', padx=5, pady=5)
        self.placement_button = Button(
            window,
            text="Submit your placement",
            command=self.show_selected_size)

        self.placement_button.pack(padx=5, pady=5)
        self.color_choice = Button(text='Choose text color', command=self.choose_color)
        self.color_choice.pack()
        self.opacity_level_label = Label(text='Choose opacity level')
        self.opacity_level_label.pack()
        self.opacity_level = OptionMenu(window, self.opacity, *self.opacity_levels)
        self.opacity_level.pack()
        self.submit_opacity_btn = Button(window, text="Submit opacity", command=self.show_selected_opacity).pack()
        self.opacity.set('')
        self.img_txt_label = Label(text='Enter your text').pack()
        self.img_txt_entry = Entry(window, textvariable=self.img_txt, font=('calibre', 10, 'normal')).pack()
        self.create_txt_btn = Button(text='Create text logo', command=self.write_txt_logo).pack()
        self.create_logo_btn = Button(text='Choose a logo instead').pack()

    def choose_color(self):
        self.color_code = colorchooser.askcolor(title="Choose color")
        self.color_code = list(self.color_code[0])

    def write_txt_logo(self):
        self.txt = self.img_txt.get()
        self.img_txt.set("")
        img = Image.open(self.img_name).convert("RGBA")
        txt_base = Image.new("RGBA", img.size, (255, 255, 255, 0))
        I1 = ImageDraw.Draw(txt_base)
        if self.size == 'TOP NW':
            x = 28
            y = 36
        elif self.size == 'TOP NE':
            x = int(img.width - (img.width / 2.75))
            y = 36
            print(x)
        elif self.size == 'BOTTOM NW':
            x = 28
            y = img.height - (img.height / 8)
        else:
            x = int(img.width - (img.width / 2.75))
            y = img.height - (img.height / 8)
        if self.opacity_choice == '95%':
            opacity = 15
        elif self.opacity_choice == '75%':
            opacity = 50
        elif self.opacity_choice == '50%':
            opacity = 125

        font_size = int(img.width / 15)
        img_font = ImageFont.truetype("arial.ttf", font_size)
        I1.text((x, y), f"{self.txt}", fill=(self.color_code[0], self.color_code[1], self.color_code[2],
                                             opacity), font=img_font)
        watermarked = Image.alpha_composite(img, txt_base)
        watermarked.show()

    def choose_logo(self):
        pass


create = waterMark(window)

window.mainloop()
