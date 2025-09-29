from PIL import Image


lemur = Image.open("lemur.png")
flag = Image.open("flag.png")

width_flag, height_flag = flag.size
width_lemur, height_lemur = lemur.size



assert(width_flag==width_lemur)
assert(height_flag==height_lemur)
width = width_flag
height = height_flag
flag_pixels = flag.load()
lemur_pixels = lemur.load()

for w in range(width):
  for h in range(height):
    r_flag,g_flag,b_flag = flag_pixels[w,h]
    r_lemur,g_lemur,b_lemur = lemur_pixels[w,h]
    r = r_flag ^ r_lemur
    g = g_flag ^ g_lemur
    b = b_flag ^ b_lemur
    flag_pixels[w,h] = (r,g,b)

flag.save("result.png", format="png")
    
    
    
    