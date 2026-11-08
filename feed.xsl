<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RSS feed · AmitForHealth</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&amp;family=Lora:ital,wght@0,400;0,600;1,400&amp;family=Lato:wght@400;700&amp;display=swap"/>
<link rel="stylesheet" href="/style.css"/></head>
<body><main class="wrap">
<header class="top"><a href="/">← Amit Kumar</a></header>
<article class="post col3">
<p class="kicker"><a href="/">RSS feed</a></p>
<h1>Follow AmitForHealth in a feed reader</h1>
<p class="dek">This page is a feed. Copy its address into Feedly, Inoreader, NetNewsWire or any RSS app, and new essays will arrive there automatically.</p>
<p class="meta">Feed address: <strong>https://amitforhealth.in/feed.xml</strong></p>
<div class="body">
<p>Prefer email? <a href="/#subscribe">Get the monthly email</a> instead.</p>
<h2>Latest essays</h2>
<div class="group"><ul>
<xsl:for-each select="rss/channel/item">
<li><xsl:attribute name="class">col<xsl:value-of select="(position()-1) mod 5"/></xsl:attribute>
<a><xsl:attribute name="href"><xsl:value-of select="substring-after(link,'amitforhealth.in')"/></xsl:attribute><xsl:value-of select="title"/></a>
<div class="small"><xsl:value-of select="substring(pubDate,6,11)"/></div></li>
</xsl:for-each>
</ul></div>
</div>
</article>
</main></body></html>
</xsl:template>
</xsl:stylesheet>
