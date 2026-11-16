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
4. Guiones en `src/content.py` (30-45 s; gancho en la primera frase; datos comprobados con fuente).
5. `python3 src/audio.py <ids>` y luego `python3 src/render.py render <ids>`. Revisar fotogramas antes de dar por bueno el lote.
6. Subir los MP4 a una release de GitHub (`gh release create semana-AAAA-MM-DD out/*.mp4`) e importarlos con `vidiq_video_upload` usando la URL de descarga.
7. Crear un borrador por vídeo con `publishAt` en las mejores horas según `data/learnings.md`. Por defecto: 19:00-21:00 hora de Ciudad de México.
8. Enviar al dueño el resumen del lote y esperar su "sí". Después, `vidiq_social_post_publish` y actualizar `data/published.json`.

## Créditos de vidIQ
El plan da 150 al mes. Presupuesto: unos 25 por semana (búsquedas a 5 cada una).


## Pendientes de publicar (ya montados)
05_online, 06_mapa, 07_personajes, 08_plataformas, 09_novedades, 10_analisis
