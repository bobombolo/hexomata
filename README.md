# hexomata and hexomata2
a hexagonal cellular automata in pygame.

Hexomata2 is an 18 neighbor system with the ability to switch back to 6 neighbor.

Hexomata2 actually renders a 1920x1080 canvas that the application only sees a window of. Scroll around with the arrow keys.

Hexomata3 is hexomata2 with a 3-state "brian's brain" system.

Hexomata4 is a hexagonal shaped field that plays music samples.

![Screenshot 2023-03-30 18 18 43](https://user-images.githubusercontent.com/25610408/228976394-f21856ba-17c5-414c-86b1-90b7eeaca5f5.png)

Control survival/birth ruleset, FPS and cell size. Draw your own pattern with Blank and then unPause to watch it grow. Try a random field. Change the colors to anything you like.

If you are rendering frames to the render folder then use the following command to assemble into a video:

ffmpeg -r 5 -f image2 -s 1920x1080 -i hexomata%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p hexomata.mp4
