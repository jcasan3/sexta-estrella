# Sexta Estrella: cómo funciona el canal

Canal de Shorts sobre GTA 6 en español neutro/latino. YouTube: @laasextaestrella (UC0DbF4dRYCmkdu-4p8xmp3w), publicado con vidIQ. TikTok lo sube el dueño a mano.

## Reglas fijas
- Solo datos confirmados. Si algo es rumor o reporte, se dice en el vídeo.
- Sin material de Rockstar (gameplay, tráilers, logo, arte). Gráficos, música y voz propios.
- YouTube: siempre **público**, categoría 20 (Videojuegos).
- El dueño aprueba cada lote semanal con un "sí" antes de publicar (vidIQ lo exige). Una sola aprobación programa toda la semana.
- Variar formatos entre vídeos (política de "contenido no auténtico" de YouTube): no repetir la misma estructura dos veces seguidas.

## Ciclo semanal (lunes)
1. `./setup.sh`
2. Rendimiento: estadísticas de los vídeos publicados con vidIQ (vistas, retención, suscriptores). Anotar en `data/learnings.md` qué temas, ganchos, títulos y horas funcionaron y cuáles no.
3. Temas: `vidiq_keyword_research` (questions/rising, language es) más búsqueda web de noticias de la semana. Elegir 7 temas con demanda y poca competencia que no estén ya en `data/published.json`.
4. Guiones en `src/content2.py` (estilo v2: 25-35 s, frases cortas, gancho fuerte en el primer segundo, muchas referencias concretas a GTA 6: lugares de Leonida, personajes, mecánicas; datos comprobados con fuente en data/sources.md).
5. `python3 src/audio2.py <ids>` (voz Kokoro em_alex, efectos y música) y luego `python3 src/render2.py render <ids>`. Fondos animados disponibles: city, beach, highway, police, map. Gráficos: title, stamp, big, list, timeline, stars, num, pin, vs, cta. Revisar fotogramas antes de dar por bueno el lote. Si hace falta un fondo o gráfico nuevo, añadirlo a render2.py.
6. Subir los MP4 a una release de GitHub (`gh release create semana-AAAA-MM-DD out/*.mp4`) e importarlos con `vidiq_video_upload` usando la URL de descarga.
7. Crear un borrador por vídeo con `publishAt` en las mejores horas según `data/learnings.md`. Por defecto: 19:00-21:00 hora de Ciudad de México.
8. Enviar al dueño el resumen del lote y esperar su "sí". Después, `vidiq_social_post_publish` y actualizar `data/published.json`.

## Informe semanal para Vic (cada sábado)
Tabla con cada vídeo publicado: título, fecha, vistas, likes, comentarios y, si vidIQ lo da, duración media vista y % de retención. Después: qué funcionó y qué no, qué cambia en el siguiente lote (temas, ganchos, fondos, voz, horas). Guardar el informe en data/reports/AAAA-MM-DD.md.

## Mejora continua
Cada lote debe cambiar algo medible respecto al anterior a partir de los datos (gancho, duración, fondos, ritmo, temas). Anotar en data/learnings.md la hipótesis y el resultado la semana siguiente.

## Créditos de vidIQ
El plan da 150 al mes. Presupuesto: unos 25 por semana (búsquedas a 5 cada una).



## Vídeo extra por noticia (comprobación diaria)
Cada día se revisan las noticias de GTA 6 (solo búsqueda web, sin gastar créditos de vidIQ). Si hay algo gordo (parche importante, récord de ventas, anuncio de Rockstar sobre Online o PC, secreto viral), se hace un vídeo extra y se programa para ese mismo día a las 19:00 de México, con el "sí" del dueño. Máximo un extra al día. Si no hay nada relevante, no se hace nada y no se avisa. Antes de elegir el tema, revisar data/published.json para no repetirlo.
