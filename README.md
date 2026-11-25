# Bibelstudium-Ecke – statische Website

Private, lokale Website mit der Neue-Welt-Übersetzung (aus den RTF-Dateien im Ordner
`Bibelprojekt`). **Keine offizielle Website von Jehovas Zeugen**, das steht auch im Fuß jeder Seite.

## Öffnen

Doppelklick auf `website/index.html`. Alle Seiten sind reine HTML-Dateien mit relativen Links
und funktionieren ohne Server und ohne Internet (nur die Schriften Noto Sans und Noto Serif
kommen von Google Fonts; offline wird eine Systemschrift verwendet).

## Inhalt

| Seite | Inhalt |
|---|---|
| `index.html` | Start: Bibelvers für heute, „So studierst du“ in 4 Schritten, Themen, Buchgruppen |
| `bibel.html` | 66 Bücher, gegliedert nach Hebräischen und Christlichen Griechischen Schriften |
| `bibel/<buch>/index.html` | Buchseite: Schreiber, Ort, Zeit, Kapitelraster, Übersicht des Buches |
| `bibel/<buch>/<kapitel>.html` | Kapitel mit Überschriften, seitlicher Übersicht, Kapitelwahl, vor/zurück; Verse direkt verlinkbar (`#v16`) |
| `themen.html` | 8 Themen (Gottes Name, Königreich, Paradies, Tod und Auferstehung, Lösegeld, Jesus Christus, Beten, Familie) – nur Bibelstellen |
| `suche.html` | Volltextsuche über 31 078 Verse, Filter, „Ganze Wörter“, `"genauer Satz"`, `-Wort` |
| `lexikon.html`, `konkordanz.html` | Worterklärungen und Konkordanz, A–Z, Filter, Bibelstellen verlinkt |
| `vorwort.html`, `anhang-a.html`, `anhang-b.html` | Texte aus der Vorlage |
| `hinweise.html` | Herkunft der Überschriften, Speicherung, Hinweis „nicht offiziell“ |

## Überschriften

**Nur Überschriften aus der Vorlage** (Buchübersicht der Neue-Welt-Übersetzung) – **keine selbst
verfassten Überschriften**. Wo die Vorlage mehrere Überschriften in einer Zeile zusammenfasst
(z. B. Mt 5: „Wut (Vers 21 bis 26), Ehebruch (Vers 27 bis 30) …“), stehen sie einzeln am Vers.
Hauptüberschriften in Großbuchstaben mit Linie, Unterüberschriften mit gelbem Strich.

## Design und Themes

Farbwelt angelehnt an jw.org (Violett, viel Weiß, ruhige Grautöne), Formensprache angelehnt an IKEA
(kräftige Überschriften, flache Kacheln, Pillen-Buttons, nummerierte Schritte, Gelb als Akzent).
Kein fremdes Logo, keine fremden Texte. Unter **„Darstellung“** (oben rechts):

### 61 Themes in 10 Gruppen

Im Fenster „Darstellung“ sind die Gruppen aufklappbar; die Gruppe mit dem aktiven Theme öffnet sich
automatisch. Die 34 neueren Themes stehen als Daten in `tools/themes_extra.py` und werden beim
Erzeugen zu `assets/themes-extra.css`.

| Gruppe | Themes |
|---|---|
| Automatisch | **Hell/Dunkel wie Windows** (Standard bzw. Nacht, wechselt beim Zurückkehren ins Fenster), **Jahreszeit** (Frühling März–Mai, Sommer Juni–Aug., Herbst Sep.–Nov., Winter Dez.–Feb.) |
| Klassisch | Standard (Violett), Nacht, Sepia, **Druckbibel** (Papierton, EB Garamond, zwei Spalten mit Trennlinie, Kopfzeile, Überschriften in Kapitälchen), **Schreibmaschine** (wie ein alter getippter Bericht: Papier mit feinen Linien, Schreibmaschinenschrift Courier Prime und für Überschriften Special Elite, leicht verlaufende Tinte, Versnummern in Rot wie bei zweifarbigen Farbbändern, Unterstreichungen statt Farbflächen, Buttons in eckigen Klammern) |
| Historisch & biblisch | **Schriftrolle** (Pergament, schmale Spalten), **Tontafel** (erdige Töne, eingeprägte Schrift Cinzel), **Altes Druckbuch** (gebrochene Schrift, rote Initialen), **Stiftshütte** (Blau, Purpur, Karmesin, Gold, feines Leinen nach 2. Mose) |
| Papier & Schreibgeräte | **Notizbuch** (kariertes Papier, Handschrift-Überschriften Caveat, Textmarker), **Karteikarte** (jeder Absatz als linierte Karte mit roter Kopfzeile), **Zeitung** (Schlagzeilen-Schrift Playfair, 2–3 Spalten), **Blaupause** (weiße Linien auf Blau, technisches Raster) |
| Technik & Retro | **Terminal** (grün auf Schwarz, VT323, Bildschirmzeilen, blinkender Cursor), **E-Reader** (Grau, keine Farben, keine Animationen), **Pixel / 8-Bit** (Press Start 2P, Pixelrahmen), **Fernschreiber** (Großbuchstaben, Endlospapier mit Lochrand) |
| Im Stil von | JW.ORG, **JW Library**, **Wachtturm**, IKEA, Google, **Apple**, LEGO, Blau & Gelb, **Coca-Cola** (Rot, geschwungene Schrift Lobster, Welle), **Formel 1** (Titillium Web kursiv, Zielflaggen-Leiste, schräge Buttons), **Spotify** (Grün auf Schwarz, Montserrat), **Netflix** (Rot auf Schwarz, Bebas Neue), **Nintendo** (Rot, runde Formen, Nunito), **Starbucks** (Grün und Gold, Lora), **NASA** (Blau und Rot, Space Grotesk in Großbuchstaben), **YouTube** (Rot, Roboto, graue Pillen-Navigation), **Amazon** (dunkle Leiste, orange, gelbe Buttons), **Instagram** (Farbverlauf Violett–Rot–Orange, Inter), **Wikipedia** (Lexikon-Überschriften, blaue Links), **Notion** (minimalistisch, Inter), **Windows 95** (graue 3D-Fenster, Titelleisten, Türkis), **Microsoft Word** (Dokumentseite auf grauem Grund, Calibri) |
| Natur | Wald, Meer, Wüste, Paradies (von Himmelblau zu Grün) |
| Stimmungen | **Morgenandacht** (sanfte Morgenröte), **Abendlicht** (warm, wenig Blau), **Sternenhimmel** (Nachtblau mit Sternen, Psalm 147:4), **Garten** (Blüten- und Blattfarben) |
| Jahreszeiten | Frühling, Sommer, Herbst, Winter |
| Für die Augen | Hoher Kontrast, **Gelb auf Schwarz**, **Weiß auf Dunkelblau**, **Blendarm**, **Graustufen**, **Bernstein auf Schwarz**, **Großdruck** (30 px, Atkinson Hyperlegible, kräftige Linien), **Dunkelgrün** (cremefarbene Schrift) |

Bewusst keine Feiertags-Themes (z. B. Weihnachten oder Ostern).

**Kontrast geprüft (25.11.2026):** Für alle 59 festen Themes wurde automatisch das Kontrastverhältnis
nach WCAG gemessen: Startseite (Text, Navigation, Name, Startfläche, Logo) und Kapitelseite (Bibeltext,
Versnummern, Überschriften, Übersicht). Bibeltext mindestens 6,6 : 1, Fließtext mindestens 5,3 : 1.
Sechs Themes mussten dafür nachgebessert werden.

„Im Stil von“ heißt angelehnt: Farben, Schriften und Formen ähneln dem Vorbild, aber ohne Logos
oder Inhalte. Gemessen habe ich nur jw.org; alle anderen sind frei nachempfunden. Wo die
Originalschrift nicht frei erhältlich ist, wird eine ähnliche freie Schrift verwendet
(z. B. Titillium Web statt der Formel-1-Schrift, Montserrat statt Spotifys Circular).

### Lese-Optionen (mit jedem Theme kombinierbar)

- **Schrift im Bibeltext:** wie im Theme, mit Serifen (Noto Serif), ohne Serifen (Noto Sans),
  besonders gut lesbar (Atkinson Hyperlegible), klassisch (EB Garamond)
- **Schriftgröße** 15–40 px, **Zeilenabstand** 1,4–2,6, **Lesebreite** 40–110 Zeichen
- **Vers für Vers:** jeder Vers in einer eigenen Zeile
- **Zweispaltig:** auf Bildschirmen ab 1000 px Breite
- **Weite Abstände:** mehr Abstand zwischen Buchstaben, Wörtern und Absätzen
- **Lesezeile:** dunkelt alles außer der Zeile unter Maus oder Finger ab; auf dunklen Themes stärker
- **Fokus-Modus:** nur der Bibeltext, ohne Kopf, Seitenleiste und Fuß; beenden mit dem Knopf oben rechts oder mit Esc
- Überschriften ausblenden, Versnummern ausblenden, **Alles zurücksetzen**

### Hinweise zu einzelnen Themes

- **JW.ORG:** Werte am 25.11.2026 auf jw.org gemessen: Noto Sans überall (auch im Bibeltext),
  Hintergrund #f1f1f1, Text #292929, Links und Buttons #4a6da7, dazu ein Hellblau zum Markieren,
  eine schieferfarbene Startfläche und eckige Formen. Kein Logo und keine Texte von jw.org.
- **LEGO:** Schrift Outfit als freie Alternative zu LEGOs „Cera Pro“, kräftiges Rot, Gelb, Blau und
  Grün, dicke schwarze Kanten, Kacheln mit Noppen und Klötzchen-Schatten, eine Leiste aus Steinen.
- **IKEA:** Noto Sans überall, auch im Bibeltext. IKEAs eigene Schrift „Noto IKEA“ ist eine Variante
  davon und nicht frei erhältlich. Dazu fette, eng gesetzte Überschriften, eckige Kacheln, blaue
  runde Buttons, Gelb, schwarze Überschriftenlinien.
- **Google:** Überschriften in „Google Sans“, falls sie auf dem PC installiert ist, sonst Roboto
  (Googles freie Hausschrift); der Text in Roboto. Dazu Material-Farben, die vierfarbige Leiste,
  runde Karten und eine Suchleiste mit Schatten.

Die Einstellungen werden im Browser gespeichert (`localStorage`, Schlüssel `bse.einstellungen`) –
sonst speichert die Seite nichts.

## Neu erzeugen

```powershell
python -I website/tools/build_data.py   # nur nötig, wenn sich die RTF-Dateien ändern
python -I website/tools/build_site.py   # erzeugt alle HTML-Seiten neu
```

`build/bibel.json` ist eine Zwischendatei. Der Ordner `bibel/` wird bei jedem Lauf komplett neu erzeugt.

## Geprüft (25.11.2026)

- 1265 Seiten erzeugt; alle 134 255 internen Links und Vers-Anker automatisch geprüft. Nur 2 führen
  ins Leere, beide absichtlich: Joh 7:53 und 8:11 aus Anhang A. Diese Verse fehlen in der Vorlage,
  weil sie nicht in den ältesten Handschriften stehen.
- Behobener Vorlagenfehler: „Kapitel 5“ in Richter war nicht fett formatiert, deshalb rutschte
  die Gliederung von Kapitel 5 zu Kapitel 4.
- Im Browser getestet: Startseite, Mt 5 (11 Überschriften, 0 eigene), Ps 83:18-Sprung aus dem
  Suchfeld, Suche „Königreich Gottes“ (70 Treffer, Filter), Theme Blau & Gelb seitenübergreifend,
  Handy-Ansicht (1. Mose 3, Themen).
