#ifndef SIPMINTERFACE_HH
#define SIPMINTERFACE_HH

#define ACK           6
#define EOT           4

#include <stdio.h>    /* Standard input/output definitions */
#include <stdlib.h> 
#include <stdint.h>   /* Standard types */
#include <string.h>   /* String function definitions */
#include <unistd.h>   /* UNIX standard function definitions */
#include <fcntl.h>    /* File control definitions */
#include <errno.h>    /* Error number definitions */
#include <termios.h>  /* POSIX terminal control definitions */
#include <sys/ioctl.h>

#ifdef __cplusplus
class sipm {
public:
  sipm(char *device);
  ~sipm();
#endif

  int check_value(int value);
  int check_channel(int value);
  int setgain(int channel, unsigned short int value);
  int setthreshold(int channel, unsigned short int value);
  int savetoeeprom();
  int applyvalues();
  int readvalues();

  int maxchannel;
  unsigned short int gain[256];
  unsigned short int threshold[256];

#ifdef __cplusplus
private:
#endif

#ifndef __cplusplus
  int init(char *device);
#endif
  int serial;

#ifdef __cplusplus
};
#endif

int getdevicelist(char ***devicelist, int *devicenum);
#endif
