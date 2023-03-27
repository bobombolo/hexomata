# hexomata and hexomata2
a hexagonal cellular automata in pygame.

Windows executable for old build of hexomata here https://drive.google.com/file/d/1MuouB4mwtbghTjz9N4Oa-fTxMP91IYJJ/view

Hexomata2 is an 18 neighbor system with the ability to switch back to 6 neighbor. Windows executable here https://drive.google.com/file/d/14psNYcqUSVCzmia4938uJi_gPZOa8zIi/view


![Screenshot 2023-03-26 22 41 47](https://user-images.githubusercontent.com/25610408/227827765-d3e715ec-4235-4eef-a6d2-bec1b9fd7bb4.png)

Control survival/birth ruleset, FPS and cell size. Draw your own pattern with Blank and then unPause to watch it grow. Try a random field.

If you are rendering frames to the render folder then use the following command to assemble into a video:

ffmpeg -r 5 -f image2 -s 1920x1080 -i hexomata%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p hexomata.mp4
