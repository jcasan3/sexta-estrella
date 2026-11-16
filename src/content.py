# -*- coding: utf-8 -*-
"""Guiones de los 10 Shorts. Cada 'beat' = una frase de voz + un gráfico.
say  : frase hablada (también se usa para los subtítulos)
kind : tipo de gráfico; el resto de campos depende del tipo.
En los titulares, *asteriscos* = palabra resaltada.
"""
CHANNEL = "SEXTA ESTRELLA"
HANDLE = "@SextaEstrella"

CTA = dict(say="Síguenos: el jueves subimos todo lo del lanzamiento.", kind="cta")
CTA2 = dict(say="Síguenos: cada día, un dato nuevo de GTA 6.", kind="cta")

VIDEOS = [
 dict(
  id="01_hora", pal=0,
  title="¿A qué hora sale GTA 6 en tu país? (hora exacta) #Shorts",
  desc="GTA 6 se desbloquea el jueves 19 de noviembre de 2026 a la medianoche, hora local, en PS5 y Xbox Series X|S. Te explicamos qué significa eso en México, Colombia, Perú, Argentina y Chile, y por qué algunos países juegan antes.",
  tags="gta 6, gta vi, a qué hora sale gta 6, hora lanzamiento gta 6, gta 6 méxico, gta 6 colombia, gta 6 argentina, gta 6 fecha",
  beats=[
   dict(say="¿A qué hora sale GTA 6 en tu país?", kind="hook", kicker="LANZAMIENTO", head="¿A qué *hora* sale GTA 6?", icon="clock"),
   dict(say="Sale el jueves 19 de noviembre de 2026.", kind="big", label="FECHA OFICIAL", value="19 NOV", sub="jueves · 2026"),
   dict(say="Y Rockstar ya lo aclaró: se desbloquea a la medianoche, hora local, en todas las regiones.", kind="big", label="SE DESBLOQUEA", value="00:00", sub="hora local · todas las regiones"),
   dict(say="O sea, a las doce en punto de tu país: México, Colombia, Perú, Argentina, Chile. Cada uno a su medianoche.", kind="list", title="Jueves 19, a tu medianoche",
        items=[("ok","México","00:00 centro"),("ok","Colombia","00:00"),("ok","Perú","00:00"),("ok","Argentina","00:00"),("ok","Chile","00:00")]),
   dict(say="Por eso Nueva Zelanda juega primero, y América, varias horas después.", kind="text", head="Primero: *Nueva Zelanda*", sub="América entra horas después", icon="globe"),
   dict(say="Ojo: si tu país tiene varios husos horarios, las tiendas usan la hora de la capital. Revisa la ficha de tu tienda.", kind="text", head="¿Varios husos? Manda la *capital*", sub="Confirma en la ficha de tu tienda"),
   dict(say="Y vale igual para PS5 y para Xbox Series.", kind="list", title="Misma hora en",
        items=[("ok","PS5",""),("ok","Xbox Series X|S","")]),
   CTA,
  ]),
 dict(
  id="02_pc", pal=1,
  title="¿GTA 6 sale en PC? Lo que sí se sabe #Shorts",
  desc="GTA 6 llega el 19 de noviembre de 2026 solo a PS5 y Xbox Series X|S. Rockstar no ha anunciado versión de PC. Repasamos el reporte que apunta a inicios de 2027 y lo que pasó con GTA 5.",
  tags="gta 6 pc, gta 6 pc fecha, gta vi pc, cuándo sale gta 6 en pc, gta 6 requisitos, gta 6 steam",
  beats=[
   dict(say="¿GTA 6 sale en PC? Respuesta corta: el jueves, no.", kind="stamp", q="¿GTA 6 sale en PC el jueves?", stamp="NO", icon="monitor"),
   dict(say="El lanzamiento del 19 de noviembre es solo para PS5 y Xbox Series.", kind="list", title="19 de noviembre",
        items=[("ok","PS5",""),("ok","Xbox Series X|S",""),("no","PC","")]),
   dict(say="Rockstar no ha anunciado versión de PC: ni fecha, ni requisitos.", kind="list", title="PC: lo oficial",
        items=[("q","Versión","sin anunciar"),("q","Fecha","sin anunciar"),("q","Requisitos","sin anunciar")]),
   dict(say="Lo que sí hay es un reporte de GamesBeat que la ubica entre enero y marzo de 2027.", kind="big", label="REPORTE DE GAMESBEAT", value="ENE–MAR", sub="2027 · no es oficial"),
   dict(say="Es un reporte, no un anuncio.", kind="text", head="Reporte *≠* anuncio", sub="Rockstar no lo ha confirmado"),
   dict(say="Y hay antecedente: GTA 5 salió en consolas en septiembre de 2013, y llegó a PC en abril de 2015.", kind="timeline", title="Lo que pasó con GTA 5",
        points=[("SEP 2013","Consolas"),("ABR 2015","PC")]),
   dict(say="Así que si solo tienes PC, toca esperar, y esquivar spoilers.", kind="text", head="Solo PC: toca *esperar*", sub="y esquivar spoilers"),
   CTA,
  ]),
 dict(
  id="03_ediciones", pal=2,
  title="GTA 6: ¿Estándar o Ultimate? Precio y diferencias #Shorts",
  desc="GTA 6 cuesta 79.99 USD en edición Estándar y 99.99 USD en Ultimate. Qué cambia entre una y otra, el pack Vintage Vice City y cuánto ronda en México.",
  tags="gta 6 precio, gta 6 ediciones, gta 6 ultimate edition, gta 6 estándar, cuánto cuesta gta 6, gta 6 precio méxico, vintage vice city pack",
  beats=[
   dict(say="¿Estándar o Ultimate? Qué edición de GTA 6 te conviene.", kind="hook", kicker="PRECIO Y EDICIONES", head="¿Estándar o *Ultimate*?"),
   dict(say="La Estándar cuesta 79 dólares con 99. La Ultimate, 99 con 99.", kind="vs",
        a=("ESTÁNDAR","$79.99","USD"), b=("ULTIMATE","$99.99","USD")),
   dict(say="Son veinte dólares de diferencia.", kind="big", label="DIFERENCIA", value="+$20", sub="dólares"),
   dict(say="¿Qué suma la Ultimate? Extras digitales dentro del juego, como vehículos, armas y ropa.", kind="list", title="La Ultimate suma",
        items=[("ok","Vehículos",""),("ok","Armas",""),("ok","Ropa","")]),
   dict(say="La historia es la misma en las dos.", kind="text", head="La historia es *la misma*", sub="en las dos ediciones"),
   dict(say="Si compras en digital antes del 20 de noviembre, cualquier edición incluye el pack Vintage Vice City.", kind="big", label="COMPRANDO ANTES DEL 20 NOV", value="PACK", sub="Vintage Vice City · en cualquier edición"),
   dict(say="En México, la Estándar ronda entre 1300 y 1500 pesos, según la tienda.", kind="big", label="MÉXICO · ESTÁNDAR", value="~$1,300–1,500", sub="pesos · según la tienda"),
   dict(say="Y no hay edición de colección: solo existen estas dos.", kind="text", head="Sin edición de *colección*", sub="Solo Estándar y Ultimate"),
   CTA,
  ]),
 dict(
  id="04_peso", pal=0,
  title="GTA 6 pesa más de 200 GB: prepara tu consola #Shorts",
  desc="La descarga de GTA 6 llega hasta 212 GB y la edición física no trae disco. Cómo dejar la precarga lista en PS5 y Xbox Series antes de la medianoche del 19 de noviembre.",
  tags="gta 6 peso, gta 6 cuánto pesa, gta 6 gb, gta 6 precarga, gta 6 preload, gta 6 descarga, gta 6 físico sin disco",
  beats=[
   dict(say="GTA 6 pesa más de 200 gigas. ¿Tienes espacio?", kind="hook", kicker="PRECARGA", head="¿Tienes *espacio* para GTA 6?"),
   dict(say="La descarga llega hasta 212 gigas.", kind="bar", label="TAMAÑO DE DESCARGA", target=212, unit="GB", sub="hasta"),
   dict(say="La precarga está abierta desde el 10 de noviembre, en PS5 y en Xbox Series.", kind="big", label="PRECARGA ABIERTA DESDE", value="10 NOV", sub="PS5 · Xbox Series X|S"),
   dict(say="Y la edición física no trae disco: en la caja viene un código de descarga.", kind="text", head="La caja *no trae disco*", sub="Trae un código de descarga"),
   dict(say="Así que todos descargan.", kind="text", head="*Todos* descargan", sub=""),
   dict(say="Tres pasos: libera espacio, deja la descarga hoy mismo, y pon la consola en modo reposo.", kind="list", title="Hazlo hoy",
        items=[("num","Libera espacio",""),("num","Inicia la descarga",""),("num","Modo reposo","")]),
   dict(say="Con internet lento puede tardar muchas horas. No lo dejes para el miércoles.", kind="text", head="No lo dejes para el *miércoles*", sub="Con internet lento tarda horas"),
   dict(say="El juego queda bloqueado hasta la medianoche del 19.", kind="big", label="BLOQUEADO HASTA", value="00:00", sub="jueves 19 · hora local"),
   CTA,
  ]),
 dict(
  id="05_online", pal=1,
  title="¿GTA 6 trae Online el día 1? #Shorts",
  desc="GTA 6 sale el 19 de noviembre de 2026 como experiencia para un jugador. Rockstar no ha anunciado modo online ni fecha. Lo confirmado, lo que es expectativa y qué pasa con el GTA Online actual.",
  tags="gta 6 online, gta online 2, gta 6 multijugador, gta 6 online fecha, gta 6 online día 1, gta 6 un jugador",
  beats=[
   dict(say="¿GTA 6 trae Online el día uno? No.", kind="stamp", q="¿GTA 6 trae Online el día 1?", stamp="NO"),
   dict(say="GTA 6 sale como una experiencia para un jugador.", kind="big", label="EL 19 DE NOVIEMBRE", value="1 JUGADOR", sub="solo modo historia"),
   dict(say="Rockstar no ha anunciado un modo online para GTA 6: ni nombre, ni fecha.", kind="list", title="Online de GTA 6",
        items=[("q","Anuncio","no hay"),("q","Nombre","no hay"),("q","Fecha","no hay")]),
   dict(say="Hay quien lo espera para 2027, pero son expectativas, no anuncios.", kind="text", head="¿2027? Es una *expectativa*", sub="No es un anuncio de Rockstar"),
   dict(say="Un dato: en 2013, GTA Online llegó unas dos semanas después de GTA 5.", kind="timeline", title="Así fue en 2013",
        points=[("17 SEP","GTA 5"),("1 OCT","GTA Online")]),
   dict(say="Y el GTA Online actual seguirá con soporte después del lanzamiento, según Take-Two.", kind="text", head="El Online actual *sigue*", sub="Con soporte, según Take-Two"),
   dict(say="Así que el jueves: modo historia, y nada más.", kind="text", head="Jueves: *modo historia*", sub="y nada más"),
   CTA,
  ]),
 dict(
  id="06_mapa", pal=2,
  title="El mapa de GTA 6: las 6 regiones de Leonida #Shorts",
  desc="GTA 6 no es solo Vice City. Repasamos las seis regiones confirmadas del estado de Leonida y qué se sabe (y qué no) del tamaño del mapa.",
  tags="gta 6 mapa, mapa gta 6, leonida, vice city, gta 6 regiones, gta 6 tamaño mapa, grassrivers, port gellhorn, mount kalaga",
  beats=[
   dict(say="El mapa de GTA 6 no es solo Vice City.", kind="hook", kicker="EL MAPA", head="No es solo *Vice City*"),
   dict(say="El juego transcurre en Leonida, un estado ficticio inspirado en Florida.", kind="big", label="EL ESTADO", value="LEONIDA", sub="ficticio · inspirado en Florida"),
   dict(say="Hay seis regiones confirmadas.", kind="big", label="REGIONES CONFIRMADAS", value="6", sub=""),
   dict(say="Vice City, la versión de Miami. Los Cayos de Leonida, islas tropicales. Grassrivers, los pantanos. Port Gellhorn, zona portuaria. Ambrosia. Y el parque nacional Mount Kalaga.", kind="list", title="Las 6 regiones",
        items=[("num","Vice City","su Miami"),("num","Cayos de Leonida","islas tropicales"),("num","Grassrivers","pantanos"),("num","Port Gellhorn","zona portuaria"),("num","Ambrosia",""),("num","Mount Kalaga","parque nacional")]),
   dict(say="¿Qué tan grande es? Rockstar no ha dado una cifra oficial.", kind="text", head="¿Tamaño? *Sin cifra oficial*", sub="Rockstar no la ha publicado"),
   dict(say="Eso de que es el doble que GTA 5 son estimaciones de fans.", kind="text", head="«El doble que GTA 5»", sub="Es una estimación de fans"),
   CTA2,
  ]),
 dict(
  id="07_personajes", pal=0,
  title="¿Quiénes son Jason y Lucia? La historia de GTA 6 #Shorts",
  desc="GTA 6 tiene dos protagonistas: Jason Duval y Lucia Caminos. Quiénes son, de qué va la historia y cómo funciona la relación entre ambos, sin spoilers.",
  tags="gta 6 personajes, jason y lucia, lucia caminos, jason duval, gta 6 historia, gta 6 protagonistas",
  beats=[
   dict(say="¿Quiénes son Jason y Lucia?", kind="hook", kicker="PROTAGONISTAS", head="¿Quiénes son *Jason y Lucia*?", icon="people"),
   dict(say="GTA 6 tiene dos protagonistas: Jason Duval y Lucia Caminos.", kind="vs",
        a=("JASON","Duval","protagonista"), b=("LUCIA","Caminos","protagonista"), mid="Y"),
   dict(say="Lucia es la primera protagonista mujer jugable de la saga principal.", kind="text", head="Lucia: la *primera* protagonista", sub="mujer jugable de la saga principal"),
   dict(say="Jason, según Rockstar, trabajó para traficantes en los Cayos de Leonida.", kind="text", head="Jason: pasado en *los Cayos*", sub="Trabajó para traficantes locales"),
   dict(say="La historia: una conspiración criminal que se extiende por todo el estado.", kind="text", head="Una *conspiración* criminal", sub="por todo el estado de Leonida"),
   dict(say="Y el centro de todo es la relación entre los dos: el juego tiene un sistema de relación de pareja.", kind="big", label="EL CENTRO DE LA HISTORIA", value="LOS DOS", sub="con sistema de relación"),
   dict(say="Además, puedes alternar entre ambos mientras juegas.", kind="text", head="*Alternas* entre ambos", sub="mientras juegas"),
   CTA2,
  ]),
 dict(
  id="08_plataformas", pal=1,
  title="¿GTA 6 sale en PS4 o Switch 2? Plataformas confirmadas #Shorts",
  desc="GTA 6 sale el 19 de noviembre de 2026 en PS5 y Xbox Series X|S, con mejoras en PS5 Pro. No sale en PS4 ni Xbox One, y no hay versión anunciada para Switch 2 ni PC.",
  tags="gta 6 ps4, gta 6 switch 2, gta 6 plataformas, gta 6 xbox one, gta 6 ps5 pro, gta 6 30 fps, gta 6 consolas",
  beats=[
   dict(say="¿GTA 6 sale en PS4? ¿Y en Switch 2? Aclaramos todo.", kind="hook", kicker="PLATAFORMAS", head="¿En *PS4*? ¿En *Switch 2*?"),
   dict(say="Sale en PS5 y en Xbox Series X y S.", kind="list", title="Día 1",
        items=[("ok","PS5",""),("ok","Xbox Series X",""),("ok","Xbox Series S","")]),
   dict(say="En PS5 Pro tiene mejoras: imagen más nítida y sombras con trazado de rayos.", kind="list", title="En PS5 Pro",
        items=[("ok","Imagen más nítida",""),("ok","Sombras con","trazado de rayos")]),
   dict(say="No sale en PS4 ni en Xbox One.", kind="list", title="Generación anterior",
        items=[("no","PS4",""),("no","Xbox One","")]),
   dict(say="Switch 2: no hay versión anunciada. PC: tampoco.", kind="list", title="Sin anunciar",
        items=[("q","Switch 2",""),("q","PC","")]),
   dict(say="Y apunta esto: el objetivo en consolas es de 30 cuadros por segundo.", kind="big", label="OBJETIVO EN CONSOLAS", value="30 FPS", sub="cuadros por segundo"),
   CTA,
  ]),
 dict(
  id="09_novedades", pal=2,
  title="6 novedades confirmadas de GTA 6 que cambian el juego #Shorts",
  desc="Seis mecánicas que Rockstar mostró en el Extended Look de GTA 6: seis estrellas de búsqueda, Perfil Criminal, testigos y cámaras, clonador de llaves, armas a la vista y gimnasio.",
  tags="gta 6 novedades, gta 6 gameplay, gta 6 jugabilidad, gta 6 perfil criminal, gta 6 seis estrellas, gta 6 extended look, gta 6 mecánicas",
  beats=[
   dict(say="Seis novedades confirmadas de GTA 6.", kind="hook", kicker="JUGABILIDAD", head="*6 novedades* confirmadas", icon="stars"),
   dict(say="Uno: vuelven las seis estrellas de búsqueda. GTA 5 tenía cinco.", kind="num", n=1, head="Vuelven las *6 estrellas*", sub="GTA 5 tenía cinco", icon="stars"),
   dict(say="Dos: el Perfil Criminal, que registra cómo te comportas durante todo el juego.", kind="num", n=2, head="*Perfil Criminal*", sub="Registra cómo te comportas"),
   dict(say="Tres: testigos y cámaras arman una descripción de ti.", kind="num", n=3, head="*Testigos* y cámaras", sub="Arman tu descripción"),
   dict(say="Cuatro: los autos nuevos piden un clonador de llaves para robarlos.", kind="num", n=4, head="*Clonador* de llaves", sub="Para robar autos nuevos"),
   dict(say="Cinco: la gente reacciona si caminas con armas a la vista.", kind="num", n=5, head="Armas *a la vista*", sub="La gente reacciona"),
   dict(say="Y seis: el gimnasio y lo que consumes cambian tus estadísticas.", kind="num", n=6, head="*Gimnasio* y consumibles", sub="Cambian tus estadísticas"),
   dict(say="Todo salió en el Extended Look de 26 minutos que Rockstar mostró en agosto.", kind="big", label="FUENTE: EXTENDED LOOK", value="26 MIN", sub="mostrado por Rockstar en agosto"),
   CTA2,
  ]),
 dict(
  id="10_analisis", pal=0,
  title="GTA 6: ¿esperar las reseñas o comprar ya? #Shorts",
  desc="Según reportes, las reseñas de GTA 6 saldrían el miércoles 18 de noviembre, un día antes del lanzamiento. No está confirmado por Rockstar. Qué hacer si ya lo vas a comprar y qué hacer si tienes dudas.",
  tags="gta 6 reseñas, gta 6 análisis, gta 6 review, gta 6 metacritic, gta 6 embargo, gta 6 vale la pena, gta 6 notas",
  beats=[
   dict(say="¿Esperar las reseñas de GTA 6, o comprar ya?", kind="hook", kicker="RESEÑAS", head="¿Esperar las *reseñas*?", icon="gauge"),
   dict(say="Según reportes, las reseñas saldrían el miércoles 18, un día antes del lanzamiento.", kind="big", label="RESEÑAS · SEGÚN REPORTES", value="18 NOV", sub="miércoles · un día antes"),
   dict(say="Ojo: Rockstar no ha confirmado esa fecha.", kind="text", head="*Sin confirmar* por Rockstar", sub="Tómalo como reporte"),
   dict(say="Si se cumple, habrá notas antes de que tu juego se desbloquee.", kind="text", head="Notas *antes* de jugar", sub="si el reporte se cumple"),
   dict(say="¿Lo vas a comprar sí o sí? Precarga ya: son hasta 212 gigas.", kind="bar", label="SI YA LO DECIDISTE: PRECARGA", target=212, unit="GB", sub="hasta"),
   dict(say="¿Tienes dudas? Espera unas horas. Es una descarga digital: no se agota.", kind="text", head="¿Dudas? *Espera* unas horas", sub="Es digital: no se agota"),
   dict(say="Y cuidado con los spoilers desde el miércoles: Nueva Zelanda juega primero.", kind="text", head="Cuidado con los *spoilers*", sub="Nueva Zelanda juega primero", icon="globe"),
   CTA,
  ]),
]

# Pronunciación para la voz (texto escrito -> como debe sonar)
PRON = [
 ("GTA 6", "ge te a seis"), ("GTA 5", "ge te a cinco"), ("GTA", "ge te a"),
 ("PS5 Pro", "pleiestéishon cinco pro"), ("PS5", "pleiestéishon cinco"), ("PS4", "pleiestéishon cuatro"),
 ("Xbox Series X y S", "équis box síris équis y ese"), ("Xbox Series", "équis box síris"), ("Xbox One", "équis box uán"),
 ("Switch 2", "suích dos"), ("PC", "pe ce"),
 ("Vice City", "vais síti"), ("Rockstar", "rók estar"), ("Take-Two", "téik tu"), ("GamesBeat", "guéims bit"),
 ("Online", "onláin"), ("online", "onláin"), ("Ultimate", "áltimeit"), ("Vintage", "víntach"), ("pack", "pak"),
 ("Jason Duval", "yéison duvál"), ("Jason", "yéison"), ("Lucia", "Lucía"),
 ("Grassrivers", "gras rívers"), ("Port Gellhorn", "port guéljorn"), ("Mount Kalaga", "máunt kalaga"),
 ("Extended Look", "exténded luk"), ("spoilers", "espóilers"),
 ("79 dólares con 99", "setenta y nueve dólares con noventa y nueve"), ("99 con 99", "noventa y nueve con noventa y nueve"),
 ("1300 y 1500", "mil trescientos y mil quinientos"),
 ("2027", "dos mil veintisiete"), ("2026", "dos mil veintiséis"), ("2015", "dos mil quince"), ("2013", "dos mil trece"),
 ("212", "doscientos doce"), ("200", "doscientos"),
]

def spoken(text):
    for a, b in PRON:
        text = text.replace(a, b)
    return text
