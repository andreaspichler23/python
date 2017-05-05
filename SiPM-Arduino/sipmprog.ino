/*
  - we have 2.5 kB of RAM, 12 bit DACs need to store the values an short int of
    2 bytes, 2 values per channel -> 4 bytes per channel data
  - EEPROM size is 1 kB
  - -> max 1024/4 = 256 channels
 */
#include <EEPROM.h>
#include <SPI.h>

#define MAXCHANNELS 256
#define SIZEEEPROM 1024

#define ACK           6
#define EOT           4

// SPI interface, CS can be any pin
#define MOSI     ICSP-4
#define MISO     ICSP-1
#define SCK      ICSP-3
#define CS            7

// interrupt 0-pin3 1-pin2 2-pin0 3-pin1
// PIN 2 is interrupt
#define INTNUM        1
#define INTPIN        2

#define WAIT __asm__("nop\n\t") // 62.5 ns
volatile bool finalboard = false;

// This allocates 1 kB of RAM
unsigned short int gain[MAXCHANNELS];
unsigned short int threshold[MAXCHANNELS];

int led  = 3;
int freq = 0;
bool high = false;

byte chbuf = -1;
byte channels = 0;

// defining functions
byte getchannel();
byte countchannel();
unsigned short int getvalue();
void writetoeeprom();
void readfromeeprom();
void ISR_final_board();

enum SPI {
  OPTIMIZE,
  WRITE,
  WRITETHROUGH,
  ACTIVATE,
  NOP
};

void send_SPI_command(byte cmd);

/*
  Setup function
 */
void setup() {
  pinMode(CS, OUTPUT);              // chip select as output
  digitalWrite(CS, HIGH);
  pinMode(led, OUTPUT);
  pinMode(INTPIN, INPUT);           // set interrupt pin as input

  SPI.setBitOrder(MSBFIRST);        // most significant bit first
  SPI.begin();                      // start SPI interface

  // attach ISR on falling edge trigger
  attachInterrupt(INTNUM, ISR_final_board, FALLING);

  readfromeeprom();                 // restore gain and treshold from eeprom 
  
  channels = countchannel();        // get channel number
  send_SPI_command(OPTIMIZE);       // optimize linearity
  WAIT; 
  send_SPI_command(WRITETHROUGH);   // write values to DACs
   

  Serial.begin(9600);       // initialize serial connection (USB) with 9,6 kBaud
  //while (!Serial) {;}     // wait for serial interface to become active
  delay(10);
}

/*
  Main loop function
 */
void loop() {
  if (Serial.available() > 0) {    // execute if there is something in the UART
    byte inByte = Serial.read();   // read byte

    switch(inByte) {               // get command
    case 'S':                     
      inByte = Serial.read();
      switch(inByte){              // get second part of the command
	
      case 'G':                    // set the Gain
	chbuf = getchannel();      // get the channelnumber from 1 byte
	if(chbuf != -1){
	  gain[chbuf] = getvalue();// get the 12 bit DAC value
	  Serial.write(ACK);       // send ACK back to computer
	}
	break;

      case 'T':                    // Set Threshold
	chbuf = getchannel();
	if(chbuf != -1){
	  threshold[chbuf] = getvalue();
	  Serial.write(ACK);
	}
	break;

      case 'V':                    // Save data to EEPROM
	writetoeeprom();           // write current values to EEPROM
	delay(10);
	Serial.write(ACK);
	break;
    
      default:
	break;
      }
      break;
      
    case 'A':                      // Apply values to DACs
      high = true;
      send_SPI_command(WRITETHROUGH); 
      //send_SPI_command(WRITE);   // write values to DACs
      //send_SPI_command(ACTIVATE);// activate DAC output   
      Serial.write(ACK);
      break;
      
    case 'G':                      // Return the number of connected channels
      digitalWrite(led, LOW);
      Serial.write(channels);      // Channel number
      Serial.write(ACK);        
      high = false;
      break;

    case 'R':                      // Send the current values 
      for(int i=0; i<channels+1; i++){
	byte high = (gain[i]&0xF00) >> 8;
	byte low = gain[i]&0xFF;
	Serial.write(high);
	Serial.write(low);}
      for(int i=0; i<channels+1; i++){
	byte high = (threshold[i]&0xF00) >> 8;
	byte low = threshold[i]&0xFF;
	Serial.write(high);
	Serial.write(low);}
      Serial.write(EOT);           // End of transmission      
      break;

    case 'T':
      Serial.println("TEST");
      for(int i=0; i<MAXCHANNELS; i++){
      	Serial.print(gain[i],DEC);
      	Serial.print(" ");
      }
    default:
      break;
    }
  }
}

// read the channelnumber from UART
byte getchannel(){
  byte channel = Serial.read();
  return channel;
}

// get a short value from two transmitted bytes
unsigned short int getvalue(){
  // val|val
  byte tmp = Serial.read();
  unsigned short int result = (unsigned short int)tmp<<8;
  //result << 8;
  result += (unsigned short int) Serial.read();
  return result;
}

// writes all gain and threshold values to the eeprom
void writetoeeprom(){
  unsigned short int adr = 0;
  
  // first 256 values are the gain
  for(int i=0; i<MAXCHANNELS; i++){
    byte  low =  gain[i]       & 0xFF;
    byte high = (gain[i] >> 8) & 0xFF;
    EEPROM.write(adr,high);
    delay(4);               // 4 ms write time 
    adr++;
    EEPROM.write(adr,low);
    adr++;
    delay(4);               // 4 ms write time
  }

  // second 256 values are the threshold
  for(int i=0; i<MAXCHANNELS; i++){
    byte  low =  threshold[i]       & 0xFF;
    byte high = (threshold[i] >> 8) & 0xFF;
    EEPROM.write(adr,high);
    adr++;
    delay(4);             // 4 ms write time
    EEPROM.write(adr,low);
    adr++;
    delay(4);             // 4 ms write time
  }
}

// read gain and threshold values from EEROM
void readfromeeprom(){
  unsigned short int adr = 0;
  // reading back gain values
  for(int i=0; i<MAXCHANNELS; i++){
    byte high = EEPROM.read(adr);
    adr++;
    byte  low = EEPROM.read(adr);
    adr++;

    gain[i]  = high << 8;
    gain[i] += low;
    }

  // reading back threshold values
  for(int i=0; i<MAXCHANNELS; i++){
    byte high = EEPROM.read(adr);
    adr++;
    byte  low = EEPROM.read(adr);
    adr++;

    threshold[i]  = high << 8;
    threshold[i] += low;
    }
}

void send_SPI_command(byte cmd){
  byte  low = 0;
  byte high = 0;
  unsigned short int tmpval=0;
  digitalWrite(CS, LOW);    // select DACs
  switch(cmd) {
  case OPTIMIZE:            // Optimize linearity
      for(byte i=0; i<channels/2; i++){
	SPI.transfer(0x05); // optimize
	SPI.transfer(0x02); // Set lin bit
	SPI.transfer(0x00);
      }
      digitalWrite(CS, HIGH);
      
      delay(10);            // 10 ms for linearity optimizations
  
      for(byte i=0; i<channels/2; i++){
	SPI.transfer(0x05); // optimize
	SPI.transfer(0x00); // Erase lin bit
	SPI.transfer(0x00);
      }
    break;

  case WRITE:
    for(byte i=0; i<channels; i+=2){
      SPI.transfer(0x11);           // write dac channel 1
      tmpval = gain[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);           // Set gain
      SPI.transfer(low);            // Set gain
    }
    digitalWrite(CS, HIGH);
    WAIT;

    digitalWrite(CS, LOW);
    for(byte i=1; i<channels; i+=2){
      SPI.transfer(0x12);            // write dac channel 2
      tmpval = gain[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);            // Set gain
      SPI.transfer(low);             // Set gain
    }
    digitalWrite(CS, HIGH);
    WAIT;

    digitalWrite(CS, LOW);
    for(byte i=0; i<channels; i+=2){
      SPI.transfer(0x14);            // write dac channel 3
      tmpval = threshold[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);            // Set threshold
      SPI.transfer(low);             // Set threshold
    }
    digitalWrite(CS, HIGH);
    WAIT;

    digitalWrite(CS, LOW);
    for(byte i=1; i<channels; i+=2){
      SPI.transfer(0x18);            // write dac channel 4
      tmpval = threshold[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);            // Set threshold
      SPI.transfer(low);             // Set threshold
    }
    break;

  case WRITETHROUGH:
  
    for(byte i=0; i<channels; i+=2){
      //if(finalboard)
	//break;
      SPI.transfer(0x31);           // write and activate dac channel 1
      tmpval = gain[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);           // Set gain
      SPI.transfer(low);            // Set gain
    }
    digitalWrite(CS, HIGH);
    WAIT;

    digitalWrite(CS, LOW);
    for(byte i=1; i<channels; i+=2){
      SPI.transfer(0x32);            // write and activate dac channel 2
      tmpval = gain[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);            // Set gain
      SPI.transfer(low);             // Set gain
    }
    digitalWrite(CS, HIGH);
    WAIT;

    digitalWrite(CS, LOW);
    for(byte i=0; i<channels; i+=2){
      SPI.transfer(0x34);            // write and activate dac channel 3
      tmpval = threshold[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);            // Set threshold
      SPI.transfer(low);             // Set threshold
    }
    digitalWrite(CS, HIGH);
    WAIT;

    digitalWrite(CS, LOW);
    for(byte i=1; i<channels; i+=2){
      SPI.transfer(0x38);            // write and activate dac channel 4
      tmpval = threshold[i] << 4;		      
      low =   tmpval       & 0xFF;
      high = (tmpval >> 8) & 0xFF;
      SPI.transfer(high);            // Set threshold
      SPI.transfer(low);             // Set threshold
    }
    break;

  case ACTIVATE:
    for(byte i=0; i<channels/2; i++){
      if(finalboard)
	break;
      SPI.transfer(0x01);            // activate
      SPI.transfer(0x0F);            // all channels
      SPI.transfer(0x00);
    }
    digitalWrite(CS, HIGH);
    break;

  case NOP:
      for(byte i=0; i<channels/2; i++){
	if(finalboard)
	  break;
	SPI.transfer(0x20);          // NOP
	SPI.transfer(0x00); 
	SPI.transfer(0x00);
      }   
    break;
  default:
    break;
  }
  digitalWrite(CS, HIGH);
  finalboard = false;
}

byte countchannel(){
  byte i=0;
  digitalWrite(CS, LOW);
  
  for(i=0; i<MAXCHANNELS/2; i++){
    if(finalboard)
      break;
    SPI.transfer(0x20);       // NOP
    SPI.transfer(0x00); 
    SPI.transfer(0x00);
  }
  digitalWrite(CS, HIGH);
  if(i == MAXCHANNELS/2) i=0; // probably nothing connected
  channels=i*2;
}

void ISR_final_board(){       // Interrupt service routine
  finalboard = true;
}