import tkinter
import random
import math
from gtts import gTTS
from PIL import Image, ImageDraw
from PIL import ImageFont
import random

font = ImageFont.truetype("arial.ttf", 150)

def prime(n):
    lis = []
    for i in range(1, n//2+1):
        if n%i == 0 and i*i <= n+1 and not (i in lis and n//i in lis):
            lis.append(i)
            lis.append(n//i)

    if len(lis) > 2:
        return False
    else:
        return True


def factor(n):
    divs = []
    for i in range(1,n//2+1):
        if n%i == 0 and i*i < n+1:
            divs.append(i)
            divs.append(n//i)
    return sorted(list(set(divs)))


def mult(n):
    divs = []
    for i in range(1, n // 2 + 1):
        if n % i == 0 and i * i < n + 1:
            divs.append([i, n // i])
    return divs


def upsearch(lis, n):
    l, r = 0, len(lis)
    while r - l > 1:
        m = (l + r) // 2
        if lis[m] <= n:
            l = m
        else:
            r = m
    return l


def lowsearch(lis, n):
    l, r = 0, len(lis)
    while l != r:
        m = (l+r)//2
        if lis[m] < n:
            l = m+1
        else:
            r = m
    return l


def speech_it(text):
    tts = gTTS(text=text, lang='ru')
    name = "speeched.mp3"
    tts.save(name)


def graph(lis):
    image = Image.new("RGBA", (920,920),(0,0,0,0))
    canvas = ImageDraw.Draw(image)
    points = []
    rand = [i for i in range(10,910)]

    for i in range(len(lis)):
        g = random.choice(rand)
        s = random.choice(rand)
        points.append((g,s))
        canvas.ellipse(((g)-6,(s)-6, (g)+6, (s)+6), fill="black", outline="black")
        canvas.text((g-4,s-6), text=str(i), fill="white")

    for i in range(len(lis)):
        for j in range(len(lis[i])):
            canvas.line((points[i][0], points[i][1], points[lis[i][j]][0], points[lis[i][j]][1]), fill="black", width=2)
            canvas.text((points[i][0]-4, points[i][1]-6), text=str(i), fill="white")

    for i in range(len(lis)):
        for j in range(len(lis[i])):
            canvas.text((points[i][0]-4, points[i][1]-6), text=str(i), fill="white")

    image.save("drew.png", "PNG")


def draw_inventory(objects):
    image = Image.new("RGBA", (960, 600), (35, 35, 35, 255))
    canvas = ImageDraw.Draw(image)
    k = 120

    for i in range(len(objects)):
        canvas.line((k * i, 0, k * i, 1200), fill='gray', width=2)
        for j in range(len(objects[i])):
            canvas.line((0, k * j, 1920, k * j), fill='gray', width=2)
            if objects[i][j] is not None:
                img = Image.open(objects[i][j])
                img = img.convert("RGBA")
                img = img.resize((96,96), Image.BOX)
                datas = img.getdata()

                newData = []
                for item in datas:
                    if item[3] == 0:
                        newData.append((35, 35, 35, 255))
                    else:
                        newData.append(item)

                img.putdata(newData)
                image.paste(img, (k * i+12, k * j+12, k * i + 108, k * j + 108))
    image.save("inventory.png", "PNG")

def sieve(n):
    tr = [True]*(n+1)
    ret = []
    for i in range(2,n+1):
        if i**2 <= n:
            for j in range(i**2,n+1,i):
                tr[j]=False

    for i in range(n+1):
        if tr[i]:
            ret.append(i)
    return ret


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


def quadro_uravn(a,b,c):
    if b%2 == 0:
        k = b // 2
        disc = k**2 - a* c
        if disc >= 0:
            return (math.sqrt(disc)+k)/a, (math.sqrt(disc)-k)/a
    else:
        disc = b**2 - 4* a* c
        if disc >= 0:
            return (math.sqrt(disc)+b)/a, (math.sqrt(disc)-b)/a


def random_pass(n, len, symbols):
    all_passwords=[]
    def gener_one_pass(len, symbols):
        pas = ''
        for i in range(len):
            pas += random.choice(symbols)
        return pas
    for i in range(n):
        all_passwords.append(gener_one_pass(len,symbols))
    return '\n'.join(all_passwords)


def gcd(a,b):
    if a!=0 and b != 0:
        if a > b:
            return gcd(a%b,b)
        else:
            return gcd(a,b%a)
    else:
        return a+b

def socr_drob(chisl,znamen):
    g = gcd(chisl, znamen)
    return (chisl//g, znamen//g)

def all_combin(lis):
    n = len(lis)
    end = lis[:]
    k = []
    for i in range(len(lis)):
        for j in range(len(lis)):
            end[-i] = lis[j]
            k.append(end[:])
            print(end)
    print(sorted(k))

def num_of_comb(chars,lenght):
    return len(chars)**lenght

def standart_number(x):
    l = str(x).split('.')
    print(l)
    if float(l[0]) > 10:
        y = x / (10 ** len(str(int(l[0]))) / 10)
        syblim = len(str(int(l[0]))) - 1
        print(str(y) + ' * ' + '10^' + str(syblim))
    elif float(l[0]) < -10:
        y = x / (10 ** len(str(int(l[0]))) / 100)
        syblim = len(str(int(l[0]))) - 2
        print(str(y) + ' * ' + '10^' + str(syblim))
    elif x < 1 and x > -1:
        coun = 0
        while x < 1 and x > -1:
            x *= 10
            coun += 1
        print(str(x) + ' * ' + '10^-' + str(coun))
    else:
        print(x)
