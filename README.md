# hexomata and hexomata2
a hexagonal cellular automata in pygame.

Windows executable for old build of hexomata here https://drive.google.com/file/d/1MuouB4mwtbghTjz9N4Oa-fTxMP91IYJJ/view

Hexomata2 is an 18 neighbor system with the ability to switch back to 6 neighbor.

Control survival/birth ruleset, FPS and cell size. Space to reset with random field. Render to images option (goes in render/ folder). Draw your own pattern with Blank and then unPause to watch it grow.

![Hexomata](https://user-images.githubusercontent.com/25610408/227816442-b622f0ee-8f6e-408e-92e0-7c888633ee61.png)

sounds are determined by the color of the cell according to this chart i found on the internet. Volume of each note is determined by cell count. Sound can be turned off.

If you are rendering frames to the render folder then use the following command to assemble into a video:

ffmpeg -r 5 -f image2 -s 1920x1080 -i hexomata%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p hexomata.mp4
