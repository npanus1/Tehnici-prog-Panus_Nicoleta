def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

if __name__ == "__main__":
    print("Tip real probe/foto.jpg:", tip_real("probe/foto.jpg"))

   
import re

date_ascunse = open("probe/ascuns.png", "rb").read()
print("--- Strings din probe/ascuns.png ---")
for m in re.findall(rb"[ -~]{4,}", date_ascunse):
    print(m.decode())

   
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

img_exif = Image.open("probe/foto.jpg")
exif_data = img_exif._getexif()

if exif_data:
    print("--- Metadate EXIF ---")
    for tag_id, val in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        if tag_name == "GPSInfo":
            print(f"[+] GPSInfo gasit:")
            for gps_tag_id, gps_val in val.items():
                gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                print(f"    {gps_tag_name} = {gps_val}")
        else:
            print(f"{tag_name} = {val}")
else:
    print("[-] Nu s-au gasit metadate EXIF.")

    
date_fisier = open("probe/ascuns.png", "rb").read()
i = date_fisier.find(b"PK\x03\x04")
if i != -1:
    with open("gasit.zip", "wb") as f_out:
        f_out.write(date_fisier[i:])
    print(f"[+] Arhiva extrasa de la octetul {i} in fisierul 'gasit.zip'")
else:
    print("[-] Nu s-a gasit nicio arhiva ZIP in interior.")

    
from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"  
biti = "".join(f"{x:08b}" for x in mesaj)

if len(biti) > len(px) * 3:
    print("[-] Mesajul este prea lung pentru această imagine!")
else:
    px_nou = []
    bit_idx = 0
    for rgb in px:
        r, g, b = rgb
        if bit_idx < len(biti):
            r = (r & ~1) | int(biti[bit_idx]); bit_idx += 1
        if bit_idx < len(biti):
            g = (g & ~1) | int(biti[bit_idx]); bit_idx += 1
        if bit_idx < len(biti):
            b = (b & ~1) | int(biti[bit_idx]); bit_idx += 1
        px_nou.append((r, g, b))
    
    img_stego = Image.new("RGB", img.size)
    img_stego.putdata(px_nou)
    img_stego.save("stego.png")
    print("[+] Mesajul a fost ascuns cu succes în 'stego.png'!")

    
px_stego = list(Image.open("stego.png").convert("RGB").getdata())
biti_extrasi = []

for rgb in px_stego:
    for canal in rgb:
        biti_extrasi.append(str(canal & 1))


octeti = []
for i in range(0, len(biti_extrasi), 8):
    octet_biti = "".join(biti_extrasi[i:i+8])
    if len(octet_biti) < 8:
        break
    caracter = int(octet_biti, 2)
    if caracter == 0:  
        break
    octeti.append(caracter)

mesaj_decriptat = bytes(octeti).decode("utf-8", errors="ignore")
print(f"[+] Mesaj secret dezvăluit: {mesaj_decriptat}")