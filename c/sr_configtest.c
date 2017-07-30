
/*
 This file is part of metpx-sarracenia.
 The sarracenia suite is Free and is proudly provided by the Government of Canada
 Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2017

 author: Peter Silva

status: 
  This is just a beginning stub, not working at all. 

  Purpose is to have something that parses the sarracenia configuration files in C.

 */

#include <stdio.h>
#include "sr_config.h"

#define FNAME   "/home/peter/.config/sarra/post/test2.conf" 

int main( int argc, char *const *argv ) {

  int ret;
  struct sr_config_t sr_cfg;

  printf( "reading: %s\n", argv[1] );

  sr_config_init( &sr_cfg, argv[0] );
  ret = sr_config_read( &sr_cfg, argv[1] );
  if (!ret) {
     fprintf(stderr, "failed to read config %s\n", argv[1] );
     exit(1);
  }
  ret = sr_config_finalize( &sr_cfg, 1);
  if (!ret) {
     fprintf(stderr, "failed to finalize config %s\n", argv[1] );
     exit(1);
  }


  printf( "broker, scheme=%s\n", sr_cfg.broker->ssl?"amqps":"amqp" );
  printf( "broker, userInfo=%s \n", sr_cfg.broker->user );
  printf( "broker, hostText=%s \n", sr_cfg.broker->hostname );
  printf( "broker, portText=%d \n", sr_cfg.broker->port );
  printf( "posting accept_unmatched=%s \n", sr_cfg.accept_unmatched?"on":"off" );
  printf( "posting debug=%s \n", sr_cfg.debug?"on":"off" );
  printf( "posting events= 0x%02x \n", sr_cfg.events);
  printf( "posting exchange=%s \n", sr_cfg.exchange);
  printf( "posting queue_name=%s \n", sr_cfg.queuename);
  printf( "posting url=%s \n", sr_cfg.url);
  printf( "posting sumalgo=%c \n", sr_cfg.sumalgo);

  exit(0);

}