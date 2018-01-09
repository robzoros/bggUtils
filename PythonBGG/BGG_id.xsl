<?xml version="1.0" encoding="UTF-8"?>	
<!--
    Created on : 17 de septiembre de 2017
    Author     : Roberto
    Description:
        Extrae el ID del juego de una colección de BGG
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="text" encoding="utf-8" indent="yes"/>
	<xsl:template match="items">
		<xsl:for-each select="item">
    		<xsl:value-of select="@objectid"/>
    		<xsl:text>&#xa;</xsl:text>
		</xsl:for-each>
    </xsl:template>	
	

</xsl:stylesheet>
