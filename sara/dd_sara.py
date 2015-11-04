#!/usr/bin/python3
#
# This file is part of sarracenia.
# The sarracenia suite is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2008-2015
#
# Questions or bugs report: dps-client@ec.gc.ca
# sarracenia repository: git://git.code.sf.net/p/metpx/git
# Documentation: http://metpx.sourceforge.net/#SaraDocumentation
#
# dd_sara.py : python3 program allowing users to listen and download product from
#              another sarracenia server or from user posting (dd_post/dd_watch)
#
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  Jun Hu         - Shared Services Canada
#  Last Changed   : Sep 22 10:41:32 EDT 2015
#  Last Revision  : Sep 22 10:41:32 EDT 2015
#
########################################################################
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#
#

import os,sys,time

try :    
         from dd_amqp           import *
         from dd_file           import *
         from dd_ftp            import *
         from dd_http           import *
         from dd_instances      import *
         from dd_message        import *
         from dd_sftp           import *
except : 
         from sara.dd_amqp      import *
         from sara.dd_file      import *
         from sara.dd_ftp       import *
         from sara.dd_http      import *
         from sara.dd_instances import *
         from sara.dd_message   import *
         from sara.dd_sftp      import *

class dd_sara(dd_instances):

    def __init__(self,config=None,args=None):
        dd_instances.__init__(self,config,args)
        self.defaults()
        self.exchange = 'xpublic'
        self.configure()

    def check(self):

        # dont want to recreate these if they exists

        if not hasattr(self,'msg') :
           self.msg      = dd_message(self.logger)

        self.msg.user = self.source_broker.username

        # umask change for directory creation and chmod

        try    : os.umask(0)
        except : pass

    def close(self):
        self.hc_src.close()
        self.hc_pst.close()

    def connect(self):

        # =============
        # consumer
        # =============

        # consumer host

        self.hc_src = HostConnect( logger = self.logger )
        self.hc_src.set_url( self.source_broker )
        self.hc_src.connect()

        # consumer  add_prefetch(1) allows queue sharing between instances

        self.consumer  = Consumer(self.hc_src)
        self.consumer.add_prefetch(1)
        self.consumer.build()

        # consumer queue
        name  = 'q_' + self.source_broker.username + '.' + self.program_name + '.' + self.config_name
        if self.queue_name != None :
           name = 'q_' + self.source_broker.username + '.' + self.queue_name

        self.queue = Queue(self.hc_src,name)
        self.queue.add_binding(self.source_exchange,self.source_topic)
        self.queue.build()

        # log publisher

        self.amqp_log    = Publisher(self.hc_src)
        self.amqp_log.build()

        # =============
        # publisher
        # =============

        # publisher host

        self.hc_pst = HostConnect( logger = self.logger )
        self.hc_pst.set_url( self.broker )
        self.hc_pst.connect()

        # publisher

        self.amqp_pub    = Publisher(self.hc_pst)
        self.amqp_pub.build()

    def configure(self):

        # installation general configurations and settings

        self.general()

        # arguments from command line

        self.args(self.user_args)

        # config from file

        self.config(self.user_config)

        # verify all settings

        self.check()

        self.setlog()
        self.logger.info("user_config = %d %s" % (self.instance,self.user_config))

    def delete_event(self):
        if self.msg.sumflg != 'R' : return False

        self.msg.code = 503
        self.msg.message = "Service unavailable : delete"
        self.msg.log_error()
 
        return True


    def download(self):

        self.logger.info("downloading/copying into %s " % self.msg.local_file)

        try :
                if   self.msg.url.scheme == 'http' :
                     return http_download(self.msg, self.http_user, self.http_password )

                elif self.msg.url.scheme == 'ftp' :
                     return ftp_download(self.msg, self.ftp_user, self.ftp_password, self.ftp_mode, self.ftp_binary )

                elif self.msg.url.scheme == 'sftp' :
                     return sftp_download(self.msg, self.sftp_user, self.sftp_password, self.sftp_keyfile )

                elif self.msg.url.scheme == 'file' :
                     return file_process(self.msg)

        except :
                (stype, svalue, tb) = sys.exc_info()
                self.logger.error("Download  Type: %s, Value: %s,  ..." % (stype, svalue))
                self.msg.code    = 503
                self.msg.message = "Unable to process"
                self.msg.log_error()

        self.msg.code    = 503
        self.msg.message = "Service unavailable %s" % self.msg.url.scheme
        self.msg.log_error()


    def help(self):
        self.logger.info("Usage: %s [OPTIONS] configfile [start|stop|restart|reload|status]\n" % self.program_name )
        self.logger.info("OPTIONS:")
        self.logger.info("-i   <nbr_of_instances>      default 1")
        self.logger.info("-b   <broker>                default amqp://guest:guest@localhost/")
        self.logger.info("-dr  <document_root>")
        self.logger.info("-ex  <exchange>              default xpublic")
        self.logger.info("-u   <url>")
        self.logger.info("-sb  <source_broker>         default amqp://guest:guest@localhost/")
        self.logger.info("-se  <source_exchange>       default xpublic")
        self.logger.info("-st  <source_topic>          default v02.post.#")
        self.logger.info("-qn  <queue_name>            default q_username.config_name")
        self.logger.info("-m   <mirror>                default True")
        self.logger.info("-ms  <message_validation_script>")
        self.logger.info("-fs  <file_validation_script>")
        self.logger.info("-sk  <ssh_keyfile>")
        self.logger.info("-strip <strip count (directory)>")
        self.logger.info("-in  <put parts inplace>      default True")
        self.logger.info("-o   <overwrite no sum check> default True")
        self.logger.info("-rc  <recompute sun>          default False")
        self.logger.info("DEBUG:")
        self.logger.info("-debug")

    def is_gateway_to_clusters(self):

        if not 'to' in self.msg.headers :
           self.msg.code    = 403
           self.msg.message = "Forbidden : message without destination amqp header['to']"
           self.msg.log_error()
           return False

        for target in self.msg.to_list :

           # target is this cluster
           if target == self.from_cluster : return True

           # target is this cluster's defined route
           if target == self.route : return True

           # target is an alias ... use its expand list
           if not cluster in self.aliases : continue

           for target2 in self.aliases[cluster] :
               if target2 == self.from_cluster : return True
               if target2 in self.route        : return True

        # nope this one is not for this cluster
        self.logger.warning("skipped : not for this cluster...")

        return False

    def set_local(self):

        # relative path by default mirror 

        self.rel_path = '%s' % self.msg.path
        if 'rename' in self.msg.headers :
           self.rel_path = '%s' % self.msg.headers['rename']

        # if we dont mirror force  yyyymmdd/source in front

        if not self.mirror :
           yyyymmdd = time.strftime("%Y%m%d",time.gmtime())
           self.rel_path = '%s/%s/%s' % (yyyymmdd,self.msg.headers['source'],self.msg.path)

           if 'rename' in self.msg.headers :
              self.rel_path = '%s/%s/%s' % (yyyymmdd,self.msg.headers['source'],self.msg.headers['rename'])
              self.rel_path = self.rel_path.replace('//','/')

        token = self.rel_path.split('/')
        self.filename = token[-1]

        # if strip is used... strip N heading directories

        if self.strip > 0 :
           if self.strip > len(token) : token = [token[-1]]
           else :                       token = token[self.strip:]
           self.rel_path = '/'.join(token)


        self.local_dir  = ''
        if self.document_root != None :
           self.local_dir = self.document_root 
        if len(token) > 1 :
           self.local_dir = self.local_dir + '/' + '/'.join(token[:-1])

        # Local directory (directory created if needed)

        self.local_dir  = self.local_dir.replace('//','/')
        self.local_file = self.local_dir   + '/' + self.filename
        self.local_url  = urllib.parse.urlparse(self.url.geturl() + '/' + self.rel_path)

        # we dont propagate renaming... once used get rid of it
        if 'rename' in self.msg.headers : del self.msg.headers['rename']

    def validate_file(self,target_file, offset, length):

        if self.file_script == None : return True

        ok, code, message = self.file_script(target_file, offset, length)

        if not ok :
           self.msg.code    = code
           self.msg.message = message
           self.msg.log_error()

        return ok

    def validate_message(self):

        if self.msg_script == None : return True

        ok, code, message = self.msg_script(self.msg)

        if not ok :
           self.msg.code    = code
           self.msg.message = message
           self.msg.log_error()

        return ok


    def run(self):

        self.logger.info("dd_sara run")

        self.connect()

        self.msg.logger       = self.logger
        self.msg.amqp_log     = self.amqp_log
        self.msg.amqp_pub     = self.amqp_pub
        self.msg.exchange_pub = self.exchange

        #
        # loop on all message
        #

        raw_msg = None

        while True :

          try  :
                 if raw_msg != None : self.consumer.ack(raw_msg)

                 raw_msg = self.consumer.consume(self.queue.qname)
                 if raw_msg == None : continue

                 # make use it as a dd_message

                 self.msg.from_amqplib(raw_msg)
                 self.logger.info("Received %s '%s' %s" % (self.msg.topic,self.msg.notice,self.msg.hdrstr))

                 # if message defines destinations

                 ok = self.is_gateway_to_clusters()
                 if not ok : continue

                 # setting source from exchange 

                 if self.source_from_exchange :
                    ok = self.set_source()
                    if not ok : continue

                 # setting originating cluster if not defined

                 if not 'from_cluster' in self.msg.headers :
                    ok = self.set_from_cluster()
                    if not ok : continue

                 # message validation

                 if not self.validate_message() : continue

                 # set local file according to sara : dr + imsg.path (or renamed path)

                 self.set_local()

                 # set local file according to the message and sara's setting

                 self.msg.set_local(self.inplace,self.local_file,self.local_url)

                 # asked to delete ?

                 if self.delete_event() : continue

                 # make sure local directory exists
                 # FIXME : logging errors...
                 try    : os.makedirs(self.local_dir,0o775,True)
                 except : pass

                 # if overwrite is not enforced (False)
                 # verify if msg checksum and local_file checksum match
                 # FIXME : should we republish / repost ???

                 if not self.overwrite and self.msg.checksum_match() :

                    self.msg.code    = 304
                    self.msg.message = 'not modified'
                    self.msg.log_info()
             
                    # a part unmodified can make a difference
                    if self.inplace and self.msg.in_partfile :
                       file_reassemble(self.msg)

                    # chksum computed on msg offset/length may need to truncate
                    file_truncate(self.msg)
                    continue

                 # proceed to download  3 attempts

                 i  = 0
                 while i < 3 : 
                       ok = self.download()
                       if ok : break
                       i = i + 1
                 if not ok : continue

                 # validate file/data

                 if not self.validate_file(self.msg.local_file, self.msg.local_offset, self.msg.length) : continue

                 # force recompute checksum

                 if self.recompute_chksum :
                    self.msg.compute_local_checksum()

                    # When downloaded, it changed from the message... 
                    # this is weird... means the file changed in the mean time
                    # and probably reposted...
                    # now posting of this file will have accurate checksum

                    if not self.msg.local_checksum == self.msg.checksum :
                       self.msg.set_sum(self.msg.sumflg,self.msg.local_checksum)
                       self.msg.code    = 205
                       self.msg.message = 'Reset Content : checksum'
                       self.msg.log_info()


                 # Delayed insertion
                 # try reassemble the file, conditions may have changed since writing

                 if self.inplace and self.msg.in_partfile :
                    self.msg.code    = 307
                    self.msg.message = 'Temporary Redirect'
                    self.msg.log_info()
                    file_reassemble(self.msg)
                    continue

                 # announcing the download or insert

                 if self.msg.partflg != '1' :
                    if self.inplace : self.msg.change_partflg('i')
                    else            : self.msg.change_partflg('p')

                 self.msg.set_topic_url('v02.post',self.msg.local_url)
                 self.msg.set_notice(self.msg.local_url,self.msg.time)
                 self.msg.code    = 201
                 self.msg.message = 'Published'
                 self.msg.publish()
              
                 # if we inserted a part in file ... try reassemble

                 if self.inplace and self.msg.partflg != '1' :
                    file_reassemble(self.msg)

          except :
                 (stype, svalue, tb) = sys.exc_info()
                 self.logger.error("Type: %s, Value: %s,  ..." % (stype, svalue))

    def set_from_cluster(self):
        if self.from_cluster == None :
           self.msg.code    = 403
           self.msg.message = "Forbidden : message without cluster"
           self.msg.log_error()
           return False

        self.msg.set_from_cluster(self.from_cluster)
        return True

    def set_source(self):
        if self.msg.exchange[:3] != 'xs_' :
           self.msg.code    = 403
           self.msg.message = "Forbidden : message without source"
           self.msg.log_error()
           return False

        source = self.msg.exchange[3:]
        self.msg.set_source(source)
        return True

    def reload(self):
        self.logger.info("dd_sara reload")
        self.close()
        self.configure()
        self.run()

    def start(self):
        self.configure()
        self.logger.info("dd_sara start")
        self.run()

    def stop(self):
        self.logger.info("dd_sara stop")
        self.close()
        os._exit(0)


# ===================================
# MAIN
# ===================================

def main():

    action = None
    args   = None
    config = None

    if len(sys.argv) >= 3 :
       action = sys.argv[-1]
       config = sys.argv[-2]
       if len(sys.argv) > 3: args = sys.argv[1:-2]

    sara = dd_sara(config,args)

    if   action == 'reload' : sara.reload_parent()
    elif action == 'restart': sara.restart_parent()
    elif action == 'start'  : sara.start_parent()
    elif action == 'stop'   : sara.stop_parent()
    elif action == 'status' : sara.status_parent()
    else :
           sara.logger.error("action unknown %s" % action)
           sys.exit(1)

    sys.exit(0)



# =========================================
# direct invocation
# =========================================

if __name__=="__main__":
   main()
