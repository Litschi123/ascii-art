# IMG2ASCII
Convert images to ascii (images) from the commandline

## How it works
For every pixel of the image the greyscale value will be map to a corresponding character of a predefined set of characters which can be specified as an argument. Every aspect of the scan, the mapping and the final character placement can be specified in the CLI.

### Example
![bob_ross](https://user-images.githubusercontent.com/8984656/142440238-cdba5bae-1834-415d-91b0-558c1b05b19c.jpg)

## Capabilities / ToDo
- [x] Output ascii characters to text file _(togglable)_
- [x] Create new image which shows the source image pixels in ascii characters
- [x] Output image can be immediatly shown upon completion when specified
- [x] Make the ascii characters represent the actual pixel color _(togglable)_
- [x] Change ascii character set _(haven't really decided on a default set)_
- [x] Variable background color _(defaults to (20,20,20))_
- [x] Variable character dimensions on the final image _(default: 7,9)_
- [x] Set vertical/horizontal step size for pixel scan to skip some pixels, since the character are larger than one pixel the output image will be equally larger
