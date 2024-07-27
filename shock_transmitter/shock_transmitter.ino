#include <collar.h>

/*
 * Shock collar transmit example from serial input
 *
 * Before it can be used, either the original transmitters ID
 * needs to be found (e.g. using the Rx example) and entered into
 * "transmitter_id" below, or a value made up and the collar(s)
 * paired using the usual process:
 *   - press and hold the power button untill it beeps
 *   - send any command (e.g. 1V01)
 *   - if it works, the collar should give a long beep, and
 *     other commands will now work
 */


// Set this to whichever pin has the 433MHz transmitter connected to it
const uint8_t  tx_pin = 2;

// Either set this to the id of the original transmitter,
// or make a value up and re-pair
const uint16_t transmitter_id = 0x75DC;

CollarTx *_tx;

bool active = false;
collar_channel channel;
collar_mode mode;
uint8_t power;
uint8_t activeTime;
unsigned long startTime;

void setup()
{
  Serial.begin(115200);
  // Serial.println(transmitter_id, HEX);
  
  // Change "CollarTxType1" to "CollarTxType2" below if nessesary
  _tx =  new CollarTxType1(tx_pin, transmitter_id);
}

void loop()
{
  static char serial_buffer[12];
  static uint8_t serial_pos=0;

  while (Serial.available()) {
    delay(3);  //delay to allow buffer to fill 
    if (Serial.available() >0) {
      char c = Serial.read();  //gets one byte from serial buffer
      serial_buffer[serial_pos++] = c; //makes the string readString
    } 
  }
  serial_buffer[serial_pos] = '\0';
  
  if(serial_pos > 0){
    process_message(serial_buffer);
  }
  // Reset buffer
  memset(serial_buffer, 0, sizeof(serial_buffer));
  serial_pos = 0;

  // Used for stop feature, as well as blocking.
  if(active){
    if(startTime + activeTime * 100> millis()){
      _tx->transmit(channel, mode, power);
    } else {
      active = false;
    }
  }
}

void process_message(const char *input_message)
{
  if (strlen(input_message) != 4)
  {
    Serial.write(1);
    return;
  }

  if(input_message[0] == 'e' || input_message[0] == 'E'){
    active = false;
    activeTime = 0;
    return;
  }

  if(active){
    Serial.write(2);
    return;
  }

  power = (int)input_message[2];
  if(power >= 100){
    Serial.write(5);
    return;
  }
  // This is multiplied by 100 when used, as it is in tenths of a second
  activeTime = round(((int) input_message[3]) * 30 / 25.6);

  // Channel
  switch (input_message[1])
  {
    case 1:
      channel = CH1;
      break;

    case 2:
      channel = CH2;
      break;

    case 3:
      channel = CH3;
      break;

    default:
      Serial.write(4);
      return;
  }

  // Mode
  switch (input_message[0])
  {
    case 'B':
    case 'b':
      mode = BEEP;
      break;

    case 'S':
    case 's':
      mode = SHOCK;
      break;

    case 'V':
    case 'v':
      mode = VIBE;
      break;

    case 'P':
    case 'p':
    // This is done after setting time originally, as the pairing overrides it to be a two second beep.
      mode = BEEP;
      activeTime = 20;
      break;

    default:
      Serial.write(3);
      return;
  }

  active = true;
  startTime = millis();
  Serial.write((byte) 0x00);
}