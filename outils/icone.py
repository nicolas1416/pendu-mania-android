from PIL import Image, ImageDraw, ImageFilter
S=1024
def degrade(w,h,c1,c2):
    im=Image.new("RGB",(w,h)); d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/(h-1); d.line([(0,y),(w,y)],fill=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3)))
    return im
def bloc(d,x,y,w,h,face,cote,dessus,ep=26):
    # pavé pseudo-3D : face avant, côté droit, dessus
    d.polygon([(x+w,y),(x+w+ep,y-ep),(x+w+ep,y+h-ep),(x+w,y+h)],fill=cote)
    d.polygon([(x,y),(x+ep,y-ep),(x+w+ep,y-ep),(x+w,y)],fill=dessus)
    d.rectangle([x,y,x+w,y+h],fill=face)
def dessiner(d,k=1.0,ox=0,oy=0):
    B=((184,138,92),(138,100,64),(214,176,130))
    f=lambda v:int(v*k)
    bloc(d,ox+f(170),oy+f(800),f(640),f(70),*B,ep=f(30))          # socle
    bloc(d,ox+f(250),oy+f(150),f(70),f(650),*B,ep=f(30))          # poteau
    bloc(d,ox+f(250),oy+f(150),f(420),f(62),*B,ep=f(30))          # poutre
    d.polygon([(ox+f(320),oy+f(330)),(ox+f(470),oy+f(212)),(ox+f(500),oy+f(212)),(ox+f(320),oy+f(370))],fill=B[1])
    cx=ox+f(600)
    d.rectangle([cx-f(6),oy+f(212),cx+f(6),oy+f(330)],fill=(227,207,160))  # corde
    # personnage
    peau=(241,194,150); teal=(46,125,116); tealf=(31,89,82)
    bloc(d,cx-f(70),oy+f(330),f(140),f(130),peau,(212,165,120),(250,215,180),ep=f(22))   # tête
    bloc(d,cx-f(78),oy+f(470),f(156),f(170),teal,tealf,(70,150,140),ep=f(22))             # corps
    for s in(-1,1):  # bras levés
        x0=cx+s*f(78); 
        d.polygon([(x0,oy+f(490)),(x0+s*f(40),oy+f(490)),(x0+s*f(95),oy+f(380)),(x0+s*f(60),oy+f(365))],fill=teal)
        d.rectangle([min(x0+s*f(55),x0+s*f(100)),oy+f(340),max(x0+s*f(55),x0+s*f(100)),oy+f(380)],fill=peau)
    for s in(-1,1):  # jambes
        d.rectangle([cx+s*f(40)-f(30),oy+f(640),cx+s*f(40)+f(30),oy+f(770)],fill=(58,63,74))
        d.rectangle([cx+s*f(40)-f(34),oy+f(765),cx+s*f(40)+f(38),oy+f(800)],fill=(58,43,34))
    # visage
    e=(43,33,26)
    for s in(-1,1):
        d.ellipse([cx+s*f(34)-f(14),oy+f(370),cx+s*f(34)+f(14),oy+f(398)],fill=e)
    d.chord([cx-f(32),oy+f(395),cx+f(32),oy+f(445)],0,180,fill=e)
    # chapeau de cowboy
    br=(138,90,59)
    d.ellipse([cx-f(120),oy+f(318),cx+f(130),oy+f(352)],fill=br)
    d.rounded_rectangle([cx-f(58),oy+f(248),cx+f(64),oy+f(338)],f(18),fill=br)
    d.rectangle([cx-f(58),oy+f(310),cx+f(64),oy+f(328)],fill=(229,88,63))
# icône classique (carré arrondi)
fond=degrade(S,S,(59,47,37),(140,118,100)).convert("RGBA")
dessiner(ImageDraw.Draw(fond))
masque=Image.new("L",(S,S),0); ImageDraw.Draw(masque).rounded_rectangle([0,0,S-1,S-1],220,fill=255)
fond.putalpha(masque); fond.save("icone.png")
# premier plan pour icône adaptative : dessin réduit dans la zone sûre (66 %)
pp=Image.new("RGBA",(S,S),(0,0,0,0)); dd=ImageDraw.Draw(pp)
k=0.6; dessiner(dd,k,int(S*(1-k)/2)-10,int(S*(1-k)/2)-10)
pp.save("icone_premier_plan.png")
