import pandas as pd
import numpy as np
import re

fullcode = """
; Generated with MatterSlice 2.20.6
; filamentDiameter = 3
; extrusionWidth = 0.5
; firstLayerExtrusionWidth = 0.5
; layerThickness = 0.4
; firstLayerThickness = 0.3
; automatic settings before start_gcode
G21 ; set units to millimeters
M107 ; fan off
M140 S70 ; start heating the bed
M104 T0 S200 ; start heating T0
T0 ; set the active extruder to 0
; settings from start_gcode
G28 ; home all axes
G1 Z5 F5000
; automatic settings after start_gcode
M190 S70 ; wait for bed temperature to be reached
M109 T0 S200 ; Finish heating T0
T0 ; set the active extruder to 0
G90 ; use absolute coordinates
G92 E0 ; reset the expected extruder position
M82 ; use absolute distance for extrusion
; Layer count: 2
; Layer Change GCode
; LAYER:0
; LAYER_HEIGHT:0.3
; TYPE:FILL
M400
M107
G1 X113.25 Y105.25 Z0.3 F7800
; TYPE:SKIRT
G1 F1800
G1 X82.75 E0.647 F1080
G1 Y74.75 E1.294
G1 X113.25 E1.942
G1 Y105.25 E2.589
G1 X107.75 Y99.75 F7800
; TYPE:WALL-OUTER
G1 X88.25 E3.003 F1080
G1 Y80.25 E3.417
G1 X107.75 E3.83
G1 Y99.7 E4.243
G1 Y99.75
G1 X104.75
G1 X107.25 Y99.25 F7800
; TYPE:WALL-INNER
G1 X88.75 E4.636 F1080
G1 Y80.75 E5.028
G1 X107.25 E5.421
G1 Y99.2 E5.812
G1 Y99.25
G1 X106.75 Y98.75 F7800
G1 X89.25 E6.184 F1080
G1 Y81.25 E6.555
G1 X106.75 E6.926
G1 Y98.7 E7.297
G1 Y98.75
G1 X106.31 Y98.04 F7800
; TYPE:FILL
G1 X106.04 Y98.31 E7.305 F1080
G1 X105.34 F7800
G1 X106.31 Y97.34 E7.334 F1080
G1 Y96.63 F7800
G1 X104.63 Y98.31 E7.384 F1080
G1 X103.92 F7800
G1 X106.31 Y95.92 E7.456 F1080
G1 Y95.22 F7800
G1 X103.21 Y98.31 E7.549 F1080
G1 X102.51 F7800
G1 X106.31 Y94.51 E7.663 F1080
G1 Y93.8 F7800
G1 X101.8 Y98.31 E7.798 F1080
G1 X101.09 F7800
G1 X106.31 Y93.09 E7.955 F1080
G1 Y92.39 F7800
G1 X100.39 Y98.31 E8.133 F1080
G1 X99.68 F7800
G1 X106.31 Y91.68 E8.332 F1080
G1 Y90.97 F7800
G1 X98.97 Y98.31 E8.552 F1080
G1 X98.27 F7800
G1 X106.31 Y90.27 E8.793 F1080
G1 Y89.56 F7800
G1 X97.56 Y98.31 E9.056 F1080
G1 X96.85 F7800
G1 X106.31 Y88.85 E9.34 F1080
G1 Y88.15 F7800
G1 X96.14 Y98.31 E9.645 F1080
G1 X95.44 F7800
G1 X106.31 Y87.44 E9.971 F1080
G1 Y86.73 F7800
G1 X94.73 Y98.31 E10.318 F1080
G1 X94.02 F7800
G1 X106.31 Y86.02 E10.687 F1080
G1 Y85.32 F7800
G1 X93.32 Y98.31 E11.077 F1080
G1 X92.61 F7800
G1 X106.31 Y84.61 E11.488 F1080
G1 Y83.9 F7800
G1 X91.9 Y98.31 E11.921 F1080
G1 X91.19 F7800
G1 X106.31 Y83.2 E12.374 F1080
G1 Y82.49 F7800
G1 X90.49 Y98.31 E12.849 F1080
G1 X89.78 F7800
G1 X106.31 Y81.78 E13.345 F1080
G1 X105.69 Y81.69 F7800
G1 X89.69 Y97.69 E13.825 F1080
G1 Y96.99 F7800
G1 X104.99 Y81.69 E14.284 F1080
G1 X104.28 F7800
G1 X89.69 Y96.28 E14.722 F1080
G1 Y95.57 F7800
G1 X103.57 Y81.69 E15.139 F1080
G1 X102.86 F7800
G1 X89.69 Y94.86 E15.534 F1080
G1 Y94.16 F7800
G1 X102.16 Y81.69 E15.908 F1080
G1 X101.45 F7800
G1 X89.69 Y93.45 E16.261 F1080
G1 Y92.74 F7800
G1 X100.74 Y81.69 E16.593 F1080
G1 X100.04 F7800
G1 X89.69 Y92.04 E16.903 F1080
G1 Y91.33 F7800
G1 X99.33 Y81.69 E17.193 F1080
G1 X98.62 F7800
G1 X89.69 Y90.62 E17.461 F1080
G1 Y89.92 F7800
G1 X97.92 Y81.69 E17.707 F1080
G1 X97.21 F7800
G1 X89.69 Y89.21 E17.933 F1080
G1 Y88.5 F7800
G1 X96.5 Y81.69 E18.138 F1080
G1 X95.79 F7800
G1 X89.69 Y87.79 E18.321 F1080
G1 Y87.09 F7800
G1 X95.09 Y81.69 E18.483 F1080
G1 X94.38 F7800
G1 X89.69 Y86.38 E18.624 F1080
G1 Y85.67 F7800
G1 X93.67 Y81.69 E18.743 F1080
G1 X92.97 F7800
G1 X89.69 Y84.97 E18.841 F1080
G1 Y84.26 F7800
G1 X92.26 Y81.69 E18.919 F1080
G1 X91.55 F7800
G1 X89.69 Y83.55 E18.974 F1080
G1 Y82.85 F7800
G1 X90.84 Y81.69 E19.009 F1080
G1 X90.14 F7800
G1 X89.69 Y82.14 E19.023 F1080
; Layer Change GCode
; LAYER:1
; LAYER_HEIGHT:0.4
; TYPE:FILL
M400
M106 S255
G1 X89.25 Y81.25 Z0.7 F7800
; TYPE:WALL-INNER
G1 X93.63 E19.147 F1620
G1 X98 E19.271
G1 X102.38 E19.394
G1 X106.75 E19.518
G1 Y85.63 E19.642
G1 Y90 E19.766
G1 Y94.38 E19.889
G1 Y98.75 E20.013
G1 X102.38 E20.137
G1 X98 E20.261
G1 X93.63 E20.384
G1 X89.25 E20.508
G1 Y94.39 E20.632
G1 Y90.03 E20.755
G1 Y85.66 E20.879
G1 Y81.3 E21.002
G1 Y81.25
G1 X88.75 Y80.75 F7800
G1 X93.38 E21.133 F1620
G1 X98 E21.264
G1 X102.63 E21.394
G1 X107.25 E21.525
G1 Y85.38 E21.656
G1 Y90 E21.787
G1 Y94.63 E21.918
G1 Y99.25 E22.049
G1 X102.63 E22.18
G1 X98 E22.311
G1 X93.38 E22.441
G1 X88.75 E22.572
G1 Y94.64 E22.703
G1 Y90.03 E22.833
G1 Y85.41 E22.964
G1 Y80.8 E23.094
G1 Y80.75
G1 X88.25 Y80.25 F7800
; TYPE:WALL-OUTER
G1 X93.13 E23.232 F1134
G1 X98 E23.37
G1 X102.88 E23.508
G1 X107.75 E23.646
G1 Y85.13 E23.784
G1 Y90 E23.922
G1 Y94.88 E24.06
G1 Y99.75 E24.198
G1 X102.88 E24.336
G1 X98 E24.474
G1 X93.13 E24.611
G1 X88.25 E24.749
G1 Y94.89 E24.887
G1 Y90.03 E25.025
G1 Y85.16 E25.162
G1 Y80.3 E25.3
G1 Y80.25
G1 X91.25
G1 X89.25 Y81.25 F7800
G1 X89.69 Y81.91
; TYPE:TOP-FILL
G1 X92.97 Y85.19 E25.431 F2700
G1 X96.25 Y88.47 E25.562
G1 X99.53 Y91.75 E25.694
G1 X102.81 Y95.03 E25.825
G1 X106.09 Y98.31 E25.956
G1 X106.31 Y97.82 F7800
G1 X103.08 Y94.59 E26.085 F2700
G1 X99.86 Y91.37 E26.214
G1 X96.63 Y88.14 E26.344
G1 X93.41 Y84.92 E26.473
G1 X90.18 Y81.69 E26.602
G1 X90.88 F7800
G1 X93.97 Y84.78 E26.725 F2700
G1 X97.05 Y87.86 E26.849
G1 X100.14 Y90.95 E26.972
G1 X103.22 Y94.03 E27.096
G1 X106.31 Y97.12 E27.219
G1 Y96.41 F7800
G1 X103.37 Y93.47 E27.337 F2700
G1 X100.42 Y90.52 E27.455
G1 X97.48 Y87.58 E27.572
G1 X94.53 Y84.63 E27.69
G1 X91.59 Y81.69 E27.808
G1 X92.3 F7800
G1 X95.8 Y85.19 E27.948 F2700
G1 X99.31 Y88.7 E28.089
G1 X102.81 Y92.2 E28.229
G1 X106.31 Y95.7 E28.369
G1 Y95 F7800
G1 X102.98 Y91.67 E28.502 F2700
G1 X99.66 Y88.35 E28.635
G1 X96.33 Y85.02 E28.768
G1 X93 Y81.69 E28.901
G1 X93.71 F7800
G1 X96.86 Y84.84 E29.027 F2700
G1 X100.01 Y87.99 E29.153
G1 X103.16 Y91.14 E29.279
G1 X106.31 Y94.29 E29.405
G1 Y93.58 F7800
G1 X103.34 Y90.61 E29.524 F2700
G1 X100.37 Y87.64 E29.643
G1 X97.39 Y84.66 E29.762
G1 X94.42 Y81.69 E29.881
G1 X95.12 F7800
G1 X97.92 Y84.49 E29.993 F2700
G1 X100.72 Y87.28 E30.105
G1 X103.51 Y90.08 E30.217
G1 X106.31 Y92.87 E30.329
G1 Y92.17 F7800
G1 X102.82 Y88.68 E30.469 F2700
G1 X99.32 Y85.18 E30.608
G1 X95.83 Y81.69 E30.748
G1 X96.54 F7800
G1 X99.8 Y84.95 E30.878 F2700
G1 X103.05 Y88.2 E31.009
G1 X106.31 Y91.46 E31.139
G1 Y90.75 F7800
G1 X103.29 Y87.73 E31.26 F2700
G1 X100.27 Y84.71 E31.38
G1 X97.25 Y81.69 E31.501
G1 X97.95 F7800
G1 X100.74 Y84.48 E31.613 F2700
G1 X103.52 Y87.26 E31.724
G1 X106.31 Y90.05 E31.836
G1 Y89.34 F7800
G1 X103.76 Y86.79 E31.938 F2700
G1 X101.21 Y84.24 E32.04
G1 X98.66 Y81.69 E32.142
G1 X99.37 F7800
G1 X102.84 Y85.16 E32.281 F2700
G1 X106.31 Y88.63 E32.42
G1 Y87.92 F7800
G1 X103.2 Y84.81 E32.545 F2700
G1 X100.08 Y81.69 E32.669
G1 X100.78 F7800
G1 X103.55 Y84.46 E32.78 F2700
G1 X106.31 Y87.22 E32.89
G1 Y86.51 F7800
G1 X103.9 Y84.1 E32.987 F2700
G1 X101.49 Y81.69 E33.083
G1 X102.2 F7800
G1 X104.26 Y83.75 E33.166 F2700
G1 X106.31 Y85.8 E33.248
G1 Y85.1 F7800
G1 X102.9 Y81.69 E33.384 F2700
G1 X103.61 F7800
G1 X106.31 Y84.39 E33.492 F2700
G1 Y83.68 F7800
G1 X104.32 Y81.69 E33.572 F2700
G1 X105.03 F7800
G1 X106.31 Y82.97 E33.623 F2700
G1 Y82.27 F7800
G1 X105.73 Y81.69 E33.646 F2700
G1 X97.71 Y82.16 F7800
G1 X89.69 Y82.62
G1 X92.83 Y85.76 E33.772 F2700
G1 X95.97 Y88.9 E33.897
G1 X99.1 Y92.03 E34.023
G1 X102.24 Y95.17 E34.148
G1 X105.38 Y98.31 E34.274
G1 X104.67 F7800
G1 X101.67 Y95.31 E34.394 F2700
G1 X98.68 Y92.31 E34.514
G1 X95.68 Y89.32 E34.634
G1 X92.69 Y86.32 E34.754
G1 X89.69 Y83.32 E34.874
G1 Y84.03 F7800
G1 X92.55 Y86.89 E34.988 F2700
G1 X95.4 Y89.74 E35.102
G1 X98.26 Y92.6 E35.217
G1 X101.11 Y95.45 E35.331
G1 X103.97 Y98.31 E35.445
G1 X103.26 F7800
G1 X99.87 Y94.92 E35.581 F2700
G1 X96.48 Y91.53 E35.717
G1 X93.08 Y88.13 E35.852
G1 X89.69 Y84.74 E35.988
G1 Y85.45 F7800
G1 X92.91 Y88.67 E36.117 F2700
G1 X96.12 Y91.88 E36.246
G1 X99.34 Y95.1 E36.374
G1 X102.55 Y98.31 E36.503
G1 X101.85 F7800
G1 X98.81 Y95.27 E36.625 F2700
G1 X95.77 Y92.23 E36.746
G1 X92.73 Y89.19 E36.868
G1 X89.69 Y86.15 E36.989
G1 Y86.86 F7800
G1 X92.55 Y89.72 E37.104 F2700
G1 X95.42 Y92.59 E37.218
G1 X98.28 Y95.45 E37.333
G1 X101.14 Y98.31 E37.447
G1 X100.43 F7800
G1 X97.75 Y95.63 E37.555 F2700
G1 X95.06 Y92.94 E37.662
G1 X92.38 Y90.26 E37.77
G1 X89.69 Y87.57 E37.877
G1 Y88.28 F7800
G1 X93.03 Y91.62 E38.011 F2700
G1 X96.38 Y94.97 E38.145
G1 X99.72 Y98.31 E38.279
G1 X99.02 F7800
G1 X95.91 Y95.2 E38.403 F2700
G1 X92.8 Y92.09 E38.528
G1 X89.69 Y88.98 E38.652
G1 Y89.69 F7800
G1 X92.56 Y92.56 E38.767 F2700
G1 X95.44 Y95.44 E38.882
G1 X98.31 Y98.31 E38.997
G1 X97.6 F7800
G1 X94.96 Y95.67 E39.103 F2700
G1 X92.33 Y93.04 E39.208
G1 X89.69 Y90.4 E39.314
G1 Y91.1 F7800
G1 X92.09 Y93.5 E39.41 F2700
G1 X94.5 Y95.91 E39.506
G1 X96.9 Y98.31 E39.602
G1 X96.19 F7800
G1 X92.94 Y95.06 E39.732 F2700
G1 X89.69 Y91.81 E39.862
G1 Y92.52 F7800
G1 X92.59 Y95.42 E39.978 F2700
G1 X95.48 Y98.31 E40.094
G1 X94.77 F7800
G1 X92.23 Y95.77 E40.196 F2700
G1 X89.69 Y93.22 E40.297
G1 Y93.93 F7800
G1 X91.88 Y96.12 E40.385 F2700
G1 X94.07 Y98.31 E40.472
G1 X93.36 F7800
G1 X91.53 Y96.48 E40.546 F2700
G1 X89.69 Y94.64 E40.619
G1 Y95.35 F7800
G1 X92.65 Y98.31 E40.738 F2700
G1 X91.95 F7800
G1 X89.69 Y96.05 E40.828 F2700
G1 Y96.76 F7800
G1 X91.24 Y98.31 E40.89 F2700
G1 X90.53 F7800
G1 X89.69 Y97.47 E40.924 F2700
G1 Y98.18 F7800
G1 X89.82 Y98.31 E40.929 F2700
M400
M107
; MatterSlice Completed Successfully
M104 S0 ; turn off temperature
G28 X0  ; home X axis
M84     ; disable motors
; filament used = 40.9
; filament used extruder 1 (mm) = 40.9
; filament used extruder 2 (mm) = 0.0
; total print time (s) = 77
; MatterControl Version 2.20.6.10507 Build 2.20.6.10507 : GCode settings used
; Date 07/16/2020 00:00:00 Time 9:53
; numberOfBottomLayers = 3
; numberOfPerimeters = 3
; raftExtraDistanceAroundPart = 5
; supportInterfaceLayers = 2
; numberOfTopLayers = 3
; outsidePerimeterExtrusionWidth = 0.5
; outsidePerimeterSpeed = 21
; firstLayerSpeed = 18
; numberOfFirstLayers = 1
; raftPrintSpeed = 60
; topInfillSpeed = 50
; firstLayerExtrusionWidth = 0.5
; firstLayerThickness = 0.3
; endCode = M104 S0 ; turn off temperature\nG28 X0  ; home X axis\nM84     ; disable motors
; minimumTravelToCauseRetraction = 20
; retractionOnTravel = 1
; retractionZHop = 0
; unretractExtraExtrusion = 0
; retractRestartExtraTimeToApply = 0
; retractionSpeed = 30
; bridgeSpeed = 20
; airGapSpeed = 15
; bottomInfillSpeed = 60
; bridgeOverInfill = False
; extrusionMultiplier = 1
; infillStartingAngle = 45
; infillExtendIntoPerimeter = 0.06
; infillSpeed = 60
; infillType = TRIANGLES
; minimumExtrusionBeforeRetraction = .1
; minimumPrintingSpeed = 10
; insidePerimetersSpeed = 30
; raftAirGap = .2
; maxAcceleration = 1000
; maxVelocity = 500
; jerkVelocity = 8
; avoidCrossingMaxRatio = 2
; printTimeEstimateMultiplier = 1
; fanSpeedMinPercent = 35
; coastAtEndDistance = 3
; minFanSpeedLayerTime = 60
; fanSpeedMaxPercent = 100
; maxFanSpeedLayerTime = 30
; bridgeFanSpeedPercent = 100
; firstLayerToAllowFan = 1
; retractionOnExtruderSwitch = 10
; unretractExtraOnExtruderSwitch = 0
; resetLongExtrusion = True
; minimumLayerTimeSeconds = 30
; supportAirGap = .3
; supportInfillStartingAngle = 45
; supportLineSpacing = 2.5
; supportMaterialSpeed = 60
; interfaceLayerSpeed = 60
; supportXYDistanceFromObject = 0.7
; supportType = LINES
; travelSpeed = 130
; wipeShieldDistanceFromObject = 0
; wipeTowerSize = 0
; filamentDiameter = 3
; layerThickness = 0.4
; extrusionWidth = 0.5
; extruderCount = 4
; avoidCrossingPerimeters = True
; enableRaft = False
; outsidePerimetersFirst = False
; outputOnlyFirstLayer = False
; retractWhenChangingIslands = True
; generateSupportPerimeter = True
; generateSupport = False
; generateInternalSupport = True
; supportGrabDistance = 1
; supportPercent = 50
; expandThinWalls = True
; MergeOverlappingLines = True
; fillThinGaps = True
; continuousSpiralOuterPerimeter = False
; startCode = ; automatic settings before start_gcode\nG21 ; set units to millimeters\nM107 ; fan off\nM140 S70 ; start heating the bed\nM104 T0 S200 ; start heating T0\nT0 ; set the active extruder to 0\n; settings from start_gcode\nG28 ; home all axes\nG1 Z5 F5000 ; lift nozzle\n; automatic settings after start_gcode\nM190 S70 ; wait for bed temperature to be reached\nM109 T0 S200 ; Finish heating T0\nT0 ; set the active extruder to 0\nG90 ; use absolute coordinates\nG92 E0 ; reset the expected extruder position\nM82 ; use absolute distance for extrusion
; layerChangeCode = ; LAYER:[layer_num]
; infillPercent = 40
; perimeterStartEndOverlapRatio = 0.9
; raftExtruder = -1
; supportExtruder = 0
; supportInterfaceExtruder = 0
; numberOfSkirtLoops = 1
; skirtDistanceFromObject = 6
; skirtMinLength = 0
; numberOfBrimLoops = 0


"""
#print(fullcode)
matcher = r"Layer count: ([\d]*)"
layer_count = re.findall(matcher, fullcode)
layer_count = int(layer_count[0])
layer_count = layer_count - 1
layer_count = str(layer_count)
layer_finder = "; LAYER:"+layer_count
top_code="\n"
mid_code="\n"
low_code="\n"
finder_flag=0
for lines in fullcode.splitlines():
    if lines != layer_finder and finder_flag == 0:
        top_code = top_code+lines+"\n"
    if lines == layer_finder:
        finder_flag = 1
    if lines == "M107" and finder_flag == 1:
        finder_flag = 2
    if finder_flag == 1:
        mid_code = mid_code+lines+"\n"
    
    if finder_flag == 2:
        low_code = low_code+lines+"\n"

values_X = []
values_Y = []
for lines in mid_code.splitlines():
    if lines == "; MatterSlice Completed Successfully":
        break;

    if (lines != "" and lines[0] == "G"):
        X_reg = r"X([\d]*\.?[\d]*)"
        X_check = re.findall(X_reg, lines)
        Y_reg = r"Y([\d]*\.?[\d]*)"
        Y_check = re.findall(Y_reg, lines)
        
        if (len(X_check) == 0):
            values_X.append(values_X[-1])
        else:
            values_X.append(float(X_check[0]))
        
        if (len(Y_check) == 0):
            values_Y.append(values_Y[-1])
        else:
            values_Y.append(float(Y_check[0]))
            
print(len(values_Y))

"""
regex_Y = r"Y([\d]*\.?[\d]*)"
matches_Y = re.findall(regex_Y, low_code)
values_Y = []
for match in matches_Y:
    values_Y.append(match)

regex_X = r"X([\d]*\.?[\d]*)"
matches_X = re.findall(regex_Y, low_code)
values_X = []
for match in matches_X:
    values_X.append(match)

regex_Z = r"Z([\d]+\.?[\d]+)"
matches_Z = re.findall(regex_Z, low_code)
values_Z = []
for match in matches_Z:
    values_Z.append(match)
"""
print(top_code)
print("-----------------------------------------")
print(mid_code)
print("------------------------------------------")
print(low_code)
print(layer_finder)
"""
print(values_X)
"""