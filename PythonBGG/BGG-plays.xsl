<?xml version="1.0" encoding="UTF-8"?>	
<!--
    Created on : 1 de enero de 2018
    Author     : Roberto
    Description:
        Extrae los datos de una partida de las partidas jugadas en BGG
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="text" encoding="utf-8" indent="yes"/>
	<xsl:template match="plays">
		<xsl:for-each select="play">
    		<xsl:value-of select="@date"/>
    		<xsl:text>,</xsl:text>
    		<xsl:value-of select="@quantity"/>
    		<xsl:text>,</xsl:text>
    		<xsl:value-of select="@length"/>
    		<xsl:text>,</xsl:text>
    		<xsl:value-of select="@location"/>
    		<xsl:text>,</xsl:text>
    		<xsl:value-of select="item/@name"/>
    		<xsl:text>,</xsl:text>
    		<xsl:value-of select="item/@objectid"/>
    		<xsl:for-each select="players/player">
        		<xsl:text>,</xsl:text>
        		<xsl:value-of select="@name"/>
    		</xsl:for-each>
    		<xsl:text>&#xa;</xsl:text>
		</xsl:for-each>
    </xsl:template>	
</xsl:stylesheet>
