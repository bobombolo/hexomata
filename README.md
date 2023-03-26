# hexomata
a hexagonal cellular automata in pygame.

Windows executable here https://drive.google.com/file/d/1MuouB4mwtbghTjz9N4Oa-fTxMP91IYJJ/view

Control survival/birth ruleset, FPS and cell size. Space to reset with random field. Render to images option (goes in render/ folder). Draw your own pattern with Blank and then unPause to watch it grow.

![Screenshot 2023-03-19 07 04 05](https://user-images.githubusercontent.com/25610408/226171213-1efb7235-3131-4c5b-af61-99e0e90fe917.png)

sounds are determined by the color of the cell according to this chart:

![Screenshot 2023-03-19 00 38 22](https://user-images.githubusercontent.com/25610408/226171019-965e6bed-1014-469a-84f5-82fc04308dbd.png)

Volume of each note is determined by cell count. Sound can be turned off.

If you are rendering frames to the render folder then use the following command to assemble into a video:

ffmpeg -r 5 -f image2 -s 1920x1080 -i hexomata%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p hexomata.mp4
