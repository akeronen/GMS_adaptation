fileNormalTiles = open("output_normal_tiles.txt","w")
fileMirroredTiles = open("output_mirrored_tiles.txt","w")
fileRotatedTiles = open("output_rotated_tiles.txt","w")
fileRotateAndMirroredTiles = open("output_rotate_and_mirrored_tiles.txt","w")

TileMirror_Mask = (1 << 28)
TileIndex_ShiftedMask = 0x7ffff
TileRotate_Mask = (1 << 30)

tiles_mirror = 0
tiles_normal = 0
tiles_rotate = 0
tiles_rotate_mirrored = 0

# input is from GMS (extracted) .yy-file contents from:
#            "tiles": {
#                "TileSerialiseData":
with open("input.txt") as f:
    lines = f.readlines()
    for line in lines:
        list = line.split(",")
        for value in list:
            lastvalueInList = list[-1]
            if value != '\n':
                intValue = int(value)
                if intValue > 0:
                    intValue = intValue + 1
                # write outputs
                if (intValue & TileRotate_Mask and intValue & TileMirror_Mask):
                    intValue = intValue & TileIndex_ShiftedMask
                    fileNormalTiles.write(str(0))
                    fileMirroredTiles.write(str(0))
                    fileRotatedTiles.write(str(0))
                    fileRotateAndMirroredTiles.write(str(intValue + 2))
                    tiles_rotate_mirrored = tiles_rotate_mirrored + 1
                elif (intValue & TileRotate_Mask):
                    intValue = intValue & TileIndex_ShiftedMask
                    fileNormalTiles.write(str(0))
                    fileMirroredTiles.write(str(0))
                    fileRotatedTiles.write(str(intValue + 2))
                    fileRotateAndMirroredTiles.write(str(0))
                    tiles_rotate = tiles_rotate + 1
                elif (intValue & TileMirror_Mask):
                    intValueMirrored = intValue & TileIndex_ShiftedMask
                    fileNormalTiles.write(str(0))
                    fileMirroredTiles.write(str(intValueMirrored + 1))
                    fileRotatedTiles.write(str(0))
                    fileRotateAndMirroredTiles.write(str(0))
                    tiles_mirror = tiles_mirror + 1
                else:
                    # not with any mask so its then a normal tile
                    fileNormalTiles.write(str(intValue))
                    fileMirroredTiles.write(str(0))
                    fileRotatedTiles.write(str(0))
                    fileRotateAndMirroredTiles.write(str(0))
                    tiles_normal = tiles_normal + 1
                # ToDo: this leaves last lines ending with unnecessary commas
                fileNormalTiles.write(",")
                fileMirroredTiles.write(",")
                fileRotatedTiles.write(",")
                fileRotateAndMirroredTiles.write(",")
        fileNormalTiles.write("\n")
        fileMirroredTiles.write("\n")
        fileRotatedTiles.write("\n")
        fileRotateAndMirroredTiles.write("\n")
    fileNormalTiles.write("\n")
    fileMirroredTiles.write("\n")
    fileRotatedTiles.write("\n")
    fileRotateAndMirroredTiles.write("\n")
fileNormalTiles.close()
fileMirroredTiles.close()
fileRotatedTiles.close()
fileRotateAndMirroredTiles.close()

print("normal tiles: " +  str(tiles_normal))
print("mirrored tiles: " +  str(tiles_mirror))
print("rotate tiles: " +  str(tiles_rotate))
print("rotate and mirrored tiles: " +  str(tiles_rotate_mirrored))
