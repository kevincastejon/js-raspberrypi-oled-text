const { spawn } = require('child_process');
const events = require('events');

const scrollValues = {
  on: '1',
  off: '0',
  auto: 'A',
};
const python = spawn('python', ['./oled-text.py']);

class Oled extends events {
  constructor() {
    super();
  }

  init(){
    this._firstLine = '';
    this._secondLine = '';
    this._thirdLine = '';
    this._firstLineScroll = 'auto';
    this._secondLineScroll = 'auto';
    this._thirdLineScroll = 'auto';
    this._ready = false;
    this._commandsBuffer = [];
    python.stdout.on('data', (data) => {
      if (data.toString().trim() === 'READY') {
        this._ready = true;
        this.emit('ready');
      }
      if (data.toString().trim() === 'FREE') {
        this._commandsBuffer.shift();
        if (this._commandsBuffer.length > 0) {
          this._sendNextCommand();
        }
      }
    });
    python.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });
    python.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
    });
  }

  get firstLineScroll() {
    return (this._firstLineScroll);
  }

  set firstLineScroll(value) {
    this._firstLineScroll = value;
    this._addCommand(1, this._firstLine, scrollValues[this._firstLineScroll]);
  }

  get secondLineScroll() {
    return (this._secondLineScroll);
  }

  set secondLineScroll(value) {
    this._secondLineScroll = value;
    this._addCommand(2, this._secondLine, scrollValues[this._secondLineScroll]);
  }

  get thirdLineScroll() {
    return (this._thirdLineScroll);
  }

  set thirdLineScroll(value) {
    this._thirdLineScroll = value;
    this._addCommand(3, this._thirdLine, scrollValues[this._thirdLineScroll]);
  }

  get firstLine() {
    return (this._firstLine);
  }

  set firstLine(value) {
    this._firstLine = value;
    this._addCommand(1, value, scrollValues[this._firstLineScroll]);
  }

  get secondLine() {
    return (this._secondLine);
  }

  set secondLine(value) {
    this._secondLine = value;
    this._addCommand(2, value, scrollValues[this._secondLineScroll]);
  }

  get thirdLine() {
    return (this._thirdLine);
  }

  set thirdLine(value) {
    this._thirdLine = value;
    this._addCommand(3, value, scrollValues[this._thirdLineScroll]);
  }

  get ready() {
    return (this._ready);
  }

  _addCommand(line, text, scroll) {
    this._commandsBuffer.push({ line, text, scroll });
    if (this._commandsBuffer.length === 1) {
      this._sendNextCommand();
    }
  }

  _sendNextCommand() {
    const cmd = this._commandsBuffer[0];
    python.stdin.write(`${cmd.line + cmd.scroll + cmd.text}\n`);
  }
}
module.exports = Oled;
