#include "sipminterface.hh"
void initialize_helper(char *device, int *maxchannel, int *serial);

int serialport_init(const char* serialport, int baud)
{
    struct termios toptions;
    int fd;
    speed_t brate;    

    fd = open(serialport, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1)  {
        perror("init_serialport: Unable to open port ");
        return -1;
    }
    
    if (tcgetattr(fd, &toptions) < 0) {
        perror("init_serialport: Couldn't get term attributes");
        return -1;
    }

    brate = baud; /* let you override switch below if needed */
    switch(baud) {
    case 4800:   brate=B4800;   break;
    case 9600:   brate=B9600;   break;
#ifdef B14400
    case 14400:  brate=B14400;  break;
#endif
    case 19200:  brate=B19200;  break;
#ifdef B28800
    case 28800:  brate=B28800;  break;
#endif
    case 38400:  brate=B38400;  break;
    case 57600:  brate=B57600;  break;
    case 115200: brate=B115200; break;
    }
    cfsetispeed(&toptions, brate);
    cfsetospeed(&toptions, brate);

    /* 8N1 */
    toptions.c_cflag &= ~PARENB;
    toptions.c_cflag &= ~CSTOPB;
    toptions.c_cflag &= ~CSIZE;
    toptions.c_cflag |= CS8;
    /* no flow control */
    toptions.c_cflag &= ~CRTSCTS;

    toptions.c_cflag |= CREAD | CLOCAL;  /* turn on READ & ignore ctrl lines */
    toptions.c_iflag &= ~(IXON | IXOFF | IXANY); /* turn off s/w flow ctrl */

    toptions.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); /* make raw */
    toptions.c_oflag &= ~OPOST; /* make raw */

    /* see: http://unixwiz.net/techtips/termios-vmin-vtime.html */
    toptions.c_cc[VMIN]  = 0;
    toptions.c_cc[VTIME] = 20;
    
    if( tcsetattr(fd, TCSANOW, &toptions) < 0) {
        perror("init_serialport: Couldn't set term attributes");
        return -1;
    }

    return fd;
}

int serialport_writebyte( int fd, uint8_t b)
{
    int n = write(fd,&b,1);
    if( n!=1)
        return -1;
    return 0;
}

int serialport_read_until(int fd, char* buf, char until)
{
    char b[1];
    int i=0;
    do { 
      int n = read(fd, b, 1);  /* read a char at a time */
      if( n==-1) return -1;    /* couldn't read */
      if( n==0 ) {
	usleep( 10 * 1000 ); /* wait 10 msec try again */
	continue;
      }
      buf[i] = b[0]; i++;
    } while( b[0] != until );
    
    /*buf[i] = 0;  // null terminate the string */
    return 0;
}

#ifdef __cplusplus

sipm::sipm(char *device){
  initialize_helper(device, &maxchannel, &serial);
}

sipm::~sipm(){
    close(serial);
  }

#endif

#ifndef __cplusplus
int init(char *device){
  initialize_helper(device, &maxchannel, &serial);
   
  if(maxchannel<2) return -2;
  else return 0;
  }
#endif
  
int 
#ifdef __cplusplus
sipm::
#endif
check_value(int value){
    if(value>4095)
      return -1;
    else if(value<0)
      return -2;
    else 
      return 0;      
  }

int 
#ifdef __cplusplus
sipm::
#endif
check_channel(int value){
    if(value>maxchannel)
      return -1;
    else if(value<0)
      return -2;
    else 
      return 0;
  }

int 
#ifdef __cplusplus
sipm::
#endif
setgain(int channel, unsigned short int value){
  unsigned char command[5];
  unsigned char byte;

  command[0] = 'S';
  command[1] = 'G';
  command[2] = (unsigned char)channel; 
  command[3] = (unsigned char)((value & 0xF00) >> 8);
  command[4] = (unsigned char) (value & 0xFF);

  if(check_channel(channel) != 0)
    return -1;
  if(check_value(value) != 0)
    return -2;
  
  write(serial,command,5);
  usleep(10*1000);
  read(serial,&byte,1);
  
  if(byte!=ACK) return -3;
  else return 0;
}

int
#ifdef __cplusplus
sipm::
#endif
setthreshold(int channel, unsigned short int value){
  unsigned char byte;
  unsigned char command[5];

  command[0] = 'S';
  command[1] = 'T';
  command[2] = (unsigned char)channel; 
  command[3] = (unsigned char)((value & 0xF00) >> 8);
  command[4] = (unsigned char) (value & 0xFF);

  if(check_channel(channel) != 0)
    return -1;
  if(check_value(value) != 0)
    return -2;
  
  write(serial,command,5);
  usleep(10*1000);
  read(serial,&byte,1);
  
  if(byte!=ACK) return -3;
  else return 0;
}

int
#ifdef __cplusplus
sipm::
#endif
savetoeeprom(){
    char command[3] = "SV";
    unsigned char byte;
    int counter=0;

    write(serial,command,2);
    //usleep(26*1000);
    sleep(5);
    do {
      read(serial,&byte,1);
      if (counter >10) break;
      else counter++;
    } while(byte!=ACK);
    
    if(byte!=ACK) return -3;
    else return 0;
  }

int
#ifdef __cplusplus
sipm::
#endif
applyvalues(){
    unsigned char command[2] = "A";
    int counter=0;
    unsigned char byte;

    write(serial,command,1);
    usleep(26*1000);

    do {
      read(serial,&byte,1);
      if (counter >10) break;
      else counter++;
    } while(byte!=ACK);

    if(byte!=ACK) return -3;
    else return 0;
  }

int
#ifdef __cplusplus
sipm::
#endif
readvalues(){
    unsigned char gbuffer[512] = {512*0};
    unsigned char tbuffer[512] = {512*0};
    char byte;
    int i=0;
    serialport_writebyte(serial,(uint8_t)'R');
    usleep( 100 * 1000 ); /* we need this time to fill the PCs UART 
			    maybe it's not nessesary with a higher baudrate */

    read(serial, gbuffer, 2*maxchannel);
    read(serial, tbuffer, 2*maxchannel);
    read(serial, &byte, 1);

    for(i=0; i<2*maxchannel; i+=2){
      gain[i/2] = ((unsigned short int)(gbuffer[i]) << 8) +
	((unsigned short int)(gbuffer[i+1]));
      threshold[i/2] = ((unsigned short int)(tbuffer[i]) << 8) +
	((unsigned short int)(tbuffer[i+1]));	
    }   
    
    /*printf("Byte= 0x%x ,Gain:\n", byte);
    for(i=0;i<256; i++) printf("%i ",gain[i]);
    printf("\n");
    printf("Threshold:\n");
    for(i=0;i<256; i++) printf("%i ",threshold[i]);
    printf("\n");
    printf("\n");*/
  
    if(byte!=EOT) return -3;
    else return 0;    
  }

int getdevicelist(char ***devicelist, int* devicenum){
  FILE *fp;
  char b[256];
  char val[256];
  char val2[256];
  char listofusbdevices[256][256];
  int counter = 0;
  int i=0, buffer=0;
  // for linux : 
  system("ls -l /sys/class/tty/*/device/driver > /tmp/usbdevicetmpfile");
  
  fp = fopen("/tmp/usbdevicetmpfile", "r");
  while (!feof(fp)) {
    // for linux : 
    fscanf(fp,"%s %s %s %s %s %s %s %s %s %s %s",b,b,b,b,b,b,b,b,val,b,val2);
    if(strstr(val2,"usb")!=0){
      strcpy(listofusbdevices[counter],val);
      counter++;
      if(counter>255) break;
    }
  }
  fclose(fp);
  system("rm /tmp/usbdevicetmpfile");

#ifdef __cplusplus
  *devicelist = new char*[counter];
#endif
#ifndef __cplusplus
  *devicelist = (char **) malloc(counter);
#endif

  for(i=0; i<counter; i++){
#ifdef __cplusplus
    *devicelist[i] = new char[counter];
#endif
#ifndef __cplusplus
      *devicelist[i] = (char *) malloc(256);
#endif

    do{
      if(*(listofusbdevices[i]+15+buffer) == '/') break;
      else buffer++;
    } while(buffer < 200);
    sprintf(*devicelist[i], "/dev/" );
    strncpy(*devicelist[i]+5,listofusbdevices[i]+15, 7);
  }
  *devicenum = counter;

  return 0;
}

void initialize_helper(char *device, int *maxchannel, int *serial){
  char buffer[256] = {256*0};
  int j=-1, t=0;
  *serial = serialport_init(device, 9600);
  usleep( 10 * 1000 ); /* wait for port to be configured */
    /*if(serial==-1) return -1;*/
    do{
      serialport_writebyte(*serial,(uint8_t)'G');
      usleep( 10 * 1000 );
      j=serialport_read_until(*serial,buffer,ACK);
      /*printf("j=%i ",j);*/
    
      /*for(int i=0; i<256; i++) printf("0x%X ",(uint8_t)buffer[i]);*/
      *maxchannel = (uint8_t)buffer[0] + 1;
      if(t>10) break;
      else t++;
    } while (*maxchannel < 2);
}
