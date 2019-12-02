# raspberrypi-oled-text

Use three lines of scrollable text on OLED lcd from a Raspberry Pi

### Installation
```
npm i raspberrypi-oled-text
```

### Basic Usage
```
const Oled = require('raspberrypi-oled-text');

const oled = new Oled();
oled.on('ready', () => {
  oled.firstLineScroll = 'on';
  oled.firstLine = 'Line 1 scroll';
  oled.secondLineScroll = 'off';
  oled.secondLine = 'Line 2 no scroll';
  oled.thirdLineScroll = 'auto';
  oled.thirdLine = 'Line 3 autoscroll';
});
oled.init();
```

### Scroll modes
Valid scroll mode values:
  - 'on' - The line will scroll
  - 'off' - The line will not scroll
  - 'auto' - The line will scroll only if the characters don't fit onto the screen width

### Optimization

When setting consecutively the scroll mode and the text content of a line you should use the method instead of the setter
```
oled.firstLineScroll = 'on';          //  Uses two process commands internally
oled.firstLine = 'Not optimized';     //  (not optimized)

oled.setFirstLine('Optimized', 'on'); // Uses only one process command internally (optimized)
```

### API
- Methods
  - init() - Starts the Oled lcd
  - setFirstLine(text, scroll) - Sets the first line scroll mode and text.
    - text - String - REQUIRED - The text content of the first line.
    - scroll - String - REQUIRED - The scroll mode of the first line.
  - setSecondLine(text, scroll) - Sets the second line scroll mode and text.
    - text - String - REQUIRED - The text content of the second line.
    - scroll - String - REQUIRED - The scroll mode of the second line.
  - setThirdLine(text, scroll) - Sets the third line scroll mode and text.
    - text - String - REQUIRED - The text content of the third line.
    - scroll - String - REQUIRED - The scroll mode of the third line.
- Members
  - ready - Boolean - READ-ONLY - True if the Oled screen is ready to be controlled
  - firstLine - String - The text content of the first line. Default empty string
  - secondLine - String - The text content of the second line. Default empty string
  - thirdLine - String - The text content of the third line. Default empty string
  - firstLineScroll - String - The scroll mode of the first line. Default 'auto'
  - secondLineScroll - String - The scroll mode of the second line. Default 'auto'
  - thirdLineScroll - String - The scroll mode of the third line. Default 'auto'
- Events
  - 'ready' - Fires when the Oled screen is ready to be controlled
