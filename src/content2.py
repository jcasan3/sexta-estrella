# -*- coding: utf-8 -*-
"""Guiones v2 (estilo dinámico). Cada beat: say (voz y subtítulos), scene (fondo animado),
fx (gráfico principal) y campos propios del fx. En títulos, *palabra* = resaltada."""
CHANNEL = "SEXTA ESTRELLA"
HANDLE = "@laasextaestrella"

CTA = dict(say="Sígueme para más de GTA 6 cada día.", scene="city", fx="cta")

VIDEOS2 = [
 dict(id="05_online_v2", title="¿GTA Online 2 llega el jueves con GTA 6? #Shorts",
  desc="GTA 6 sale el 19 de noviembre de 2026 solo con modo historia. Rockstar no ha anunciado modo online ni fecha. Lo que pasó en 2013 con GTA Online y qué pasa con el GTA Online actual.",
  hashtags="#GTA6 #GTAVI #GTAOnline #GTA6Español #Shorts",
  tags=["gta 6","gta6","gta vi","gta 6 español","gta 6 online","gta online 2","gta 6 multijugador","gta 6 online fecha","gta 6 online día 1"],
  beats=[
   dict(say="¿GTA Online 2 llega el jueves?", scene="city", fx="title", text="¿GTA *ONLINE 2* EL JUEVES?", sfx="boom"),
   dict(say="Respuesta corta: no.", scene="police", fx="stamp", text="NO", sfx="slam"),
   dict(say="El 19 de noviembre llega solo el modo historia: Vice City, Jason y Lucía.", scene="beach", fx="big", label="EL 19 DE NOVIEMBRE", value="1 JUGADOR", sub="Vice City · Jason · Lucía", sfx="boom"),
   dict(say="Rockstar no ha anunciado online: ni nombre, ni fecha.", scene="city", fx="list", items=[("q","Nombre"),("q","Fecha"),("q","Detalles")]),
   dict(say="Ojo al dato: en 2013, GTA Online llegó dos semanas después de GTA 5.", scene="highway", fx="timeline", points=[("17 SEP 2013","GTA 5"),("1 OCT 2013","GTA ONLINE")], sfx="riser"),
   dict(say="Por eso muchos creen que esta vez también llegará después. Pero hoy es solo una expectativa.", scene="city", fx="title", text="*EXPECTATIVA*, NO ANUNCIO"),
   dict(say="Mientras tanto, el GTA Online de siempre sigue activo, según Take-Two.", scene="highway", fx="big", label="SEGÚN TAKE-TWO", value="SIGUE", sub="el GTA Online actual", sfx="boom"),
   CTA,
  ]),
 dict(id="08_plataformas_v2", title="¿GTA 6 en PS4? Malas noticias #Shorts",
  desc="GTA 6 sale el 19 de noviembre de 2026 solo en PS5 y Xbox Series X|S, con mejoras en PS5 Pro. No sale en PS4 ni Xbox One, y no hay versión anunciada para Switch 2 ni PC.",
  hashtags="#GTA6 #GTAVI #PS5 #GTA6Español #Shorts",
  tags=["gta 6","gta6","gta vi","gta 6 español","gta 6 ps4","gta 6 switch 2","gta 6 plataformas","gta 6 xbox one","gta 6 ps5 pro","gta 6 30 fps","que consola comprar para gta 6"],
  beats=[
   dict(say="Si tienes PS4, tengo malas noticias.", scene="police", fx="title", text="¿TIENES *PS4*?", sfx="boom"),
   dict(say="GTA 6 no sale en PS4, ni en Xbox One.", scene="city", fx="list", items=[("no","PS4"),("no","Xbox One")], sfx="slam"),
   dict(say="Solo llega a PS5 y Xbox Series, este jueves 19.", scene="highway", fx="list", items=[("ok","PS5"),("ok","Xbox Series X"),("ok","Xbox Series S")]),
   dict(say="Y en PS5 Pro se ve mejor: imagen más nítida y sombras con trazado de rayos.", scene="beach", fx="big", label="MEJORAS EN", value="PS5 PRO", sub="más nitidez · sombras con trazado de rayos", sfx="boom"),
   dict(say="¿Switch 2? ¿PC? Ninguna versión anunciada. Por ahora.", scene="city", fx="list", items=[("q","Switch 2"),("q","PC")]),
   dict(say="Dato clave: el objetivo en consolas es de 30 cuadros por segundo.", scene="highway", fx="big", label="OBJETIVO EN CONSOLAS", value="30 FPS", sub="cuadros por segundo", sfx="boom"),
   dict(say="Así que, para pisar Vice City el jueves, necesitas consola nueva.", scene="beach", fx="title", text="PARA *VICE CITY*: CONSOLA NUEVA"),
   CTA,
  ]),
 dict(id="09_novedades_v2", title="6 cosas de GTA 6 que nunca viste en GTA 5 #Shorts",
  desc="Seis mecánicas que Rockstar mostró en el gameplay extendido de GTA 6: seis estrellas de búsqueda, Perfil Criminal, testigos y cámaras, clonador de llaves, armas a la vista y gimnasio.",
  hashtags="#GTA6 #GTAVI #GTA6Gameplay #GTA6Español #Shorts",
  tags=["gta 6","gta6","gta vi","gta 6 español","gta 6 novedades","gta 6 gameplay","gta 6 jugabilidad","gta 6 perfil criminal","gta 6 seis estrellas","gta 6 extended look"],
  beats=[
   dict(say="Seis cosas de GTA 6 que nunca viste en GTA 5.", scene="police", fx="title", text="*6 COSAS* QUE GTA 5 NO TENÍA", sfx="boom"),
   dict(say="Uno: vuelven las seis estrellas de búsqueda. En GTA 5 eran cinco.", scene="police", fx="stars", n=1, text="6 ESTRELLAS", sfx="siren"),
   dict(say="Dos: el Perfil Criminal registra cómo te comportas durante todo el juego.", scene="police", fx="num", n=2, text="PERFIL *CRIMINAL*", sfx="slam"),
   dict(say="Tres: testigos y cámaras arman tu descripción. Si te ven, te buscan.", scene="city", fx="num", n=3, text="TESTIGOS Y *CÁMARAS*", sfx="slam"),
   dict(say="Cuatro: para robar autos nuevos necesitas un clonador de llaves.", scene="highway", fx="num", n=4, text="CLONADOR DE *LLAVES*", sfx="slam"),
   dict(say="Cinco: si caminas armado por Vice City, la gente reacciona.", scene="city", fx="num", n=5, text="ARMAS *A LA VISTA*", sfx="slam"),
   dict(say="Y seis: el gimnasio y lo que comes cambian tus estadísticas.", scene="beach", fx="num", n=6, text="*GIMNASIO* Y COMIDA", sfx="slam"),
   dict(say="Todo esto lo mostró Rockstar en sus 26 minutos de gameplay de agosto.", scene="city", fx="big", label="GAMEPLAY DE ROCKSTAR", value="26 MIN", sub="mostrado en agosto", sfx="boom"),
   CTA,
  ]),
 dict(id="06_mapa_v2", title="El mapa de GTA 6 es más que Vice City #Shorts",
  desc="GTA 6 transcurre en Leonida, un estado ficticio inspirado en Florida. Las seis regiones confirmadas y lo que se sabe (y lo que no) del tamaño del mapa.",
  hashtags="#GTA6 #GTAVI #ViceCity #GTA6Español #Shorts",
  tags=["gta 6","gta6","gta vi","gta 6 español","gta 6 mapa","mapa gta 6","leonida","vice city","gta 6 regiones","gta 6 tamaño mapa","grassrivers","port gellhorn","mount kalaga"],
  beats=[
   dict(say="El mapa de GTA 6 es mucho más que Vice City.", scene="map", fx="title", text="MÁS QUE *VICE CITY*", sfx="boom", pin=None),
   dict(say="Todo pasa en Leonida, un estado inspirado en Florida.", scene="map", fx="big", label="EL ESTADO", value="LEONIDA", sub="ficticio · inspirado en Florida", pin=None),
   dict(say="Seis regiones confirmadas. Vamos una por una.", scene="map", fx="big", label="REGIONES CONFIRMADAS", value="6", sub="", sfx="boom", pin="all"),
   dict(say="Vice City: la versión de Miami. Playas, neones y mucho dinero.", scene="map", fx="pin", text="VICE CITY", sub="su Miami", pin=0, sfx="pop"),
   dict(say="Los Cayos de Leonida: islas tropicales.", scene="map", fx="pin", text="CAYOS DE LEONIDA", sub="islas tropicales", pin=1, sfx="pop"),
   dict(say="Grassrivers: pantanos salvajes.", scene="map", fx="pin", text="GRASSRIVERS", sub="pantanos", pin=2, sfx="pop"),
   dict(say="Port Gellhorn: la zona portuaria.", scene="map", fx="pin", text="PORT GELLHORN", sub="zona portuaria", pin=3, sfx="pop"),
   dict(say="Ambrosia. Y el parque nacional Mount Kalaga.", scene="map", fx="pin", text="AMBROSIA · MOUNT KALAGA", sub="parque nacional", pin=[4, 5], sfx="pop"),
   dict(say="¿Y el tamaño? Rockstar no ha dado cifra. Lo del doble que GTA 5 es cosa de fans.", scene="city", fx="title", text="¿TAMAÑO? *SIN CIFRA OFICIAL*"),
   CTA,
  ]),
 dict(id="07_personajes_v2", title="Jason y Lucía: quiénes son en GTA 6 #Shorts",
  desc="Los dos protagonistas de GTA 6, Jason Duval y Lucía Caminos, y los personajes que Rockstar ya presentó. Sin spoilers.",
  hashtags="#GTA6 #GTAVI #JasonYLucia #GTA6Español #Shorts",
  tags=["gta 6","gta6","gta vi","gta 6 español","gta 6 personajes","jason y lucia","lucia caminos","jason duval","gta 6 historia","gta 6 protagonistas","cal hampton","boobie ike"],
  beats=[
   dict(say="Jason y Lucía: la pareja más peligrosa de Vice City.", scene="beach", fx="title", text="*JASON Y LUCÍA*", sfx="boom"),
   dict(say="Por primera vez en la saga principal hay una protagonista mujer jugable: Lucía Caminos.", scene="city", fx="big", label="POR PRIMERA VEZ", value="LUCÍA", sub="protagonista jugable de la saga principal", sfx="boom"),
   dict(say="Lucía pasó por la Penitenciaría de Leonida por defender a su familia.", scene="police", fx="title", text="PENITENCIARÍA DE *LEONIDA*", sfx="slam"),
   dict(say="Jason Duval: exmilitar que acabó trabajando para traficantes en los Cayos.", scene="beach", fx="big", label="EL OTRO PROTAGONISTA", value="JASON", sub="exmilitar · los Cayos de Leonida", sfx="boom"),
   dict(say="Juntos se meten en una conspiración criminal que cruza todo Leonida.", scene="highway", fx="title", text="UNA *CONSPIRACIÓN* CRIMINAL", sfx="riser"),
   dict(say="Y no están solos: Cal Hampton, Boobie Ike, Raul Bautista, Dre'Quan Priest...", scene="city", fx="list", items=[("star","Cal Hampton"),("star","Boobie Ike"),("star","Raul Bautista"),("star","Dre'Quan Priest")]),
   dict(say="Y puedes cambiar entre Jason y Lucía mientras juegas.", scene="beach", fx="vs", a="JASON", b="LUCÍA", sfx="boom"),
   CTA,
  ]),
]

PRON = [
 ("GTA Online 2", "ge te a onláin dos"), ("GTA 6", "ge te a seis"), ("GTA 5", "ge te a cinco"), ("GTA Online", "ge te a onláin"), ("GTA", "ge te a"),
 ("PS5 Pro", "pe ese cinco pro"), ("PS5", "pe ese cinco"), ("PS4", "pe ese cuatro"),
 ("Xbox Series", "equis box síries"), ("Xbox One", "equis box uan"), ("Switch 2", "suich dos"), ("PC", "pe ce"),
 ("Vice City", "váis síti"), ("Rockstar", "rokstar"), ("Take-Two", "teik tu"),
 ("online", "onláin"), ("Online", "onláin"),
 ("Jason Duval", "yéison duval"), ("Jason", "yéison"),
 ("Grassrivers", "gras ríbers"), ("Port Gellhorn", "port guéljorn"), ("Mount Kalaga", "maunt kalaga"),
 ("Cal Hampton", "kal jámpton"), ("Boobie Ike", "búbi áik"), ("Dre'Quan Priest", "dri kuan prist"),
 ("2013", "dos mil trece"), ("26", "veintiséis"), ("30", "treinta"), ("19", "diecinueve"),
]

def spoken(t):
    for a, b in PRON:
        t = t.replace(a, b)
    return t
