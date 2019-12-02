const Oled = require('./index');

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
