from PIL import Image, ImageDraw, ImageFont
import random 
import string
import pytesseract
from subprocess import check_output
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
class SimpleCaptchaException(Exception): 
    pass
class SimpleCaptcha(object):
    def __init__(self, length=5, size=(200, 100), fontsize=36, random_text=None, random_bgcolor=None):
        self.size = size 
        self.text = "CAPTCHA"
        self.fontsize = fontsize 
        self.bgcolor = 255 
        self.length = length
        
        self.image = None  # current captcha image
        
        if random_text: 
            self.text = self._random_text()
            
        if not self.text: 
            raise SimpleCaptchaException("Field text must not be empty.")
            
        if not self.size: 
            raise SimpleCaptchaException("Size must not be empty.")
            
        if not self.fontsize: 
            raise SimpleCaptchaException("Font size must be defined.")
            
        if random_bgcolor: 
            self.bgcolor = self._random_color()
    
    def _center_coords(self, draw, font): 
        width, height = draw.textsize(self.text, font) 
        xy = (self.size[0] - width) / 2., (self.size[1] - height) / 2. 
        return xy
    
    def _add_noise_dots(self, draw):
        size = self.image.size
        for _ in range(int(size[0] * size[1] * 0.1)):
            draw.point((random.randint(0, size[0]),
                        random.randint(0, size[1])),
                       fill="white")
        return draw
    
    def _add_noise_lines(self, draw):
        size = self.image.size
        for _ in range(8):
            width = random.randint(1, 2)
            start = (0, random.randint(0, size[1] - 1))
            end = (size[0], random.randint(0,size[1]-1))
            draw.line([start, end], fill="white", width=width)
            
        for _ in range(8):
            start = (-50, -50)
            end = (size[0] + 10, random.randint(0, size[1]+10))
            draw.arc(start + end, 0, 360, fill="white")
        return draw

    def get_captcha(self, size=None, text=None, bgcolor=None):
        if text is not None:
            self.text = text
                     
        if size is not None:
            self.size = size
                     
        if bgcolor is not None:
            self.bgcolor = bgcolor
                     
        self.image = Image.new('RGB', self.size, self.bgcolor)
        font = ImageFont.truetype('fonts/Vera.ttf', self.fontsize) 
        draw = ImageDraw.Draw(self.image)
        xy = self._center_coords(draw, font) 
        draw.text(xy=xy, text=self.text, font=font)
                     
        # Add some dot noise 
        draw = self._add_noise_dots(draw)
                     
        # Add some random lines 
        draw = self._add_noise_lines(draw)
                     
        self.image.save('new_image.gif')
        return self.text
                     
    def _random_text(self):
        letters = string.ascii_lowercase + string.ascii_uppercase
        random_text = ""
        for _ in range(self.length):
            random_text += random.choice(letters)

        return random_text
     
    def _random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)
class decryptCaptcha(object):
    def resolve(self, path):
        print("Resampling the Image")
        check_output(['convert', path, '-resample', '600', path])
        return pytesseract.image_to_string(Image.open(path))

    def decodedText(self):
        path = 'new_image.gif'
        print('Resolving Captcha')
        captcha_text = self.resolve(path)
        if captcha_text:
            return captcha_text
        else:
            return 'Text can not be extracted'
            
originalText = ''

def helloCallBack(): 
    messagebox.showinfo("Hello Python", "Hello World")
    
def generateCaptcha():
    global originalText
    
    sc = SimpleCaptcha(length=7, fontsize=36, random_text=True, random_bgcolor=True)
    originalText = sc.get_captcha()
    updateCaptcha()
    
def updateCaptcha():
    img2 = tk.PhotoImage(file='new_image.gif')
    captcha.configure(image=img2)
    captcha.image = img2
    
def decodeCaptcha():
    obj = decryptCaptcha()
    decode = obj.decodedText()
    messagebox.showinfo("Decoded Captcha", decode)
    
def uploadCaptchaImg():
    filename = filedialog.askopenfilename(filetypes=(("Image Files", "*.gif"),
                                                     ("All files", "*.*") ))
    
    if not filename:
        messagebox.showerror('STATUS' ,'You have not choose any file')
    else:
        imgUpload = Image.open(filename)
        imgUpload.save('new_image.gif')
        updateCaptcha()
        messagebox.showinfo('STATUS', 'Upload Successful')

def verifyCaptcha():
    global originalText
    
    answer = simpledialog.askstring("Input", "Enter captcha text?",
                                    parent=application_window)
    if answer is not None:
        if(originalText == answer):
            messagebox.showinfo('STATUS', 'Verification successful')
        else:
            messagebox.showerror('STATUS', 'Verification un-successful \nPlease try again')
    else:
        messagebox.showwarning('STATUS', 'Please enter CAPTCHA text')
    
application_window = tk.Tk()

leftframe = tk.Frame(application_window, width = 1) 
leftframe.pack(side = tk.LEFT)

rightframe = tk.Frame(application_window, width=400, height=600) 
rightframe.pack(side = tk.RIGHT)

getCaptcha = tk.Button(leftframe, text="Generate Captcha", fg="black", height = 2, width = 17, 
                       command = generateCaptcha)

getCaptcha.grid(row=1, column=0)

uploadCaptcha = tk.Button(leftframe, text="Upload Captcha", fg="black", height = 2, width = 17, 
                         command = uploadCaptchaImg)
uploadCaptcha.grid(row=2, column=0)

decodeCaptcha = tk.Button(leftframe, text="Decode Captcha", fg="black", height = 2, width = 17, 
                         command = decodeCaptcha)
decodeCaptcha.grid(row=3, column=0)

verifyCaptcha = tk.Button(leftframe, text="Verify Captcha", fg="black", height = 2, width = 17, 
                         command = verifyCaptcha)
verifyCaptcha.grid(row=4, column=0)

img = tk.PhotoImage(file='new_image.gif')
captcha = tk.Label(rightframe, image=img, width = 250, height = 150)
captcha.grid(row=1, column=1)

application_window.mainloop()               