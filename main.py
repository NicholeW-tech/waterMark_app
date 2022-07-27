from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import ImageTk, Image, ImageDraw, ImageFont

DARK_BLUE = '#6E85B7'
MED_BLUE = '#B2C8DF'
LT_BLUE = '#C4D7E0'
CREAM = '#F8F9D7'

window = Tk()
window.title('Watermark processor')
window.minsize(width=1000, height=650)
window.config(bg=MED_BLUE)
title_label = Label(text='Watermark Processor')
title_label.config(bg=MED_BLUE, fg=CREAM, font=('Prestige Elite Std', 50))

title_label.grid(column=3, row=0)


class waterMark:
    def __init__(self, window):
        window.columnconfigure(index=3, weight=1)
        window.rowconfigure(index=3, weight=1)
        self.img_choice = Button(window, text='Choose an image',
                                 command=lambda: [self.img_choice.grid_forget(), self.choose_img()])
        self.img_choice.config(bg=DARK_BLUE, fg=CREAM)
        self.img_choice.grid(column=3, row=3)
        self.img_txt = StringVar()
        self.file_name_txt = StringVar()
        self.selected_side = StringVar()
        self.opacity = StringVar()
        self.watermark_placements = {'TOP NW',
                                     'TOP NE',
                                     'BOTTOM NW',
                                     'BOTTOM NE'}
        self.opacity_levels = {
            '50%',
            '75%',
            '95%',
        }

    def show_selected_side(self):
        self.size = self.selected_side.get()

    def show_selected_opacity(self):
        self.opacity_choice = self.opacity.get()

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
        self.img_label.config(bg=MED_BLUE)
        self.img_label.grid(column=3, row=1)
        self.img_name = window.filename
        self.choose_txt_logo = Button(window, text='Create a text logo', command=lambda: [self.choose_txt_logo.
                                      grid_forget(), self.create_txt_logo()])
        self.choose_txt_logo.grid(column=3,row=3)
        self.img_label.image = self.img

    def create_txt_logo(self):
        self.img_label.grid_forget()
        title_label.grid(column=1, row=0)
        self.instruction_label = Label(text='First select options to create your text logo. View your text logo and '
                                            'make sure it\'s accurate. Afterwards exit viewer and click save')
        self.instruction_label.grid(column=1, row=2)
        self.placement_label = Label(text="Choose your watermark placement")
        self.placement_label.grid(column=0, row=1)
        self.placement = OptionMenu(window, self.selected_side, *self.watermark_placements)
        self.placement.grid(column=0, row=2)
        self.submit_placement_btn = Button(window, text="Submit placement", command=self.show_selected_side).grid(column=0, row=3)

        self.color_choice = Button(text='Choose text color', command=self.choose_color)
        self.color_choice.grid(column=1, row=3)

        self.opacity_level_label = Label(text='Choose opacity level')
        self.opacity_level_label.grid(column=1, row=4)
        self.opacity_level = OptionMenu(window, self.opacity, *self.opacity_levels)
        self.opacity_level.grid(column=1, row=5)
        self.submit_opacity_btn = Button(window, text="Submit opacity", command=self.show_selected_opacity).grid(column=1, row=6)

        self.img_txt_label = Label(text='Enter your text').grid(column=2, row=1)
        self.img_txt_entry = Entry(window, textvariable=self.img_txt, font=('calibre', 10, 'normal')).grid(column=2, row=2)
        self.create_txt_btn = Button(text='Create text logo', command=self.write_txt_logo).grid(column=2, row=3)

    def choose_color(self):
        self.color_code = colorchooser.askcolor(title="Choose color")
        self.color_code = list(self.color_code[0])

    def write_txt_logo(self):
        self.txt = self.img_txt.get()
        self.img_txt.set('')
        self.opacity_choice = self.opacity.get()
        self.opacity.set('')
        self.side = self.selected_side.get()
        self.selected_side.set('')
        img = Image.open(self.img_name).convert("RGBA")
        txt_base = Image.new("RGBA", img.size, (255, 255, 255, 0))
        I1 = ImageDraw.Draw(txt_base)
        if self.side == 'TOP NW':
            x = 28
            y = 36
        elif self.side == 'TOP NE':
            x = int(img.width - (img.width / 2.75))
            y = 36
            print(x)
        elif self.side == 'BOTTOM NW':
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
        self.watermarked = Image.alpha_composite(img, txt_base)
        self.watermarked.show()
        self.file_name_label = Label(text='Name your image file').grid(column=2, row=4)
        self.file_name = Entry(window, textvariable=self.file_name_txt, font=('calibre', 10, 'normal')).grid(column=2, row=5)
        self.save_button = Button(window, text="Save Image", command=self.save_image).grid(column=2, row=6)

    def save_image(self):
        self.watermarked.save(f'{self.file_name_txt.get()}.png')


    def create_pic_logo(self):
        img1 = Image.open(self.img_name)
        logo = Image.open(r"C:\Users\nicho\Downloads\bird_clipart.jpg")
        logo = logo.convert('RGBA')

        data = logo.getdata()
        new_data = []
        for item in data:
            if item[:3] == 255:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        logo.putdata(new_data)

        bg_img = img1.copy()
        bg_img.paste(logo, (0, 0), logo)
        bg_img.show()


create = waterMark(window)

window.mainloop()
