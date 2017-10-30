from visual.graph import * #importar graficos tambem
import math
#este programa permite exprimir o movimento da Terra dado o seu raio, a sua distancia ao sol, e a as massas dos mesmos. a partir dai e possivel controlar e prever o movimento de qualquer outro corpo com qualquer outra velocidade

#janela
scene.autoscale=0 #tirar o zoom irritante
scene.title='Earth orbit by Newton'
scene.width=1680 #resolucao do meu PC
scene.height=1050
scene.range=(2*10**11,2*10**11,2*10**11)
scene.lights=[] #importante...desligar luzes iniciais
scene.show_rendertime=True #mostrar velocidade dos ciclos (opcional, para controlo)


#corpos
scene.select()
sun=sphere(pos=(0,0,0), radius=6.96*10**8, color=color.yellow, mass=1.9891*10**30, material=materials.emissive)
earth=ellipsoid(pos=(0,0,1.495811552*10**11), size=(2*6378137,2*6356752.3,2*6378137), mass=5.98*10**24, material=materials.earth, make_trail=True, trail_type="points", interval=10000, retain=999999)
moon=ellipsoid(pos=(-6378137*math.sin(math.pi/4),0,152098233000-6378137*math.sin(math.pi/4)), size=(2*1738140,2*1735970,2*1738140), mass=7.3477*10**22, material=materials.silver, make_trail=True, trail_type="points", interval=10000, retain=999999)
lamp=local_light(pos=sun.pos, color=color.white) #luz vinda do sol
earth.trail_object.color=color.blue #deixar rasto da terra azul em vez de branco
#constantes
def distance(a,b):
    return math.sqrt((a.pos.x-b.pos.x)**2 + (a.pos.y-b.pos.y)**2 + (a.pos.z-b.pos.z)**2) #distancia sol-terra
G=6.67*10**(-11)
sun.vel=vector(0,0,0)
sun.speed=0
moon.vel=vector(-29291-11328.75544*math.sin(math.pi/4),0,-11328.75544*math.sin(math.pi/4))
moon.speed=mag(moon.vel)
earth.vel=vector(-math.sqrt((G*earth.mass)/distance(earth,sun)),0,0) # velocidade inicial no afelio
earth.speed=29781.92627
earth.rotate(angle=0.408407045, axis=(0,0,1)) # declinacao da Terra
speed='Earth speed: ' #para mostradores de resultados... soon
result='Distance: '
t=0

#graficos
gd1=gdisplay(title='Distance(t)', xtitle='time(s)', ytitle='distance(m)') # 1a janela de grafico
f1=gcurve(color=color.red, display=gd1.display)
value1=label(display=gd1.display) #mostrador de valor
gd2=gdisplay(title='Speed(t)', xtitle='time(s)', ytitle='speed(m/s)') # 2a janela de grafico
f2=gcurve(color=color.green, display=gd2.display)
value2=label(display=gd2.display) #mostrador de valor

#gravidade

    
def midpoint(a,b):
    return ((a.pos.x+b.pos.x)/2,(a.pos.y+b.pos.y)/2,(a.pos.z+b.pos.z)/2)

def gravidade(a,b):
    F=(G*a.mass*b.mass)/((distance(a,b))**2) #lei da gravitacao universal
    modulo=F/a.mass # 2a lei de newton
    a2=F/sun.mass # para o sol
    accelaration=vector(b.pos.x-a.pos.x,b.pos.y-a.pos.y,b.pos.z-a.pos.z) #vector direcional da normal
    k=modulo/math.sqrt((accelaration.x**2)+(accelaration.y**2)+(accelaration.z**2)) # k que ajusta o modulo da aceleracao
    centripeta=vector(accelaration.x*k,accelaration.y*k,accelaration.z*k) # ajuste do modulo para ter a verdadeira aceleracao centripeta
    a.vel+=centripeta
    a.pos+=a.vel
    accelaration2=vector(a.pos.x-b.pos.x,a.pos.y-b.pos.y,a.pos.z-b.pos.z) # repetir tudo para o sol (nao e desprezavel)
    k2=a2/math.sqrt((accelaration2.x**2)+(accelaration2.y**2)+(accelaration2.z**2)) 
    centripeta2=vector(accelaration2.x*k2,accelaration2.y*k2,accelaration2.z*k2) 
    b.vel+=centripeta2
    b.pos+=b.vel

def info(a,b):
    f1.plot(pos=(t,distance(a,b)-1.495811552*10**11))#grafico distancia-tempo
    value1.text=result+ str(distance(a,b))
    value1.pos=(t,distance(a,b))
    f2.plot(pos=(t,mag(a.vel)-a.speed)) #grafico velocidade-tempo
    value2.text=speed+str(mag(a.vel))
    value2.pos=(t,mag(earth.vel))
    
#motion
while True:
    rate(100)
    scene.center=earth.pos
    earth.rotate(angle=((math.pi*2)/(24*3600)), axis=(0,1,0)) # movimento de rotacao da Terra, so visivel se o rate for aumentado, ou mesmo tirado
    gravidade(moon,earth)
    gravidade(earth,sun)
    gravidade(moon,sun)
    lamp.pos=sun.pos
    info(earth,sun)
    t+=0.01
    


    
    



    
