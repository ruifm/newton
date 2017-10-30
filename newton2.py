from visual.graph import * #importar graficos tambem
import math
#janela
scene.autoscale=0 #retirar o zoom irritante
scene.title='Earth orbit by Newton'
scene.width=640 #resolucao do meu PC
scene.height=480
#importante...desligar luzes iniciais
scene.show_rendertime=True #mostrar velocidade dos ciclos (opcional, para controlo)
#constantes
t=0
G=1
#funcoes importantes
def distance(a,b):
    return float(math.sqrt((a.pos.x-b.pos.x)**2 + (a.pos.y-b.pos.y)**2 + (a.pos.z-b.pos.z)**2)) #distancia entre 2 corpos
def orbital(a,b):
    a.speed=float(math.sqrt((G*b.mass)/distance(a,b)))
    a.perpendicular=vector(a.pos.x-b.pos.x,0,a.pos.z-b.pos.z)
    a.correcto=vector(1,0,(-a.perpendicular.x)/a.perpendicular.z)
    a.factor=a.speed/mag(a.certo)
    return vector(a.correcto.x*a.factor,0,a.correcto.z*a.factor)

#corpos
earth=sphere(pos=(0,0,39000.), radius=5, color=color.blue, mass=1., make_trail=True, retain=100)
sun=sphere(pos=(0,0,0), radius=200, opacity=0.5, color=color.yellow, mass=100000000, material=materials.emissive, make_trail=True, trail_type="points", interval=5, reatain=999)
lamp=local_light(pos=sun.pos, color=color.white) #luz vinda do sol
alpha=math.acos(1-((100**2)/(2*earth.pos.z**2)))
moon=sphere(pos=(-earth.pos.z*math.sin(alpha),0,earth.pos.z*math.cos(alpha)), radius=1, mass=0.1, make_trail=True)

#graficos
gd1=gdisplay(title='Distance(t)', xtitle='time(s)', ytitle='distance(m)') # 1a janela de grafico
f1=gcurve(color=color.red, display=gd1.display)
value1=label(display=gd1.display) #mostrador de valor
result='Distance: '
#condicoes iniciais:
sun.vel=vector(0,0,0)
earth.vel=orbital(earth,sun) # velocidade inicial no afelio
moon.vel=orbital(moon,sun)


#gravidade
def gravidade(a,b):
    F=(G*a.mass*b.mass)/((distance(a,b))**2) #lei da gravitacao universal
    a.modulo=(F/a.mass) # 2a lei de newton
    b.modulo=(F/b.mass) # para o sol
    a.accelaration=vector(b.pos.x-a.pos.x,b.pos.y-a.pos.y,b.pos.z-a.pos.z) #vector direcional da normal
    a.k=a.modulo/math.sqrt((a.accelaration.x**2)+(a.accelaration.y**2)+(a.accelaration.z**2)) # k que ajusta o modulo da aceleracao
    a.centripeta=vector(a.accelaration.x*a.k,a.accelaration.y*a.k,a.accelaration.z*a.k) # ajuste do modulo para ter a verdadeira aceleracao centripeta
    a.vel+=a.centripeta
    a.pos+=a.vel
    b.accelaration=vector(a.pos.x-b.pos.x,a.pos.y-b.pos.y,a.pos.z-b.pos.z) # repetir tudo para o 2o corpo
    b.k=b.modulo/math.sqrt((b.accelaration.x**2)+(b.accelaration.y**2)+(b.accelaration.z**2)) 
    b.centripeta=vector(b.accelaration.x*b.k,b.accelaration.y*b.k,b.accelaration.z*b.k) 
    b.vel+=b.centripeta
    b.pos+=b.vel

def info(a,b):
    f1.plot(pos=(t,distance(a,b)-100))#grafico distancia-tempo
    value1.text=result+ str(distance(a,b))
    value1.pos=(t,distance(a,b))
scene.range=(distance(earth,sun),distance(earth,sun),distance(earth,sun))

def force():
    objectos=[]
    for corpo in scene.objects:
        if corpo.__class__ == sphere:
            objectos.append(corpo)
    for obj in objectos[:-1]:
        for i in range(objectos.index(obj)+1,len(objectos)):
            gravidade(obj,objectos[i])
    
#motion
while True:
    rate(5)
    scene.center=earth.pos
    gravidade(earth,sun)
    gravidade(moon,sun)
    info(moon,earth)
    t+=0.01
    
    



    
