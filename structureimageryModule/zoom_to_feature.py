import arcpy, os



str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'Upper Yaquina Near-Stream Structures (scratch).mxd'
str_df_zoom_name = r'Zoom to Feature'
str_df_state_name = r'Overall Watershed'
str_strc_cent = r'PointPotentialStructureCentroids'
str_strc_poly = r'Potential Structures'
str_strm_line = r'NHD Flowlines'

str_path_export = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\python\structure-imagery\images'
str_file_image_export_prefix = 'strt_'

memSelLyr = "in_memory" + "\\" + "memSelLayer"

mxd_cur = get_mxd(str_path_mxd, str_file_mxd)


SelLayer = arcpy.mapping.ListLayers(mxd_cur, str_strc_poly, df_zoom)[0]

mylist = unique_values(SelLayer,'FID')

# make all layers not visible
for lyr in df_zoom:
    if lyr.isGroupLayer == True:
        #print "Layers in " + lyr.name
        lyr_g = arcpy.mapping.ListLayers(lyr)
        for lyr_in_g in lyr_g:
            #print lyr_in_g.name
            lyr_in_g.visible = False
        #print ""
        del lyr_in_g, lyr_g
    else:
        print lyr.name
        lyr.visble = False
lyr = arcpy.mapping.ListLayers(mxd_cur, str_strm_line, df_zoom)[0]
lyr.visible = True
del lyr
arcpy.RefreshTOC()

for curFID in mylist:
    query = '"FID" = {}'.format(curFID)
    # Process: Select
    arcpy.Select_analysis(SelLayer, memSelLyr, query)
    add_lyr = arcpy.mapping.Layer(memSelLyr)
    arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view=add_lyr, selection_type='NEW_SELECTION', where_clause=query)
    df_zoom.panToExtent(add_lyr.getSelectedExtent())
    #df.zoomToSelectedFeatures()
    add_lyr.visible = True
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_pg.png')
    arcpy.Delete_management(add_lyr)
    arcpy.Delete_management("in_memory")
    del query

